import asyncio
import os
from datetime import datetime
from typing import Dict, List, Optional
from playwright.async_api import async_playwright, Page, Browser
from supabase import create_client, Client
from dotenv import load_dotenv
from loguru import logger
import time

# Carregar variáveis de ambiente
load_dotenv()

class EaceAutomation:
    def __init__(self):
        self.supabase: Client = create_client(
            os.getenv("SUPABASE_URL"),
            os.getenv("SUPABASE_KEY")
        )
        self.username = os.getenv("EACE_USERNAME")
        self.password = os.getenv("EACE_PASSWORD")
        self.browser: Optional[Browser] = None
        self.page: Optional[Page] = None
        
    async def init_browser(self):
        """Inicializa o navegador com configurações anti-detecção"""
        playwright = await async_playwright().start()
        
        # Configurações para bypass de detecção
        self.browser = await playwright.chromium.launch(
            headless=False,  # Modo visível para bypass
            args=[
                '--no-sandbox',
                '--disable-blink-features=AutomationControlled',
                '--disable-web-security',
                '--disable-features=VizDisplayCompositor',
                '--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
            ]
        )
        
        self.page = await self.browser.new_page()
        
        # Configurar headers realistas
        await self.page.set_extra_http_headers({
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'pt-BR,pt;q=0.9,en;q=0.8',
            'Accept-Encoding': 'gzip, deflate, br',
            'DNT': '1',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
        })
        
        # Remover sinais de automação
        await self.page.add_init_script("""
            Object.defineProperty(navigator, 'webdriver', {
                get: () => undefined,
            });
        """)
        
        logger.info("Navegador inicializado com sucesso")
        
    async def login(self) -> bool:
        """Realiza login no sistema EACE"""
        try:
            logger.info("Iniciando processo de login...")
            
            await self.page.goto("https://eace.org.br/login?login=login", 
                                wait_until="networkidle")
            
            # Aguardar carregamento completo
            await self.page.wait_for_timeout(3000)
            
            # Tentar encontrar campos de login (adaptar conforme necessário)
            # Você precisará inspecionar o site real para encontrar os seletores corretos
            await self.page.fill('input[name="username"]', self.username)
            await self.page.fill('input[name="password"]', self.password)
            
            # Clicar no botão de login
            await self.page.click('button[type="submit"]')
            
            # Aguardar redirecionamento
            await self.page.wait_for_timeout(5000)
            
            # Verificar se login foi bem-sucedido
            if "dashboard" in self.page.url or "home" in self.page.url:
                logger.success("Login realizado com sucesso")
                return True
            else:
                logger.error("Falha no login - redirecionamento não ocorreu")
                return False
                
        except Exception as e:
            logger.error(f"Erro durante login: {str(e)}")
            return False
    
    async def abrir_ticket(self, ticket_data: Dict) -> bool:
        """Abre um ticket no sistema EACE"""
        try:
            logger.info(f"Abrindo ticket: {ticket_data.get('titulo', 'Sem título')}")
            
            # Navegar para página de abertura de ticket
            await self.page.goto("https://eace.org.br/tickets/novo", 
                                wait_until="networkidle")
            
            await self.page.wait_for_timeout(2000)
            
            # Preencher formulário (adaptar seletores conforme necessário)
            if ticket_data.get('titulo'):
                await self.page.fill('input[name="titulo"]', ticket_data['titulo'])
            
            if ticket_data.get('descricao'):
                await self.page.fill('textarea[name="descricao"]', ticket_data['descricao'])
            
            if ticket_data.get('categoria'):
                await self.page.select_option('select[name="categoria"]', ticket_data['categoria'])
            
            if ticket_data.get('prioridade'):
                await self.page.select_option('select[name="prioridade"]', ticket_data['prioridade'])
            
            # Submeter formulário
            await self.page.click('button[type="submit"]')
            
            # Aguardar confirmação
            await self.page.wait_for_timeout(3000)
            
            # Verificar se ticket foi criado (adaptar conforme necessário)
            if "sucesso" in self.page.url or await self.page.locator('.success-message').count() > 0:
                logger.success(f"Ticket '{ticket_data.get('titulo')}' criado com sucesso")
                return True
            else:
                logger.error("Falha na criação do ticket")
                return False
                
        except Exception as e:
            logger.error(f"Erro ao abrir ticket: {str(e)}")
            return False
    
    def get_tickets_pendentes(self) -> List[Dict]:
        """Busca tickets pendentes no Supabase"""
        try:
            response = self.supabase.table('tickets').select('*').eq('status', 'pendente').execute()
            logger.info(f"Encontrados {len(response.data)} tickets pendentes")
            return response.data
        except Exception as e:
            logger.error(f"Erro ao buscar tickets pendentes: {str(e)}")
            return []
    
    def atualizar_status_ticket(self, ticket_id: int, status: str, eace_id: str = None) -> bool:
        """Atualiza status do ticket no Supabase"""
        try:
            update_data = {
                'status': status,
                'updated_at': datetime.now().isoformat()
            }
            
            if eace_id:
                update_data['eace_id'] = eace_id
            
            self.supabase.table('tickets').update(update_data).eq('id', ticket_id).execute()
            logger.info(f"Status do ticket {ticket_id} atualizado para: {status}")
            return True
        except Exception as e:
            logger.error(f"Erro ao atualizar status do ticket {ticket_id}: {str(e)}")
            return False
    
    async def processar_tickets(self):
        """Processa todos os tickets pendentes"""
        tickets_pendentes = self.get_tickets_pendentes()
        
        if not tickets_pendentes:
            logger.info("Nenhum ticket pendente encontrado")
            return
        
        await self.init_browser()
        
        if not await self.login():
            logger.error("Falha no login - interrompendo processamento")
            return
        
        sucessos = 0
        falhas = 0
        
        for ticket in tickets_pendentes:
            try:
                if await self.abrir_ticket(ticket):
                    self.atualizar_status_ticket(ticket['id'], 'aberto')
                    sucessos += 1
                else:
                    self.atualizar_status_ticket(ticket['id'], 'erro')
                    falhas += 1
                
                # Aguardar entre tickets para evitar bloqueio
                await asyncio.sleep(2)
                
            except Exception as e:
                logger.error(f"Erro ao processar ticket {ticket['id']}: {str(e)}")
                self.atualizar_status_ticket(ticket['id'], 'erro')
                falhas += 1
        
        logger.info(f"Processamento concluído: {sucessos} sucessos, {falhas} falhas")
        
        await self.browser.close()
    
    async def close(self):
        """Fecha o navegador"""
        if self.browser:
            await self.browser.close()

async def main():
    """Função principal"""
    automation = EaceAutomation()
    
    try:
        await automation.processar_tickets()
    except KeyboardInterrupt:
        logger.info("Processamento interrompido pelo usuário")
    except Exception as e:
        logger.error(f"Erro inesperado: {str(e)}")
    finally:
        await automation.close()

if __name__ == "__main__":
    # Configurar logging
    logger.add("eace_automation.log", 
              rotation="1 day", 
              retention="7 days",
              level="INFO")
    
    asyncio.run(main())