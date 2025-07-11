#!/usr/bin/env python3
"""
Sistema de Webhook em Tempo Real para Automação EACE
Executa instantaneamente quando novo ticket é criado
"""

import asyncio
import logging
import os
import json
from datetime import datetime
from typing import Dict, Optional
from flask import Flask, request, jsonify
import threading
from supabase import create_client, Client
from eace_automation import EACEAutomation

# Configuração de logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('logs/webhook_realtime.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class EACEWebhookProcessor:
    def __init__(self, supabase_url: str, supabase_key: str):
        """
        Inicializa o processador de webhook
        
        Args:
            supabase_url: URL do Supabase
            supabase_key: Chave do Supabase
        """
        self.supabase: Client = create_client(supabase_url, supabase_key)
        self.processed_tickets = set()
        self.load_processed_tickets()
        
        logger.info("🚀 Webhook Processor inicializado")
    
    def load_processed_tickets(self):
        """Carrega IDs de tickets já processados"""
        try:
            with open('data/processed_tickets.json', 'r') as f:
                self.processed_tickets = set(json.load(f))
                logger.info(f"📋 Carregados {len(self.processed_tickets)} tickets processados")
        except FileNotFoundError:
            self.processed_tickets = set()
            logger.info("📋 Nenhum ticket processado anteriormente")
        except Exception as e:
            logger.error(f"❌ Erro ao carregar tickets processados: {e}")
            self.processed_tickets = set()
    
    def save_processed_tickets(self):
        """Salva IDs de tickets já processados"""
        try:
            os.makedirs('data', exist_ok=True)
            with open('data/processed_tickets.json', 'w') as f:
                json.dump(list(self.processed_tickets), f)
        except Exception as e:
            logger.error(f"❌ Erro ao salvar tickets processados: {e}")
    
    def extract_inep_from_site_name(self, site_nome: str) -> Optional[str]:
        """
        Extrai número INEP do nome do site
        
        Args:
            site_nome: Nome do site (ex: "INEP - 31382221")
            
        Returns:
            Número INEP ou None se não encontrado
        """
        try:
            if " - " in site_nome:
                parts = site_nome.split(" - ")
                if len(parts) >= 2:
                    inep = parts[1].strip()
                    # Valida se é um número de 8 dígitos
                    if inep.isdigit() and len(inep) == 8:
                        return inep
            
            # Tenta outras variações
            if "INEP" in site_nome.upper():
                import re
                # Procura por números de 8 dígitos após "INEP"
                match = re.search(r'INEP[:\s-]*(\d{8})', site_nome.upper())
                if match:
                    return match.group(1)
            
            return None
        except Exception as e:
            logger.error(f"❌ Erro ao extrair INEP de '{site_nome}': {e}")
            return None
    
    def get_ticket_data(self, ticket_id: int) -> Optional[Dict]:
        """
        Busca dados completos do ticket
        
        Args:
            ticket_id: ID do ticket
            
        Returns:
            Dados do ticket ou None se não encontrado
        """
        try:
            # Query para buscar dados completos do ticket
            response = self.supabase.table('tickets').select(
                '''
                id,
                incidente_id,
                descricao_enviada,
                data_abertura,
                incidentes (
                    id,
                    tipo,
                    status,
                    site_id,
                    sites (
                        id,
                        nome
                    )
                )
                '''
            ).eq('id', ticket_id).execute()
            
            if response.data:
                ticket_data = response.data[0]
                
                # Extrai INEP do nome do site
                site_nome = ticket_data['incidentes']['sites']['nome']
                numero_inep = self.extract_inep_from_site_name(site_nome)
                
                if numero_inep:
                    return {
                        'ticket_id': ticket_data['id'],
                        'incidente_id': ticket_data['incidente_id'],
                        'site_nome': site_nome,
                        'numero_inep': numero_inep,
                        'descricao': ticket_data['descricao_enviada'],
                        'data_abertura': ticket_data['data_abertura'],
                        'incidente_tipo': ticket_data['incidentes']['tipo']
                    }
                else:
                    logger.warning(f"⚠️ INEP não encontrado para ticket {ticket_id} - Site: {site_nome}")
                    return None
            else:
                logger.warning(f"⚠️ Ticket {ticket_id} não encontrado")
                return None
                
        except Exception as e:
            logger.error(f"❌ Erro ao buscar dados do ticket {ticket_id}: {e}")
            return None
    
    def update_ticket_status(self, ticket_id: int, eace_status: str, eace_os_numero: str = None):
        """
        Atualiza status do ticket no banco
        
        Args:
            ticket_id: ID do ticket
            eace_status: Status no EACE
            eace_os_numero: Número da OS criada
        """
        try:
            update_data = {
                'eace_status': eace_status,
                'eace_processado_em': datetime.now().isoformat()
            }
            
            if eace_os_numero:
                update_data['eace_os_numero'] = eace_os_numero
            
            self.supabase.table('tickets').update(update_data).eq('id', ticket_id).execute()
            logger.info(f"✅ Status do ticket {ticket_id} atualizado: {eace_status}")
            
        except Exception as e:
            logger.error(f"❌ Erro ao atualizar status do ticket {ticket_id}: {e}")
    
    def process_ticket(self, ticket_data: Dict) -> bool:
        """
        Processa um ticket criando OS no EACE
        
        Args:
            ticket_data: Dados do ticket
            
        Returns:
            True se processado com sucesso
        """
        ticket_id = ticket_data['ticket_id']
        numero_inep = ticket_data['numero_inep']
        
        try:
            logger.info(f"🎯 Processando ticket {ticket_id} - INEP: {numero_inep}")
            
            # Verifica se já foi processado
            if ticket_id in self.processed_tickets:
                logger.info(f"⚠️ Ticket {ticket_id} já foi processado anteriormente")
                return True
            
            # Atualiza status para 'PROCESSANDO'
            self.update_ticket_status(ticket_id, 'PROCESSANDO')
            
            # Executa automação EACE
            automation = EACEAutomation()
            resultado = automation.criar_os(numero_inep)
            
            if resultado['sucesso']:
                # Atualiza status para 'CONCLUIDO'
                self.update_ticket_status(
                    ticket_id, 
                    'CONCLUIDO', 
                    resultado['numero_os']
                )
                
                # Adiciona aos processados
                self.processed_tickets.add(ticket_id)
                self.save_processed_tickets()
                
                logger.info(f"✅ Ticket {ticket_id} processado com sucesso - OS: {resultado['numero_os']}")
                return True
            else:
                # Atualiza status para 'ERRO'
                self.update_ticket_status(ticket_id, 'ERRO')
                logger.error(f"❌ Erro ao processar ticket {ticket_id}: {resultado['erro']}")
                return False
                
        except Exception as e:
            logger.error(f"❌ Erro ao processar ticket {ticket_id}: {e}")
            # Atualiza status para 'ERRO'
            self.update_ticket_status(ticket_id, 'ERRO')
            return False
    
    def handle_webhook(self, payload: Dict) -> Dict:
        """
        Processa webhook recebido
        
        Args:
            payload: Dados do webhook
            
        Returns:
            Resultado do processamento
        """
        try:
            logger.info(f"📥 Webhook recebido: {payload}")
            
            # Extrai informações do payload
            event_type = payload.get('type', '')
            table = payload.get('table', '')
            record = payload.get('record', {})
            
            # Verifica se é um INSERT na tabela tickets
            if event_type == 'INSERT' and table == 'tickets':
                ticket_id = record.get('id')
                
                if ticket_id:
                    # Busca dados completos do ticket
                    ticket_data = self.get_ticket_data(ticket_id)
                    
                    if ticket_data:
                        # Processa o ticket em thread separada para não bloquear
                        def process_async():
                            success = self.process_ticket(ticket_data)
                            if success:
                                logger.info(f"🎉 Ticket {ticket_id} processado com sucesso via webhook")
                            else:
                                logger.error(f"💥 Falha ao processar ticket {ticket_id} via webhook")
                        
                        thread = threading.Thread(target=process_async)
                        thread.daemon = True
                        thread.start()
                        
                        return {
                            'success': True,
                            'message': f'Ticket {ticket_id} sendo processado',
                            'ticket_id': ticket_id
                        }
                    else:
                        return {
                            'success': False,
                            'message': f'Dados do ticket {ticket_id} não encontrados ou INEP inválido'
                        }
                else:
                    return {
                        'success': False,
                        'message': 'ID do ticket não encontrado no payload'
                    }
            else:
                return {
                    'success': False,
                    'message': f'Evento ignorado: {event_type} na tabela {table}'
                }
                
        except Exception as e:
            logger.error(f"❌ Erro ao processar webhook: {e}")
            return {
                'success': False,
                'message': f'Erro interno: {str(e)}'
            }

# Aplicação Flask para receber webhooks
app = Flask(__name__)

# Inicializa o processador
SUPABASE_URL = os.getenv('SUPABASE_URL')
SUPABASE_KEY = os.getenv('SUPABASE_KEY')

if not SUPABASE_URL or not SUPABASE_KEY:
    logger.error("❌ Variáveis de ambiente SUPABASE_URL e SUPABASE_KEY são obrigatórias")
    exit(1)

processor = EACEWebhookProcessor(SUPABASE_URL, SUPABASE_KEY)

@app.route('/webhook/eace', methods=['POST'])
def webhook_eace():
    """Endpoint para receber webhooks do Supabase"""
    try:
        payload = request.json
        result = processor.handle_webhook(payload)
        
        if result['success']:
            return jsonify(result), 200
        else:
            return jsonify(result), 400
            
    except Exception as e:
        logger.error(f"❌ Erro no endpoint webhook: {e}")
        return jsonify({
            'success': False,
            'message': f'Erro interno: {str(e)}'
        }), 500

@app.route('/webhook/test', methods=['POST'])
def webhook_test():
    """Endpoint para testar webhook manualmente"""
    try:
        data = request.json
        ticket_id = data.get('ticket_id')
        
        if not ticket_id:
            return jsonify({
                'success': False,
                'message': 'ticket_id é obrigatório'
            }), 400
        
        # Simula payload do Supabase
        payload = {
            'type': 'INSERT',
            'table': 'tickets',
            'record': {'id': ticket_id}
        }
        
        result = processor.handle_webhook(payload)
        return jsonify(result), 200 if result['success'] else 400
        
    except Exception as e:
        logger.error(f"❌ Erro no teste webhook: {e}")
        return jsonify({
            'success': False,
            'message': f'Erro interno: {str(e)}'
        }), 500

@app.route('/status', methods=['GET'])
def status():
    """Endpoint para verificar status do sistema"""
    try:
        return jsonify({
            'status': 'running',
            'processed_tickets': len(processor.processed_tickets),
            'timestamp': datetime.now().isoformat()
        }), 200
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500

if __name__ == "__main__":
    # Cria diretórios necessários
    os.makedirs('logs', exist_ok=True)
    os.makedirs('data', exist_ok=True)
    
    logger.info("🚀 Iniciando servidor webhook EACE...")
    logger.info("📡 Endpoints disponíveis:")
    logger.info("  POST /webhook/eace - Webhook principal")
    logger.info("  POST /webhook/test - Teste manual")
    logger.info("  GET /status - Status do sistema")
    
    # Inicia servidor Flask
    app.run(
        host='0.0.0.0',
        port=int(os.getenv('PORT', 5000)),
        debug=False
    )