#!/usr/bin/env python3
"""
Versão simplificada do webhook para teste
"""

from flask import Flask, request, jsonify, send_file
import os
import logging
from datetime import datetime
import glob
import base64

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

app = Flask(__name__)

@app.route('/status', methods=['GET'])
def status():
    """Health check endpoint"""
    return jsonify({
        'status': 'online',
        'service': 'EACE Webhook System',
        'timestamp': datetime.now().isoformat(),
        'version': '1.0.0-simple'
    })

@app.route('/webhook/test', methods=['POST'])
def webhook_test():
    """Teste básico do webhook"""
    data = request.json or {}
    logger.info(f"Webhook test recebido: {data}")
    
    return jsonify({
        'status': 'success',
        'message': 'Webhook test funcionando',
        'received_data': data,
        'timestamp': datetime.now().isoformat()
    })

@app.route('/webhook/eace', methods=['POST'])
def webhook_eace():
    """Simulação do webhook EACE"""
    data = request.json or {}
    logger.info(f"Webhook EACE recebido: {data}")
    
    # Simular processamento
    record = data.get('record', {})
    descricao = record.get('descricao_enviada', '')
    
    # Extrair INEP (simulação)
    inep = "31382221"
    if 'INEP' in descricao:
        try:
            import re
            match = re.search(r'INEP.*?(\d{8})', descricao)
            if match:
                inep = match.group(1)
        except:
            pass
    
    return jsonify({
        'status': 'success',
        'message': 'Webhook EACE processado (simulação)',
        'extracted_inep': inep,
        'description': descricao,
        'timestamp': datetime.now().isoformat(),
        'note': 'Versão simplificada - sem automação real'
    })

@app.route('/', methods=['GET'])
def home():
    """Página inicial"""
    return jsonify({
        'service': 'EACE Webhook System',
        'status': 'running',
        'version': '1.0.0-simple',
        'endpoints': {
            'status': '/status',
            'webhook_test': '/webhook/test',
            'webhook_eace': '/webhook/eace',
            'screenshots': '/screenshots',
            'latest_screenshot': '/screenshots/latest',
            'screenshots_gallery': '/screenshots/gallery'
        },
        'note': 'Versão simplificada para teste'
    })

@app.route('/screenshots', methods=['GET'])
def list_screenshots():
    """Lista todos os screenshots disponíveis"""
    try:
        screenshots_dir = "/tmp/screenshots"
        if not os.path.exists(screenshots_dir):
            return jsonify({
                'status': 'error',
                'message': 'Diretório de screenshots não encontrado',
                'screenshots': []
            })
        
        # Listar arquivos PNG
        files = glob.glob(os.path.join(screenshots_dir, "*.png"))
        screenshots = []
        
        for file_path in sorted(files, key=os.path.getctime, reverse=True):
            filename = os.path.basename(file_path)
            file_stats = os.stat(file_path)
            
            screenshots.append({
                'filename': filename,
                'size': file_stats.st_size,
                'created': datetime.fromtimestamp(file_stats.st_ctime).isoformat(),
                'download_url': f'/screenshot/{filename}'
            })
        
        return jsonify({
            'status': 'success',
            'total_screenshots': len(screenshots),
            'screenshots': screenshots
        })
        
    except Exception as e:
        logger.error(f"Erro ao listar screenshots: {e}")
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500

@app.route('/screenshot/<filename>', methods=['GET'])
def get_screenshot(filename):
    """Retorna um screenshot específico"""
    try:
        screenshots_dir = "/tmp/screenshots"
        file_path = os.path.join(screenshots_dir, filename)
        
        if not os.path.exists(file_path):
            return jsonify({
                'status': 'error',
                'message': 'Screenshot não encontrado'
            }), 404
        
        return send_file(file_path, mimetype='image/png')
        
    except Exception as e:
        logger.error(f"Erro ao servir screenshot: {e}")
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500

@app.route('/screenshots/latest', methods=['GET'])
def get_latest_screenshot():
    """Retorna o screenshot mais recente"""
    try:
        screenshots_dir = "/tmp/screenshots"
        if not os.path.exists(screenshots_dir):
            return jsonify({
                'status': 'error',
                'message': 'Diretório de screenshots não encontrado'
            }), 404
        
        # Encontrar o arquivo mais recente
        files = glob.glob(os.path.join(screenshots_dir, "*.png"))
        if not files:
            return jsonify({
                'status': 'error',
                'message': 'Nenhum screenshot encontrado'
            }), 404
        
        latest_file = max(files, key=os.path.getctime)
        return send_file(latest_file, mimetype='image/png')
        
    except Exception as e:
        logger.error(f"Erro ao obter último screenshot: {e}")
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500

@app.route('/screenshots/gallery', methods=['GET'])
def screenshots_gallery():
    """Retorna uma galeria HTML dos screenshots"""
    try:
        screenshots_dir = "/tmp/screenshots"
        if not os.path.exists(screenshots_dir):
            return "<h1>Nenhum screenshot encontrado</h1>"
        
        files = glob.glob(os.path.join(screenshots_dir, "*.png"))
        if not files:
            return "<h1>Nenhum screenshot encontrado</h1>"
        
        files.sort(key=os.path.getctime, reverse=True)
        
        html = """
        <html>
        <head>
            <title>Screenshots EACE Automation</title>
            <style>
                body { font-family: Arial, sans-serif; margin: 20px; }
                .screenshot { margin: 20px 0; border: 1px solid #ccc; padding: 10px; }
                .screenshot img { max-width: 800px; height: auto; }
                .info { background: #f5f5f5; padding: 10px; margin: 10px 0; }
            </style>
        </head>
        <body>
            <h1>Screenshots da Automação EACE</h1>
            <p>Última atualização: {}</p>
        """.format(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        
        for file_path in files:
            filename = os.path.basename(file_path)
            file_stats = os.stat(file_path)
            created_time = datetime.fromtimestamp(file_stats.st_ctime).strftime("%Y-%m-%d %H:%M:%S")
            
            html += f"""
            <div class="screenshot">
                <div class="info">
                    <strong>Arquivo:</strong> {filename}<br>
                    <strong>Criado:</strong> {created_time}<br>
                    <strong>Tamanho:</strong> {file_stats.st_size} bytes
                </div>
                <img src="/screenshot/{filename}" alt="{filename}">
            </div>
            """
        
        html += """
        </body>
        </html>
        """
        
        return html
        
    except Exception as e:
        logger.error(f"Erro ao gerar galeria: {e}")
        return f"<h1>Erro ao gerar galeria: {e}</h1>"

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    logger.info(f"🚀 Iniciando EACE Webhook (versão simples) na porta {port}")
    logger.info(f"🌐 Endpoints disponíveis:")
    logger.info(f"   - Status: http://0.0.0.0:{port}/status")
    logger.info(f"   - Screenshots: http://0.0.0.0:{port}/screenshots")
    logger.info(f"   - Galeria: http://0.0.0.0:{port}/screenshots/gallery")
    
    try:
        app.run(host='0.0.0.0', port=port, debug=False)
    except Exception as e:
        logger.error(f"Erro ao iniciar aplicação: {e}")
        raise