#!/usr/bin/env python3
"""
Versão simplificada do webhook para teste
"""

from flask import Flask, request, jsonify, send_file, send_from_directory
import os
import logging
from datetime import datetime
import glob
import base64
import threading
import subprocess

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
    """Página inicial - interface HTML"""
    try:
        # Tenta servir o arquivo HTML
        if os.path.exists('endpoints.html'):
            return send_file('endpoints.html')
        else:
            # Se não existir, tenta com caminho absoluto
            abs_path = os.path.abspath('endpoints.html')
            if os.path.exists(abs_path):
                return send_file(abs_path)
            else:
                raise FileNotFoundError("endpoints.html não encontrado")
    except Exception as e:
        logger.error(f"Erro ao servir endpoints.html: {e}")
        # Fallback para JSON se arquivo não existir
        return jsonify({
            'service': 'EACE Webhook System',
            'status': 'running',
            'version': '1.0.0-simple',
            'message': 'Interface HTML não encontrada - usando fallback JSON',
            'endpoints': {
                'status': '/status',
                'webhook_test': '/webhook/test',
                'webhook_eace': '/webhook/eace',
                'screenshots': '/screenshots',
                'latest_screenshot': '/screenshots/latest',
                'screenshots_gallery': '/screenshots/gallery',
                'run_test': '/run-test',
                'inspect_page': '/inspect-page',
                'test_menu_navigation': '/test-menu-navigation',
                'test_bubble_structure': '/test-bubble-structure',
                'test_direct_click': '/test-direct-click',
                'test_smart_menu': '/test-smart-menu',
                'test_expandable_menu': '/test-expandable-menu',
                'test_os_page_mapping': '/test-os-page-mapping',
                'map_adicionar_os_button': '/map-adicionar-os-button'
            },
            'note': 'Acesse /endpoints.html para interface visual ou /debug para diagnóstico'
        })

@app.route('/debug', methods=['GET'])
def debug_files():
    """Debug - lista arquivos no diretório"""
    try:
        files = os.listdir('.')
        return jsonify({
            'current_directory': os.getcwd(),
            'files': files,
            'endpoints_html_exists': os.path.exists('endpoints.html'),
            'endpoints_html_size': os.path.getsize('endpoints.html') if os.path.exists('endpoints.html') else 0
        })
    except Exception as e:
        return jsonify({'error': str(e)})

@app.route('/endpoints.html', methods=['GET'])
def endpoints_page():
    """Serve a página HTML dos endpoints"""
    try:
        return send_file('endpoints.html')
    except Exception as e:
        logger.error(f"Erro ao servir endpoints.html: {e}")
        return jsonify({
            'error': 'Arquivo endpoints.html não encontrado',
            'message': 'Use /api para informações JSON'
        }), 404

@app.route('/api', methods=['GET'])
def api_info():
    """Informações da API em formato JSON"""
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
            'screenshots_gallery': '/screenshots/gallery',
            'run_test': '/run-test',
            'inspect_page': '/inspect-page',
            'test_menu_navigation': '/test-menu-navigation',
            'test_bubble_structure': '/test-bubble-structure',
            'test_direct_click': '/test-direct-click',
            'test_smart_menu': '/test-smart-menu',
            'test_expandable_menu': '/test-expandable-menu',
            'test_os_page_mapping': '/test-os-page-mapping',
            'map_adicionar_os_button': '/map-adicionar-os-button'
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
            <p>Última atualização: """ + datetime.now().strftime("%Y-%m-%d %H:%M:%S") + """</p>
        """
        
        for file_path in files:
            filename = os.path.basename(file_path)
            file_stats = os.stat(file_path)
            created_time = datetime.fromtimestamp(file_stats.st_ctime).strftime("%Y-%m-%d %H:%M:%S")
            
            html += """
            <div class="screenshot">
                <div class="info">
                    <strong>Arquivo:</strong> """ + filename + """<br>
                    <strong>Criado:</strong> """ + created_time + """<br>
                    <strong>Tamanho:</strong> """ + str(file_stats.st_size) + """ bytes
                </div>
                <img src="/screenshot/""" + filename + """" alt=\"""" + filename + """\">
            </div>
            """
        
        html += """
        </body>
        </html>
        """
        
        return html
        
    except Exception as e:
        logger.error(f"Erro ao gerar galeria: {e}")
        return "<h1>Erro ao gerar galeria: " + str(e) + "</h1>"

@app.route('/run-test', methods=['POST', 'GET'])
def run_automation_test():
    """Executa o teste de automação"""
    try:
        import subprocess
        import threading
        
        def run_test():
            try:
                # Criar diretório de screenshots se não existir
                screenshots_dir = "/tmp/screenshots"
                os.makedirs(screenshots_dir, exist_ok=True)
                
                # Definir variáveis de ambiente
                env = os.environ.copy()
                env['EACE_USERNAME'] = 'raiseupbt@gmail.com'
                env['EACE_PASSWORD'] = '@Uujpgi8u'
                env['DISPLAY'] = ':99'
                
                # Iniciar Xvfb se necessário
                try:
                    subprocess.run(['Xvfb', ':99', '-screen', '0', '1024x768x24'], 
                                 env=env, timeout=5, capture_output=True)
                except:
                    pass  # Pode já estar rodando
                
                # Código Python inline para teste básico
                test_code = '''
import asyncio
import os
from datetime import datetime
from playwright.async_api import async_playwright

async def test_login():
    screenshots_dir = "/tmp/screenshots"
    os.makedirs(screenshots_dir, exist_ok=True)
    
    playwright = await async_playwright().start()
    browser = await playwright.chromium.launch(headless=True)
    page = await browser.new_page()
    
    try:
        # Ir para página de login
        await page.goto("https://eace.org.br/login?login=login")
        await page.wait_for_timeout(3000)
        
        # Screenshot inicial
        await page.screenshot(path=f"{screenshots_dir}/01_login_page.png")
        
        # Preencher credenciais
        await page.fill('//input[@placeholder="seuemail@email.com"]', "raiseupbt@gmail.com")
        await page.fill('//input[@type="password"]', "@Uujpgi8u")
        await page.screenshot(path=f"{screenshots_dir}/02_credentials_filled.png")
        
        # Fazer login
        await page.click('//button[contains(text(), "Log In")]')
        await page.wait_for_timeout(5000)
        await page.screenshot(path=f"{screenshots_dir}/03_after_login.png")
        
        # Selecionar perfil se necessário
        if await page.locator('//*[contains(text(), "Fornecedor")]').count() > 0:
            await page.click('//*[contains(text(), "Fornecedor")]')
            await page.wait_for_timeout(5000)
            await page.screenshot(path=f"{screenshots_dir}/04_profile_selected.png")
        
        # Screenshot final do dashboard
        await page.screenshot(path=f"{screenshots_dir}/05_dashboard.png")
        
        # Aguardar um pouco para garantir que a página carregou
        await page.wait_for_timeout(3000)
        
        # Procurar pelo menu hamburguer ou menu lateral
        print("🔍 Procurando menu lateral...")
        
        # Tentar diferentes seletores para o menu
        menu_selectors = [
            "button[aria-label*='menu']",
            "button[class*='menu']",
            "button[class*='hamburger']",
            ".menu-toggle",
            ".hamburger",
            "[data-testid*='menu']",
            "svg[class*='menu']",
            "div[class*='menu-button']",
            "//button[contains(@class, 'menu')]",
            "//div[contains(@class, 'menu')]//button",
            "//button[@aria-label='menu']"
        ]
        
        menu_found = False
        for selector in menu_selectors:
            try:
                if selector.startswith("//"):
                    elements = await page.locator(selector).count()
                else:
                    elements = await page.locator(selector).count()
                
                if elements > 0:
                    print(f"✅ Menu encontrado com seletor: {selector}")
                    if selector.startswith("//"):
                        await page.locator(selector).first.click()
                    else:
                        await page.locator(selector).first.click()
                    menu_found = True
                    await page.wait_for_timeout(2000)
                    await page.screenshot(path=f"{screenshots_dir}/06_menu_opened.png")
                    break
            except Exception as e:
                continue
        
        # Se não encontrou o menu, tentar procurar por texto "OS" ou "Menu"
        if not menu_found:
            print("🔍 Procurando por links de OS ou Menu...")
            os_selectors = [
                "//a[contains(text(), 'OS')]",
                "//button[contains(text(), 'OS')]",
                "//div[contains(text(), 'OS')]",
                "//a[contains(text(), 'Menu')]",
                "//button[contains(text(), 'Menu')]",
                "//div[contains(text(), 'Menu')]",
                "//a[contains(@href, 'os')]",
                "//a[contains(@href, 'ordem')]",
                "//a[contains(@href, 'servico')]",
                "[href*='os']",
                "[href*='ordem']",
                "[href*='servico']"
            ]
            
            for selector in os_selectors:
                try:
                    if selector.startswith("//"):
                        elements = await page.locator(selector).count()
                    else:
                        elements = await page.locator(selector).count()
                    
                    if elements > 0:
                        print(f"✅ Link OS encontrado com seletor: {selector}")
                        if selector.startswith("//"):
                            await page.locator(selector).first.click()
                        else:
                            await page.locator(selector).first.click()
                        await page.wait_for_timeout(5000)
                        await page.screenshot(path=f"{screenshots_dir}/07_os_page.png")
                        menu_found = True
                        break
                except Exception as e:
                    continue
        
        # Se ainda não encontrou, vamos explorar a estrutura da página
        if not menu_found:
            print("🔍 Explorando estrutura da página...")
            await page.screenshot(path=f"{screenshots_dir}/06_page_structure.png")
            
            # Tentar encontrar todos os elementos clicáveis
            try:
                # Procurar por elementos com ícones ou que podem ser menu
                clickable_elements = await page.evaluate("""
                    () => {
                        const elements = [];
                        const selectors = ['button', 'a', '[role="button"]', 'div[onclick]', '.menu', '.nav'];
                        
                        selectors.forEach(selector => {
                            document.querySelectorAll(selector).forEach(el => {
                                const text = el.textContent?.trim() || '';
                                const classes = el.className || '';
                                const href = el.href || '';
                                
                                if (text.toLowerCase().includes('menu') || 
                                    text.toLowerCase().includes('os') ||
                                    classes.toLowerCase().includes('menu') ||
                                    classes.toLowerCase().includes('hamburger') ||
                                    href.toLowerCase().includes('os')) {
                                    elements.push({
                                        text: text,
                                        classes: classes,
                                        href: href,
                                        tagName: el.tagName
                                    });
                                }
                            });
                        });
                        
                        return elements;
                    }
                """)
                
                print(f"📋 Elementos encontrados: {clickable_elements}")
                
                # Tentar clicar no primeiro elemento que pareça ser um menu
                if clickable_elements:
                    first_element = clickable_elements[0]
                    print(f"🔗 Tentando clicar no primeiro elemento: {first_element}")
                    
                    # Tentar diferentes maneiras de clicar
                    try:
                        await page.click(f"text='{first_element['text']}'")
                        await page.wait_for_timeout(3000)
                        await page.screenshot(path=f"{screenshots_dir}/07_clicked_element.png")
                    except:
                        pass
                        
            except Exception as e:
                print(f"❌ Erro ao explorar página: {e}")
        
        # Screenshot final
        await page.screenshot(path=f"{screenshots_dir}/08_final_exploration.png")
        
        print(f"✅ Exploration completed - URL: {page.url}")
        print(f"📸 Screenshots salvos em: {screenshots_dir}")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        await page.screenshot(path=f"{screenshots_dir}/error.png")
    
    finally:
        await browser.close()
        await playwright.stop()

if __name__ == "__main__":
    asyncio.run(test_login())
'''
                
                # Executar código Python
                result = subprocess.run([
                    'python3', '-c', test_code
                ], env=env, capture_output=True, text=True, timeout=300)
                
                logger.info(f"Teste executado - Return code: {result.returncode}")
                logger.info(f"Stdout: {result.stdout}")
                if result.stderr:
                    logger.error(f"Stderr: {result.stderr}")
                    
            except Exception as e:
                logger.error(f"Erro ao executar teste: {e}")
        
        # Executar em thread separada para não bloquear
        thread = threading.Thread(target=run_test)
        thread.daemon = True
        thread.start()
        
        return jsonify({
            'status': 'success',
            'message': 'Teste de automação iniciado',
            'note': 'Aguarde alguns minutos e verifique os screenshots',
            'endpoints': {
                'gallery': '/screenshots/gallery',
                'screenshots': '/screenshots',
                'latest': '/screenshots/latest'
            }
        })
        
    except Exception as e:
        logger.error(f"Erro ao iniciar teste: {e}")
        return jsonify({
            'status': 'error',
            'message': f'Erro ao iniciar teste: {e}'
        }), 500

@app.route('/inspect-page', methods=['POST', 'GET'])
def inspect_page():
    """Inspeciona a página atual do dashboard para encontrar elementos de menu"""
    try:
        import subprocess
        import threading
        
        def run_inspection():
            try:
                # Criar diretório de screenshots se não existir
                screenshots_dir = "/tmp/screenshots"
                os.makedirs(screenshots_dir, exist_ok=True)
                
                # Definir variáveis de ambiente
                env = os.environ.copy()
                env['EACE_USERNAME'] = 'raiseupbt@gmail.com'
                env['EACE_PASSWORD'] = '@Uujpgi8u'
                env['DISPLAY'] = ':99'
                
                # Código Python para inspeção detalhada
                inspection_code = '''
import asyncio
import json
from playwright.async_api import async_playwright

async def inspect_dashboard():
    screenshots_dir = "/tmp/screenshots"
    
    playwright = await async_playwright().start()
    browser = await playwright.chromium.launch(headless=True)
    page = await browser.new_page()
    
    try:
        # Fazer login primeiro
        await page.goto("https://eace.org.br/login?login=login")
        await page.wait_for_timeout(3000)
        
        await page.fill('//input[@placeholder="seuemail@email.com"]', "raiseupbt@gmail.com")
        await page.fill('//input[@type="password"]', "@Uujpgi8u")
        await page.click('//button[contains(text(), "Log In")]')
        await page.wait_for_timeout(5000)
        
        # Selecionar perfil se necessário
        if await page.locator('//*[contains(text(), "Fornecedor")]').count() > 0:
            await page.click('//*[contains(text(), "Fornecedor")]')
            await page.wait_for_timeout(5000)
        
        # Agora inspecionar a página
        print("🔍 Inspecionando dashboard...")
        
        # Obter informações da página
        page_info = await page.evaluate("""
            () => {
                const info = {
                    url: window.location.href,
                    title: document.title,
                    body_classes: document.body.className,
                    all_buttons: [],
                    all_links: [],
                    menu_elements: [],
                    navigation_elements: []
                };
                
                // Todos os botões
                document.querySelectorAll('button').forEach((btn, index) => {
                    info.all_buttons.push({
                        index: index,
                        text: btn.textContent?.trim() || '',
                        classes: btn.className || '',
                        id: btn.id || '',
                        visible: btn.offsetParent !== null
                    });
                });
                
                // Todos os links
                document.querySelectorAll('a').forEach((link, index) => {
                    info.all_links.push({
                        index: index,
                        text: link.textContent?.trim() || '',
                        href: link.href || '',
                        classes: link.className || '',
                        id: link.id || ''
                    });
                });
                
                // Elementos que podem ser menu
                const menuSelectors = [
                    'nav', '[role="navigation"]', '.menu', '.nav', 
                    '[class*="menu"]', '[class*="nav"]', '[class*="sidebar"]',
                    'button[aria-label*="menu"]', 'button[class*="menu"]'
                ];
                
                menuSelectors.forEach(selector => {
                    document.querySelectorAll(selector).forEach(el => {
                        info.menu_elements.push({
                            selector: selector,
                            text: el.textContent?.trim() || '',
                            classes: el.className || '',
                            id: el.id || '',
                            tagName: el.tagName
                        });
                    });
                });
                
                // Elementos de navegação específicos
                const navTexts = ['dashboard', 'menu', 'os', 'ordem', 'serviço'];
                navTexts.forEach(text => {
                    const elements = document.querySelectorAll(`*`);
                    elements.forEach(el => {
                        const content = el.textContent?.toLowerCase() || '';
                        if (content.includes(text) && content.length < 50) {
                            info.navigation_elements.push({
                                search_term: text,
                                text: el.textContent?.trim() || '',
                                tagName: el.tagName,
                                classes: el.className || '',
                                id: el.id || ''
                            });
                        }
                    });
                });
                
                return info;
            }
        """)
        
        # Salvar informações em arquivo
        with open(f"{screenshots_dir}/page_inspection.json", "w") as f:
            json.dump(page_info, f, indent=2)
        
        # Screenshot da página atual
        await page.screenshot(path=f"{screenshots_dir}/inspection_screenshot.png")
        
        print("✅ Inspeção concluída")
        print(f"📊 Encontrados: {len(page_info['all_buttons'])} botões, {len(page_info['all_links'])} links")
        print(f"🔍 Elementos de menu: {len(page_info['menu_elements'])}")
        print(f"🧭 Elementos de navegação: {len(page_info['navigation_elements'])}")
        
        return page_info
        
    except Exception as e:
        print(f"❌ Erro na inspeção: {e}")
        return {"error": str(e)}
    
    finally:
        await browser.close()
        await playwright.stop()

if __name__ == "__main__":
    result = asyncio.run(inspect_dashboard())
    print(json.dumps(result, indent=2))
'''
                
                # Executar código Python
                result = subprocess.run([
                    'python3', '-c', inspection_code
                ], env=env, capture_output=True, text=True, timeout=300)
                
                logger.info(f"Inspeção executada - Return code: {result.returncode}")
                logger.info(f"Stdout: {result.stdout}")
                if result.stderr:
                    logger.error(f"Stderr: {result.stderr}")
                    
            except Exception as e:
                logger.error(f"Erro ao executar inspeção: {e}")
        
        # Executar em thread separada
        thread = threading.Thread(target=run_inspection)
        thread.daemon = True
        thread.start()
        
        return jsonify({
            'status': 'success',
            'message': 'Inspeção da página iniciada',
            'note': 'Aguarde alguns minutos e verifique o arquivo page_inspection.json nos screenshots',
            'info': 'Este endpoint analisa todos os elementos da página para encontrar menus e navegação'
        })
        
    except Exception as e:
        logger.error(f"Erro ao iniciar inspeção: {e}")
        return jsonify({
            'status': 'error',
            'message': f'Erro ao iniciar inspeção: {e}'
        }), 500

@app.route('/test-menu-navigation', methods=['POST', 'GET'])
def test_menu_navigation():
    """Testa navegação específica para o segundo item do menu lateral"""
    try:
        import subprocess
        import threading
        
        def run_menu_test():
            try:
                # Criar diretório de screenshots se não existir
                screenshots_dir = "/tmp/screenshots"
                os.makedirs(screenshots_dir, exist_ok=True)
                
                # Definir variáveis de ambiente
                env = os.environ.copy()
                env['EACE_USERNAME'] = 'raiseupbt@gmail.com'
                env['EACE_PASSWORD'] = '@Uujpgi8u'
                env['DISPLAY'] = ':99'
                
                # Código Python para teste específico do menu
                menu_test_code = '''
import asyncio
import json
from playwright.async_api import async_playwright

async def test_menu_navigation():
    screenshots_dir = "/tmp/screenshots"
    
    playwright = await async_playwright().start()
    browser = await playwright.chromium.launch(headless=True)
    page = await browser.new_page()
    
    try:
        # Fazer login primeiro
        print("🔐 Fazendo login...")
        await page.goto("https://eace.org.br/login?login=login")
        await page.wait_for_timeout(3000)
        
        await page.fill('//input[@placeholder="seuemail@email.com"]', "raiseupbt@gmail.com")
        await page.fill('//input[@type="password"]', "@Uujpgi8u")
        await page.click('//button[contains(text(), "Log In")]')
        await page.wait_for_timeout(5000)
        
        # Selecionar perfil se necessário
        if await page.locator('//*[contains(text(), "Fornecedor")]').count() > 0:
            await page.click('//*[contains(text(), "Fornecedor")]')
            await page.wait_for_timeout(5000)
        
        # Screenshot do dashboard
        await page.screenshot(path=f"{screenshots_dir}/menu_01_dashboard.png")
        print("✅ Login realizado, agora procurando menu lateral...")
        
        # Estratégia 1: Procurar especificamente pelo segundo ícone do menu lateral
        print("🔍 Estratégia 1: Procurando segundo ícone do menu lateral...")
        sidebar_found = False
        
        # Seletores específicos baseados na imagem do sistema
        sidebar_selectors = [
            "aside a:nth-child(2)",
            "nav a:nth-child(2)", 
            ".sidebar a:nth-child(2)",
            "div[class*='sidebar'] a:nth-child(2)",
            "div[class*='menu'] a:nth-child(2)",
            "ul li:nth-child(2) a",
            "ul li:nth-child(2)",
            "nav ul li:nth-child(2)",
            "aside ul li:nth-child(2)"
        ]
        
        for selector in sidebar_selectors:
            try:
                elements = await page.locator(selector).count()
                if elements > 0:
                    print(f"📍 Sidebar encontrada: {selector}")
                    
                    # Capturar screenshot da sidebar
                    await page.screenshot(path=f"{screenshots_dir}/menu_02_sidebar_found.png")
                    
                    # Procurar pelo segundo item dentro da sidebar
                    sidebar_items = await page.locator(f"{selector} a, {selector} button, {selector} div[onclick], {selector} li").count()
                    print(f"📋 Itens encontrados na sidebar: {sidebar_items}")
                    
                    if sidebar_items >= 2:
                        print("🎯 Tentando clicar no segundo item...")
                        try:
                            # Tentar clicar no segundo item (índice 1)
                            await page.locator(f"{selector} a, {selector} button, {selector} div[onclick], {selector} li").nth(1).click()
                            await page.wait_for_timeout(3000)
                            await page.screenshot(path=f"{screenshots_dir}/menu_03_second_item_clicked.png")
                            sidebar_found = True
                            break
                        except Exception as e:
                            print(f"❌ Erro ao clicar no segundo item: {e}")
                            continue
                    
            except Exception as e:
                continue
        
        # Estratégia 2: Se não encontrou, procurar por texto específico "OS" ou "operação"
        if not sidebar_found:
            print("🔍 Estratégia 2: Procurando por texto 'OS' ou 'operação'...")
            
            # Procurar por elementos que contenham texto relacionado a OS
            menu_patterns = [
                "//a[contains(text(), 'OS')]",
                "//a[contains(text(), 'operação')]",
                "//a[contains(text(), 'Controle')]",
                "//button[contains(text(), 'OS')]",
                "//div[contains(text(), 'OS')]",
                "//li[contains(text(), 'OS')]",
                "//*[@title='OS']",
                "//*[@aria-label='OS']",
                "//a[contains(@href, 'os')]",
                "//a[contains(@href, 'operacao')]"
            ]
            
            for pattern in menu_patterns:
                try:
                    elements = await page.locator(pattern).count()
                    if elements > 0:
                        print(f"📍 Menu pattern encontrado: {pattern}")
                        await page.locator(pattern).click()
                        await page.wait_for_timeout(3000)
                        await page.screenshot(path=f"{screenshots_dir}/menu_03_pattern_clicked.png")
                        sidebar_found = True
                        break
                except Exception as e:
                    continue
        
        # Estratégia 3: Procurar no menu lateral esquerdo (posição específica)
        if not sidebar_found:
            print("🔍 Estratégia 3: Análise de posição no menu lateral...")
            
            # Obter elementos especificamente do menu lateral esquerdo
            elements_info = await page.evaluate("""
                () => {
                    const elements = [];
                    const clickable = ['a', 'button', 'div[onclick]', 'li', '[role="button"]'];
                    
                    clickable.forEach(selector => {
                        document.querySelectorAll(selector).forEach((el, index) => {
                            const rect = el.getBoundingClientRect();
                            const text = el.textContent?.trim() || '';
                            const classes = el.className || '';
                            
                            // Filtrar elementos do menu lateral esquerdo (baseado na imagem)
                            if (rect.left < 100 && rect.width > 15 && rect.height > 15 && rect.top > 50) {
                                elements.push({
                                    selector: selector,
                                    index: index,
                                    text: text,
                                    left: rect.left,
                                    top: rect.top,
                                    width: rect.width,
                                    height: rect.height,
                                    classes: classes,
                                    href: el.href || ''
                                });
                            }
                        });
                    });
                    
                    // Ordenar por posição vertical (top) - o segundo item será o índice 1
                    return elements.sort((a, b) => a.top - b.top);
                }
            """)
            
            print(f"📋 Elementos no lado esquerdo: {len(elements_info)}")
            
            # Tentar clicar no segundo elemento (se existir)
            if len(elements_info) >= 2:
                second_element = elements_info[1]
                print(f"🎯 Tentando clicar no segundo elemento: {second_element}")
                
                try:
                    # Várias tentativas de clicar no segundo elemento
                    click_attempts = [
                        f"{second_element['selector']}:nth-child({second_element['index'] + 1})",
                        f"{second_element['selector']}:nth-of-type(2)",
                        f"({second_element['selector']})[2]"
                    ]
                    
                    for attempt in click_attempts:
                        try:
                            await page.click(attempt)
                            await page.wait_for_timeout(3000)
                            await page.screenshot(path=f"{screenshots_dir}/menu_03_position_clicked.png")
                            
                            # Verificar se navegou para página de OS
                            current_url = page.url
                            if 'os' in current_url.lower() or 'operacao' in current_url.lower():
                                print(f"✅ Sucesso! Navegou para: {current_url}")
                                sidebar_found = True
                                break
                        except:
                            continue
                    
                    if not sidebar_found:
                        print("❌ Não conseguiu clicar no segundo elemento")
                        
                except Exception as e:
                    print(f"❌ Erro ao clicar por posição: {e}")
            
            # Tentar também o primeiro, terceiro e quarto elementos
            if not sidebar_found and len(elements_info) >= 4:
                print("🔍 Tentando outros elementos do menu...")
                for i in [0, 2, 3]:  # primeiro, terceiro, quarto
                    try:
                        element = elements_info[i]
                        print(f"🎯 Tentando elemento {i+1}: {element['text']}")
                        
                        await page.click(f"{element['selector']}:nth-child({element['index'] + 1})")
                        await page.wait_for_timeout(3000)
                        
                        current_url = page.url
                        if 'os' in current_url.lower() or 'operacao' in current_url.lower():
                            print(f"✅ Sucesso com elemento {i+1}!")
                            sidebar_found = True
                            break
                    except:
                        continue
        
        # Estratégia 4: Procurar especificamente por ícones ou imagens
        if not sidebar_found:
            print("🔍 Estratégia 4: Procurando por ícones...")
            
            # Procurar por SVGs, ícones, ou elementos que podem ser menu
            icon_selectors = [
                "svg:nth-child(2)",
                "i:nth-child(2)",
                ".icon:nth-child(2)",
                "[class*='icon']:nth-child(2)",
                "//svg[2]",
                "//i[2]",
                "//*[contains(@class, 'icon')][2]"
            ]
            
            for selector in icon_selectors:
                try:
                    if selector.startswith("//"):
                        elements = await page.locator(selector).count()
                    else:
                        elements = await page.locator(selector).count()
                    
                    if elements > 0:
                        print(f"📍 Ícone encontrado: {selector}")
                        if selector.startswith("//"):
                            await page.locator(selector).click()
                        else:
                            await page.locator(selector).click()
                        await page.wait_for_timeout(3000)
                        await page.screenshot(path=f"{screenshots_dir}/menu_03_icon_clicked.png")
                        sidebar_found = True
                        break
                except Exception as e:
                    continue
        
        # Screenshot final
        await page.screenshot(path=f"{screenshots_dir}/menu_04_final_result.png")
        
        # Verificar se conseguiu navegar
        final_url = page.url
        print(f"📍 URL final: {final_url}")
        
        if sidebar_found:
            print("✅ Navegação bem-sucedida!")
        else:
            print("❌ Não conseguiu encontrar o segundo item do menu")
        
        return {
            "success": sidebar_found,
            "final_url": final_url,
            "elements_found": len(elements_info) if 'elements_info' in locals() else 0
        }
        
    except Exception as e:
        print(f"❌ Erro no teste: {e}")
        await page.screenshot(path=f"{screenshots_dir}/menu_error.png")
        return {"error": str(e)}
    
    finally:
        await browser.close()
        await playwright.stop()

if __name__ == "__main__":
    result = asyncio.run(test_menu_navigation())
    print(json.dumps(result, indent=2))
'''
                
                # Executar código Python
                result = subprocess.run([
                    'python3', '-c', menu_test_code
                ], env=env, capture_output=True, text=True, timeout=300)
                
                logger.info(f"Teste de menu executado - Return code: {result.returncode}")
                logger.info(f"Stdout: {result.stdout}")
                if result.stderr:
                    logger.error(f"Stderr: {result.stderr}")
                    
            except Exception as e:
                logger.error(f"Erro ao executar teste de menu: {e}")
        
        # Executar em thread separada
        thread = threading.Thread(target=run_menu_test)
        thread.daemon = True
        thread.start()
        
        return jsonify({
            'status': 'success',
            'message': 'Teste de navegação do menu iniciado',
            'note': 'Aguarde alguns minutos. O teste tentará 4 estratégias diferentes para encontrar o segundo item do menu',
            'strategies': [
                '1. Procurar por sidebar/menu lateral',
                '2. Usar padrões XPath para segundo item',
                '3. Análise de posição dos elementos',
                '4. Procurar por ícones especificamente'
            ]
        })
        
    except Exception as e:
        logger.error(f"Erro ao iniciar teste de menu: {e}")
        return jsonify({
            'status': 'error',
            'message': f'Erro ao iniciar teste de menu: {e}'
        }), 500

@app.route('/test-bubble-structure', methods=['POST', 'GET'])
def test_bubble_structure():
    """Testa navegação específica para estrutura do Bubble.io"""
    try:
        import subprocess
        import threading
        
        def run_bubble_test():
            try:
                # Criar diretório de screenshots se não existir
                screenshots_dir = "/tmp/screenshots"
                os.makedirs(screenshots_dir, exist_ok=True)
                
                # Definir variáveis de ambiente
                env = os.environ.copy()
                env['EACE_USERNAME'] = 'raiseupbt@gmail.com'
                env['EACE_PASSWORD'] = '@Uujpgi8u'
                env['DISPLAY'] = ':99'
                
                # Código Python para teste específico do Bubble.io
                bubble_test_code = '''
import asyncio
import json
from playwright.async_api import async_playwright

async def test_bubble_navigation():
    screenshots_dir = "/tmp/screenshots"
    
    playwright = await async_playwright().start()
    browser = await playwright.chromium.launch(headless=True)
    page = await browser.new_page()
    
    try:
        # Fazer login primeiro
        print("🔐 Fazendo login...")
        await page.goto("https://eace.org.br/login?login=login")
        await page.wait_for_timeout(3000)
        
        await page.fill('//input[@placeholder="seuemail@email.com"]', "raiseupbt@gmail.com")
        await page.fill('//input[@type="password"]', "@Uujpgi8u")
        await page.click('//button[contains(text(), "Log In")]')
        await page.wait_for_timeout(5000)
        
        # Selecionar perfil se necessário
        if await page.locator('//*[contains(text(), "Fornecedor")]').count() > 0:
            await page.click('//*[contains(text(), "Fornecedor")]')
            await page.wait_for_timeout(5000)
        
        # Screenshot do dashboard
        await page.screenshot(path=f"{screenshots_dir}/bubble_01_dashboard.png")
        print("✅ Login realizado, procurando estrutura do Bubble.io...")
        
        # Estratégia 1: Procurar por "Gerenciar chamados" (baseado no inspect element)
        print("🔍 Estratégia 1: Procurando por 'Gerenciar chamados'...")
        
        gerenciar_selectors = [
            "//button[contains(text(), 'Gerenciar chamados')]",
            "//button[contains(text(), 'Gerenciar')]",
            "//button[contains(text(), 'chamados')]",
            "//div[contains(text(), 'Gerenciar chamados')]",
            "//*[contains(text(), 'Gerenciar chamados')]",
            "button[aria-label*='Gerenciar']",
            "button[title*='Gerenciar']"
        ]
        
        button_found = False
        for selector in gerenciar_selectors:
            try:
                if selector.startswith("//"):
                    elements = await page.locator(selector).count()
                else:
                    elements = await page.locator(selector).count()
                
                if elements > 0:
                    print(f"✅ Encontrado 'Gerenciar chamados': {selector}")
                    if selector.startswith("//"):
                        await page.locator(selector).click()
                    else:
                        await page.locator(selector).click()
                    await page.wait_for_timeout(3000)
                    await page.screenshot(path=f"{screenshots_dir}/bubble_02_gerenciar_clicked.png")
                    button_found = True
                    break
            except Exception as e:
                print(f"❌ Erro com {selector}: {e}")
                continue
        
        # Estratégia 2: Procurar por estrutura específica do Bubble.io
        if not button_found:
            print("🔍 Estratégia 2: Procurando estrutura específica do Bubble.io...")
            
            # Baseado na imagem: generic > button > SvgRoot
            bubble_selectors = [
                "div[class*='generic'] button",
                "div[data-element-type] button",
                "div[id*='generic'] button",
                "button[focusable='true']",
                "button[focusable]",
                "button:has(svg)",
                "button svg",
                "div[class*='bubble'] button"
            ]
            
            for selector in bubble_selectors:
                try:
                    elements = await page.locator(selector).count()
                    if elements > 0:
                        print(f"📍 Encontrado elementos Bubble: {elements} com {selector}")
                        
                        # Tentar clicar no segundo elemento (índice 1)
                        if elements >= 2:
                            await page.locator(selector).nth(1).click()
                            await page.wait_for_timeout(3000)
                            await page.screenshot(path=f"{screenshots_dir}/bubble_02_structure_clicked.png")
                            
                            # Verificar se navegou
                            current_url = page.url
                            if 'os' in current_url.lower() or 'chamados' in current_url.lower():
                                print(f"✅ Sucesso com estrutura! URL: {current_url}")
                                button_found = True
                                break
                        
                except Exception as e:
                    continue
        
        # Estratégia 3: Procurar por posição no menu lateral (focusable=true)
        if not button_found:
            print("🔍 Estratégia 3: Procurando por elementos focusable no menu lateral...")
            
            # Obter elementos focusable do lado esquerdo
            focusable_info = await page.evaluate("""
                () => {
                    const elements = [];
                    const focusableElements = document.querySelectorAll('button[focusable="true"], button[focusable], [focusable="true"]');
                    
                    focusableElements.forEach((el, index) => {
                        const rect = el.getBoundingClientRect();
                        const text = el.textContent?.trim() || '';
                        
                        // Filtrar elementos do menu lateral esquerdo
                        if (rect.left < 150 && rect.width > 10 && rect.height > 10 && rect.top > 50) {
                            elements.push({
                                index: index,
                                text: text,
                                left: rect.left,
                                top: rect.top,
                                width: rect.width,
                                height: rect.height,
                                classes: el.className,
                                id: el.id,
                                focusable: el.getAttribute('focusable'),
                                tagName: el.tagName
                            });
                        }
                    });
                    
                    return elements.sort((a, b) => a.top - b.top);
                }
            """)
            
            print(f"📋 Elementos focusable encontrados: {len(focusable_info)}")
            
            # Tentar clicar no segundo elemento focusable
            if len(focusable_info) >= 2:
                second_focusable = focusable_info[1]
                print(f"🎯 Tentando segundo elemento focusable: {second_focusable}")
                
                try:
                    # Clicar por posição
                    await page.click(f"button[focusable]:nth-child({second_focusable['index'] + 1})")
                    await page.wait_for_timeout(3000)
                    await page.screenshot(path=f"{screenshots_dir}/bubble_02_focusable_clicked.png")
                    
                    current_url = page.url
                    if 'os' in current_url.lower() or 'chamados' in current_url.lower():
                        print(f"✅ Sucesso com focusable! URL: {current_url}")
                        button_found = True
                        
                except Exception as e:
                    print(f"❌ Erro ao clicar focusable: {e}")
        
        # Estratégia 4: Força bruta - tentar todos os botões do menu lateral
        if not button_found:
            print("🔍 Estratégia 4: Força bruta - todos os botões do menu lateral...")
            
            all_buttons = await page.evaluate("""
                () => {
                    const buttons = [];
                    document.querySelectorAll('button').forEach((btn, index) => {
                        const rect = btn.getBoundingClientRect();
                        if (rect.left < 150 && rect.width > 10 && rect.height > 10 && rect.top > 50) {
                            buttons.push({
                                index: index,
                                text: btn.textContent?.trim() || '',
                                left: rect.left,
                                top: rect.top
                            });
                        }
                    });
                    return buttons.sort((a, b) => a.top - b.top);
                }
            """)
            
            print(f"📋 Todos os botões do menu: {len(all_buttons)}")
            
            # Tentar clicar em cada botão até encontrar o correto
            for i, button in enumerate(all_buttons):
                try:
                    print(f"🎯 Tentando botão {i+1}: {button['text']}")
                    await page.click(f"button:nth-child({button['index'] + 1})")
                    await page.wait_for_timeout(2000)
                    
                    current_url = page.url
                    if 'os' in current_url.lower() or 'chamados' in current_url.lower() or 'controle' in current_url.lower():
                        print(f"✅ SUCESSO! Botão {i+1} levou para: {current_url}")
                        await page.screenshot(path=f"{screenshots_dir}/bubble_02_success.png")
                        button_found = True
                        break
                        
                except Exception as e:
                    continue
        
        # Screenshot final
        await page.screenshot(path=f"{screenshots_dir}/bubble_03_final.png")
        
        final_url = page.url
        print(f"📍 URL final: {final_url}")
        
        if button_found:
            print("✅ NAVEGAÇÃO BEM-SUCEDIDA!")
        else:
            print("❌ Não conseguiu encontrar o botão correto")
        
        return {
            "success": button_found,
            "final_url": final_url,
            "focusable_elements": len(focusable_info) if 'focusable_info' in locals() else 0,
            "total_buttons": len(all_buttons) if 'all_buttons' in locals() else 0
        }
        
    except Exception as e:
        print(f"❌ Erro no teste: {e}")
        await page.screenshot(path=f"{screenshots_dir}/bubble_error.png")
        return {"error": str(e)}
    
    finally:
        await browser.close()
        await playwright.stop()

if __name__ == "__main__":
    result = asyncio.run(test_bubble_navigation())
    print(json.dumps(result, indent=2))
'''
                
                # Executar código Python
                result = subprocess.run([
                    'python3', '-c', bubble_test_code
                ], env=env, capture_output=True, text=True, timeout=300)
                
                logger.info(f"Teste Bubble executado - Return code: {result.returncode}")
                logger.info(f"Stdout: {result.stdout}")
                if result.stderr:
                    logger.error(f"Stderr: {result.stderr}")
                    
            except Exception as e:
                logger.error(f"Erro ao executar teste Bubble: {e}")
        
        # Executar em thread separada
        thread = threading.Thread(target=run_bubble_test)
        thread.daemon = True
        thread.start()
        
        return jsonify({
            'status': 'success',
            'message': 'Teste específico para Bubble.io iniciado',
            'note': 'Teste baseado na estrutura do inspect element: button "Gerenciar chamados" focusable=true',
            'strategies': [
                '1. Procurar por texto "Gerenciar chamados"',
                '2. Procurar por estrutura específica do Bubble.io',
                '3. Procurar por elementos focusable no menu lateral',
                '4. Força bruta - testar todos os botões do menu'
            ]
        })
        
    except Exception as e:
        logger.error(f"Erro ao iniciar teste Bubble: {e}")
        return jsonify({
            'status': 'error',
            'message': f'Erro ao iniciar teste Bubble: {e}'
        }), 500

@app.route('/test-direct-click', methods=['POST', 'GET'])
def test_direct_click():
    """Teste direto - força bruta em todos os botões do menu lateral"""
    try:
        import subprocess
        import threading
        
        def run_direct_test():
            try:
                # Criar diretório de screenshots se não existir
                screenshots_dir = "/tmp/screenshots"
                os.makedirs(screenshots_dir, exist_ok=True)
                
                # Definir variáveis de ambiente
                env = os.environ.copy()
                env['EACE_USERNAME'] = 'raiseupbt@gmail.com'
                env['EACE_PASSWORD'] = '@Uujpgi8u'
                env['DISPLAY'] = ':99'
                
                # Código Python para teste direto
                direct_test_code = '''
import asyncio
import json
from playwright.async_api import async_playwright

async def test_direct_navigation():
    screenshots_dir = "/tmp/screenshots"
    
    playwright = await async_playwright().start()
    browser = await playwright.chromium.launch(headless=True)
    page = await browser.new_page()
    
    try:
        # Fazer login
        print("🔐 Fazendo login...")
        await page.goto("https://eace.org.br/login?login=login")
        await page.wait_for_timeout(3000)
        
        await page.fill('//input[@placeholder="seuemail@email.com"]', "raiseupbt@gmail.com")
        await page.fill('//input[@type="password"]', "@Uujpgi8u")
        await page.click('//button[contains(text(), "Log In")]')
        await page.wait_for_timeout(5000)
        
        # Selecionar perfil se necessário
        if await page.locator('//*[contains(text(), "Fornecedor")]').count() > 0:
            await page.click('//*[contains(text(), "Fornecedor")]')
            await page.wait_for_timeout(5000)
        
        # Screenshot inicial
        await page.screenshot(path=f"{screenshots_dir}/direct_01_dashboard.png")
        print("✅ Login realizado!")
        
        # Obter TODOS os botões da página
        print("🔍 Mapeando TODOS os botões da página...")
        all_buttons = await page.evaluate("""
            () => {
                const buttons = [];
                document.querySelectorAll('button').forEach((btn, index) => {
                    const rect = btn.getBoundingClientRect();
                    const text = btn.textContent?.trim() || '';
                    const visible = rect.width > 0 && rect.height > 0 && btn.offsetParent !== null;
                    
                    if (visible) {
                        buttons.push({
                            index: index,
                            text: text,
                            left: rect.left,
                            top: rect.top,
                            width: rect.width,
                            height: rect.height,
                            classes: btn.className,
                            id: btn.id,
                            focusable: btn.getAttribute('focusable'),
                            innerHTML: btn.innerHTML.substring(0, 100)
                        });
                    }
                });
                return buttons;
            }
        """)
        
        print(f"📋 Total de botões encontrados: {len(all_buttons)}")
        
        # Salvar informações dos botões
        with open(f"{screenshots_dir}/buttons_info.json", "w") as f:
            json.dump(all_buttons, f, indent=2)
        
        # Tentar clicar em cada botão
        success_found = False
        initial_url = page.url
        
        for i, button in enumerate(all_buttons):
            try:
                print(f"🎯 Testando botão {i+1}/{len(all_buttons)}: '{button['text']}'")
                
                # Voltar para dashboard se mudou de página
                if page.url != initial_url:
                    await page.goto(initial_url)
                    await page.wait_for_timeout(2000)
                
                # Clicar no botão
                await page.click(f"button:nth-child({button['index'] + 1})")
                await page.wait_for_timeout(3000)
                
                # Verificar se mudou de página
                current_url = page.url
                if current_url != initial_url:
                    print(f"📍 Botão {i+1} mudou URL para: {current_url}")
                    await page.screenshot(path=f"{screenshots_dir}/direct_02_button_{i+1}_clicked.png")
                    
                    # Verificar se é a página que queremos
                    if any(keyword in current_url.lower() for keyword in ['os', 'chamados', 'operacao', 'controle']):
                        print(f"✅ SUCESSO! Botão {i+1} levou para página de OS!")
                        print(f"   Texto: '{button['text']}'")
                        print(f"   URL: {current_url}")
                        await page.screenshot(path=f"{screenshots_dir}/direct_03_SUCCESS.png")
                        success_found = True
                        break
                    else:
                        print(f"   ❌ Não é a página de OS")
                
                # Limite de tentativas para não travar
                if i >= 20:  # Testar apenas os primeiros 20 botões
                    print("⚠️ Limite de 20 botões atingido")
                    break
                    
            except Exception as e:
                print(f"❌ Erro no botão {i+1}: {e}")
                continue
        
        # Screenshot final
        await page.screenshot(path=f"{screenshots_dir}/direct_04_final.png")
        
        print(f"📍 URL final: {page.url}")
        if success_found:
            print("✅ ENCONTROU A PÁGINA DE OS!")
        else:
            print("❌ Não encontrou a página de OS")
        
        return {
            "success": success_found,
            "final_url": page.url,
            "total_buttons_tested": min(len(all_buttons), 20),
            "all_buttons_count": len(all_buttons)
        }
        
    except Exception as e:
        print(f"❌ Erro geral: {e}")
        await page.screenshot(path=f"{screenshots_dir}/direct_error.png")
        return {"error": str(e)}
    
    finally:
        await browser.close()
        await playwright.stop()

if __name__ == "__main__":
    result = asyncio.run(test_direct_navigation())
    print(json.dumps(result, indent=2))
'''
                
                # Executar código Python
                result = subprocess.run([
                    'python3', '-c', direct_test_code
                ], env=env, capture_output=True, text=True, timeout=300)
                
                logger.info(f"Teste direto executado - Return code: {result.returncode}")
                logger.info(f"Stdout: {result.stdout}")
                if result.stderr:
                    logger.error(f"Stderr: {result.stderr}")
                    
            except Exception as e:
                logger.error(f"Erro ao executar teste direto: {e}")
        
        # Executar em thread separada
        thread = threading.Thread(target=run_direct_test)
        thread.daemon = True
        thread.start()
        
        return jsonify({
            'status': 'success',
            'message': 'Teste direto iniciado - força bruta em todos os botões',
            'note': 'Este teste clica em cada botão da página até encontrar o que leva para OS',
            'info': 'Gerará screenshots de cada botão clicado e salvará informações em buttons_info.json'
        })
        
    except Exception as e:
        logger.error(f"Erro ao iniciar teste direto: {e}")
        return jsonify({
            'status': 'error',
            'message': f'Erro ao iniciar teste direto: {e}'
        }), 500

@app.route('/test-smart-menu', methods=['POST', 'GET'])
def test_smart_menu():
    """Teste inteligente - foca apenas no menu lateral esquerdo e evita links externos"""
    try:
        import subprocess
        import threading
        
        def run_smart_test():
            try:
                # Criar diretório de screenshots se não existir
                screenshots_dir = "/tmp/screenshots"
                os.makedirs(screenshots_dir, exist_ok=True)
                
                # Definir variáveis de ambiente
                env = os.environ.copy()
                env['EACE_USERNAME'] = 'raiseupbt@gmail.com'
                env['EACE_PASSWORD'] = '@Uujpgi8u'
                env['DISPLAY'] = ':99'
                
                # Código Python para teste inteligente
                smart_test_code = '''
import asyncio
import json
from playwright.async_api import async_playwright

async def test_smart_navigation():
    screenshots_dir = "/tmp/screenshots"
    
    playwright = await async_playwright().start()
    browser = await playwright.chromium.launch(headless=True)
    page = await browser.new_page()
    
    try:
        # Fazer login
        print("🔐 Fazendo login...")
        await page.goto("https://eace.org.br/login?login=login")
        await page.wait_for_timeout(3000)
        
        await page.fill('//input[@placeholder="seuemail@email.com"]', "raiseupbt@gmail.com")
        await page.fill('//input[@type="password"]', "@Uujpgi8u")
        await page.click('//button[contains(text(), "Log In")]')
        await page.wait_for_timeout(5000)
        
        # Selecionar perfil se necessário
        if await page.locator('//*[contains(text(), "Fornecedor")]').count() > 0:
            await page.click('//*[contains(text(), "Fornecedor")]')
            await page.wait_for_timeout(5000)
        
        # Screenshot inicial
        await page.screenshot(path=f"{screenshots_dir}/smart_01_dashboard.png")
        print("✅ Login realizado!")
        
        # Obter apenas botões do menu lateral esquerdo (evitando links externos)
        print("🔍 Mapeando botões do menu lateral...")
        menu_buttons = await page.evaluate("""
            () => {
                const buttons = [];
                const domain = window.location.hostname;
                
                document.querySelectorAll('button').forEach((btn, index) => {
                    const rect = btn.getBoundingClientRect();
                    const text = btn.textContent?.trim() || '';
                    const visible = rect.width > 0 && rect.height > 0 && btn.offsetParent !== null;
                    
                    // Filtrar apenas botões do menu lateral esquerdo
                    if (visible && rect.left < 200 && rect.top > 50) {
                        // Evitar botões que parecem ser links externos
                        const isExternal = text.toLowerCase().includes('intranet') || 
                                         text.toLowerCase().includes('portal') ||
                                         text.toLowerCase().includes('site') ||
                                         text.toLowerCase().includes('www') ||
                                         text.toLowerCase().includes('http');
                        
                        if (!isExternal) {
                            buttons.push({
                                index: index,
                                text: text,
                                left: rect.left,
                                top: rect.top,
                                width: rect.width,
                                height: rect.height,
                                classes: btn.className,
                                id: btn.id,
                                focusable: btn.getAttribute('focusable'),
                                innerHTML: btn.innerHTML.substring(0, 100)
                            });
                        }
                    }
                });
                
                // Ordenar por posição vertical (menu de cima para baixo)
                return buttons.sort((a, b) => a.top - b.top);
            }
        """)
        
        print(f"📋 Botões do menu lateral encontrados: {len(menu_buttons)}")
        
        # Salvar informações dos botões
        with open(f"{screenshots_dir}/menu_buttons_info.json", "w") as f:
            json.dump(menu_buttons, f, indent=2)
        
        # Tentar clicar em cada botão do menu
        success_found = False
        initial_url = page.url
        
        for i, button in enumerate(menu_buttons):
            try:
                print(f"🎯 Testando botão {i+1}/{len(menu_buttons)}: '{button['text']}'")
                
                # Garantir que estamos na página inicial
                if page.url != initial_url:
                    print(f"   🔄 Voltando para dashboard...")
                    await page.goto(initial_url)
                    await page.wait_for_timeout(3000)
                
                # Screenshot antes do clique
                await page.screenshot(path=f"{screenshots_dir}/smart_02_before_button_{i+1}.png")
                
                # Clicar no botão usando diferentes métodos
                click_success = False
                
                # Método 1: Clicar por seletor
                try:
                    await page.click(f"button:nth-child({button['index'] + 1})")
                    click_success = True
                except:
                    pass
                
                # Método 2: Clicar por posição (se o primeiro falhar)
                if not click_success:
                    try:
                        await page.click(f"button", position={"x": button['width']//2, "y": button['height']//2})
                        click_success = True
                    except:
                        pass
                
                # Método 3: Clicar por texto (se os outros falharem)
                if not click_success and button['text']:
                    try:
                        await page.click(f"text='{button['text']}'")
                        click_success = True
                    except:
                        pass
                
                if not click_success:
                    print(f"   ❌ Não conseguiu clicar no botão {i+1}")
                    continue
                
                # Aguardar possível mudança de página
                await page.wait_for_timeout(4000)
                
                # Verificar se mudou de página
                current_url = page.url
                if current_url != initial_url:
                    print(f"   📍 Botão {i+1} mudou URL para: {current_url}")
                    await page.screenshot(path=f"{screenshots_dir}/smart_03_button_{i+1}_result.png")
                    
                    # Verificar se ainda está no domínio eace.org.br
                    if 'eace.org.br' in current_url:
                        # Verificar se é a página que queremos
                        if any(keyword in current_url.lower() for keyword in ['os', 'chamados', 'operacao', 'controle']):
                            print(f"   ✅ SUCESSO! Botão {i+1} levou para página de OS!")
                            print(f"   Texto: '{button['text']}'")
                            print(f"   URL: {current_url}")
                            await page.screenshot(path=f"{screenshots_dir}/smart_04_SUCCESS.png")
                            success_found = True
                            break
                        else:
                            print(f"   ℹ️  Mudou de página mas não é OS")
                    else:
                        print(f"   ⚠️  Saiu do domínio eace.org.br")
                else:
                    print(f"   ➡️  Não mudou de página")
                    
            except Exception as e:
                print(f"   ❌ Erro no botão {i+1}: {e}")
                continue
        
        # Screenshot final
        await page.screenshot(path=f"{screenshots_dir}/smart_05_final.png")
        
        print(f"📍 URL final: {page.url}")
        if success_found:
            print("✅ ENCONTROU A PÁGINA DE OS!")
        else:
            print("❌ Não encontrou a página de OS nos botões do menu lateral")
        
        return {
            "success": success_found,
            "final_url": page.url,
            "menu_buttons_tested": len(menu_buttons),
            "initial_url": initial_url
        }
        
    except Exception as e:
        print(f"❌ Erro geral: {e}")
        await page.screenshot(path=f"{screenshots_dir}/smart_error.png")
        return {"error": str(e)}
    
    finally:
        await browser.close()
        await playwright.stop()

if __name__ == "__main__":
    result = asyncio.run(test_smart_navigation())
    print(json.dumps(result, indent=2))
'''
                
                # Executar código Python
                result = subprocess.run([
                    'python3', '-c', smart_test_code
                ], env=env, capture_output=True, text=True, timeout=300)
                
                logger.info(f"Teste inteligente executado - Return code: {result.returncode}")
                logger.info(f"Stdout: {result.stdout}")
                if result.stderr:
                    logger.error(f"Stderr: {result.stderr}")
                    
            except Exception as e:
                logger.error(f"Erro ao executar teste inteligente: {e}")
        
        # Executar em thread separada
        thread = threading.Thread(target=run_smart_test)
        thread.daemon = True
        thread.start()
        
        return jsonify({
            'status': 'success',
            'message': 'Teste inteligente iniciado - foco no menu lateral e evita links externos',
            'note': 'Filtra apenas botões do menu lateral esquerdo e evita "intranet", "portal", etc.',
            'features': [
                'Foca apenas no menu lateral esquerdo (left < 200px)',
                'Evita botões com texto "intranet", "portal", "site", etc.',
                'Sempre volta para dashboard se mudar de página',
                'Verifica se continua no domínio eace.org.br',
                'Múltiplos métodos de clique como fallback'
            ]
        })
        
    except Exception as e:
        logger.error(f"Erro ao iniciar teste inteligente: {e}")
        return jsonify({
            'status': 'error',
            'message': f'Erro ao iniciar teste inteligente: {e}'
        }), 500

@app.route('/test-expandable-menu', methods=['GET', 'POST'])
def test_expandable_menu():
    """Teste para navegação de menu expansível - foco em dois passos: expandir + clicar"""
    try:
        def run_expandable_test():
            try:
                # Configurar ambiente
                env = os.environ.copy()
                env['DISPLAY'] = ':99'
                
                # Código para teste de menu expansível
                expandable_test_code = '''
import asyncio
import json
from playwright.async_api import async_playwright
import os

async def test_expandable_menu():
    """Teste de menu expansível com dois passos: expandir menu + clicar item"""
    
    # Configurar diretório de screenshots
    screenshots_dir = "/tmp/screenshots"
    os.makedirs(screenshots_dir, exist_ok=True)
    
    playwright = await async_playwright().start()
    
    try:
        # Configurar browser
        browser = await playwright.chromium.launch(
            headless=True,
            args=['--no-sandbox', '--disable-dev-shm-usage']
        )
        
        page = await browser.new_page()
        
        print("🚀 Iniciando teste de menu expansível...")
        
        # Fazer login
        await page.goto("https://eace.org.br/login?login=login")
        await page.wait_for_timeout(3000)
        
        await page.fill('//input[@placeholder="seuemail@email.com"]', "raiseupbt@gmail.com")
        await page.fill('//input[@type="password"]', "@Uujpgi8u")
        await page.click('//button[contains(text(), "Log In")]')
        await page.wait_for_timeout(5000)
        
        # Selecionar perfil se necessário
        if await page.locator('//*[contains(text(), "Fornecedor")]').count() > 0:
            await page.click('//*[contains(text(), "Fornecedor")]')
            await page.wait_for_timeout(5000)
        
        await page.screenshot(path=f"{screenshots_dir}/expandable_01_dashboard.png")
        
        # FASE 1: Expandir o menu (hambúrguer)
        print("🔍 FASE 1: Procurando e expandindo o menu...")
        
        menu_expanded = False
        
        # Seletores para botão de menu hambúrguer
        menu_toggle_selectors = [
            "button[class*='menu']",
            "button[class*='hamburger']", 
            "button[class*='toggle']",
            "button[aria-label*='menu']",
            "button[focusable='true']",
            "//button[contains(@class, 'menu')]",
            "//button[@focusable='true']",
            "//button[contains(@aria-label, 'menu')]",
            "//button[1]",  # Primeiro botão da página
            "//div[contains(@class, 'generic')]//button[1]"
        ]
        
        for selector in menu_toggle_selectors:
            try:
                if selector.startswith("//"):
                    elements = await page.locator(selector).count()
                else:
                    elements = await page.locator(selector).count()
                
                if elements > 0:
                    print(f"📍 Tentando expandir menu com: {selector}")
                    
                    if selector.startswith("//"):
                        await page.locator(selector).click()
                    else:
                        await page.locator(selector).click()
                    
                    await page.wait_for_timeout(2000)
                    await page.screenshot(path=f"{screenshots_dir}/expandable_02_menu_expanded.png")
                    
                    # Verificar se menu foi expandido (procurar por mais elementos visíveis)
                    visible_elements = await page.evaluate("""
                        () => {
                            const elements = document.querySelectorAll('a, button, [role="button"]');
                            return Array.from(elements).filter(el => {
                                const rect = el.getBoundingClientRect();
                                return rect.width > 0 && rect.height > 0;
                            }).length;
                        }
                    """)
                    
                    print(f"🔍 Elementos visíveis após clique: {visible_elements}")
                    
                    # Assumir que menu foi expandido se há mais elementos visíveis
                    if visible_elements > 10:  # Threshold arbitrário
                        menu_expanded = True
                        break
                        
            except Exception as e:
                print(f"❌ Erro ao expandir menu com {selector}: {e}")
                continue
        
        if not menu_expanded:
            print("❌ Não conseguiu expandir o menu")
            await page.screenshot(path=f"{screenshots_dir}/expandable_02_menu_not_expanded.png")
        
        # FASE 2: Procurar e clicar no item do menu relacionado a OS
        print("🔍 FASE 2: Procurando item 'Gerenciar chamados' ou similar...")
        
        os_found = False
        
        # Primeiro, procurar especificamente por "Gerenciar chamados" (baseado na imagem)
        specific_selectors = [
            "//button[contains(text(), 'Gerenciar chamados')]",
            "//a[contains(text(), 'Gerenciar chamados')]",
            "//div[contains(text(), 'Gerenciar chamados')]",
            "//*[contains(text(), 'Gerenciar chamados')]",
            "//button[contains(text(), 'chamados')]",
            "//a[contains(text(), 'chamados')]",
            "//*[contains(text(), 'chamados')]"
        ]
        
        for selector in specific_selectors:
            try:
                elements = await page.locator(selector).count()
                if elements > 0:
                    print(f"📍 Encontrado 'Gerenciar chamados': {selector}")
                    await page.locator(selector).click()
                    await page.wait_for_timeout(3000)
                    await page.screenshot(path=f"{screenshots_dir}/expandable_03_chamados_clicked.png")
                    
                    # Verificar se navegou para página de OS/chamados
                    current_url = page.url
                    if 'os' in current_url.lower() or 'chamados' in current_url.lower() or 'controle' in current_url.lower():
                        print(f"✅ SUCESSO! Navegou para: {current_url}")
                        os_found = True
                        break
                        
            except Exception as e:
                print(f"❌ Erro ao clicar em {selector}: {e}")
                continue
        
        # Se não encontrou "Gerenciar chamados", procurar por outros termos
        if not os_found:
            print("🔍 Procurando por termos alternativos...")
            
            alternative_selectors = [
                "//*[contains(text(), 'OS')]",
                "//*[contains(text(), 'Operação')]",
                "//*[contains(text(), 'Controle')]",
                "//*[contains(text(), 'Tickets')]",
                "//*[contains(text(), 'Atendimento')]",
                "//button[contains(@class, 'generic')]",
                "//a[contains(@href, 'os')]",
                "//a[contains(@href, 'chamados')]",
                "//a[contains(@href, 'controle')]"
            ]
            
            for selector in alternative_selectors:
                try:
                    elements = await page.locator(selector).count()
                    if elements > 0:
                        print(f"📍 Tentando alternativa: {selector}")
                        await page.locator(selector).click()
                        await page.wait_for_timeout(3000)
                        await page.screenshot(path=f"{screenshots_dir}/expandable_04_alternative_clicked.png")
                        
                        current_url = page.url
                        if 'os' in current_url.lower() or 'chamados' in current_url.lower() or 'controle' in current_url.lower():
                            print(f"✅ SUCESSO com alternativa! URL: {current_url}")
                            os_found = True
                            break
                            
                except Exception as e:
                    print(f"❌ Erro com alternativa {selector}: {e}")
                    continue
        
        # FASE 3: Análise estrutural do menu expandido
        if not os_found:
            print("🔍 FASE 3: Analisando estrutura do menu expandido...")
            
            # Mapear todos os elementos do menu expandido
            menu_elements = await page.evaluate("""
                () => {
                    const elements = [];
                    const selectors = ['button', 'a', '[role="button"]', 'div[onclick]'];
                    
                    selectors.forEach(selector => {
                        document.querySelectorAll(selector).forEach((el, index) => {
                            const rect = el.getBoundingClientRect();
                            const text = el.textContent?.trim() || '';
                            
                            // Focar no menu lateral esquerdo
                            if (rect.left < 200 && rect.width > 10 && rect.height > 10 && text.length > 0) {
                                elements.push({
                                    tagName: el.tagName.toLowerCase(),
                                    text: text,
                                    classes: el.className,
                                    href: el.href || '',
                                    left: rect.left,
                                    top: rect.top,
                                    index: index
                                });
                            }
                        });
                    });
                    
                    return elements.sort((a, b) => a.top - b.top);
                }
            """)
            
            print(f"📋 Elementos encontrados no menu: {len(menu_elements)}")
            
            # Procurar pelo segundo elemento (baseado no feedback do usuário)
            if len(menu_elements) >= 2:
                target_element = menu_elements[1]  # Segundo elemento (índice 1)
                print(f"🎯 Tentando segundo elemento: {target_element}")
                
                try:
                    # Tentar clicar no elemento por texto
                    if target_element['text']:
                        await page.click(f"text='{target_element['text']}'")
                        await page.wait_for_timeout(3000)
                        await page.screenshot(path=f"{screenshots_dir}/expandable_05_second_element.png")
                        
                        current_url = page.url
                        if 'os' in current_url.lower() or 'chamados' in current_url.lower() or 'controle' in current_url.lower():
                            print(f"✅ SUCESSO com segundo elemento! URL: {current_url}")
                            os_found = True
                            
                except Exception as e:
                    print(f"❌ Erro ao clicar no segundo elemento: {e}")
        
        # Screenshot final
        await page.screenshot(path=f"{screenshots_dir}/expandable_06_final.png")
        
        final_url = page.url
        print(f"📍 URL final: {final_url}")
        
        if os_found:
            print("✅ Teste de menu expansível CONCLUÍDO COM SUCESSO!")
        else:
            print("❌ Não conseguiu navegar para página de OS/chamados")
        
        return {
            "success": os_found,
            "final_url": final_url,
            "menu_expanded": menu_expanded,
            "elements_found": len(menu_elements) if 'menu_elements' in locals() else 0
        }
        
    except Exception as e:
        print(f"❌ Erro no teste expansível: {e}")
        await page.screenshot(path=f"{screenshots_dir}/expandable_error.png")
        return {"error": str(e)}
    
    finally:
        await browser.close()
        await playwright.stop()

if __name__ == "__main__":
    result = asyncio.run(test_expandable_menu())
    print(json.dumps(result, indent=2))
'''
                
                # Executar código Python
                result = subprocess.run([
                    'python3', '-c', expandable_test_code
                ], env=env, capture_output=True, text=True, timeout=300)
                
                logger.info(f"Teste expansível executado - Return code: {result.returncode}")
                logger.info(f"Stdout: {result.stdout}")
                if result.stderr:
                    logger.error(f"Stderr: {result.stderr}")
                    
            except Exception as e:
                logger.error(f"Erro ao executar teste expansível: {e}")
        
        # Executar em thread separada
        thread = threading.Thread(target=run_expandable_test)
        thread.daemon = True
        thread.start()
        
        return jsonify({
            'status': 'success',
            'message': 'Teste de menu expansível iniciado - abordagem em duas fases',
            'note': 'Fase 1: Expandir menu hambúrguer + Fase 2: Clicar em "Gerenciar chamados"',
            'phases': [
                'Fase 1: Identifica e clica no botão do menu hambúrguer',
                'Fase 2: Procura por "Gerenciar chamados" no menu expandido',
                'Fase 3: Se não encontrar, analisa estrutura e tenta segundo elemento',
                'Foco específico no menu lateral esquerdo (left < 200px)',
                'Baseado na imagem do inspect element fornecida'
            ]
        })
        
    except Exception as e:
        logger.error(f"Erro ao iniciar teste expansível: {e}")
        return jsonify({
            'status': 'error',
            'message': f'Erro ao iniciar teste expansível: {e}'
        }), 500

@app.route('/test-os-page-mapping', methods=['GET', 'POST'])
def test_os_page_mapping():
    """Mapeia a página 'Controle de OS' e procura pelo botão 'Adicionar nova OS'"""
    try:
        def run_os_mapping_test():
            try:
                # Configurar ambiente
                env = os.environ.copy()
                env['DISPLAY'] = ':99'
                
                # Código para mapear página de OS
                os_mapping_code = '''
import asyncio
import json
from playwright.async_api import async_playwright
import os
from datetime import datetime

async def map_os_page():
    """Mapeia a página de Controle de OS e procura pelo botão Adicionar nova OS"""
    
    # Configurar diretório de screenshots
    screenshots_dir = "/tmp/screenshots"
    os.makedirs(screenshots_dir, exist_ok=True)
    
    playwright = await async_playwright().start()
    
    try:
        # Configurar browser
        browser = await playwright.chromium.launch(
            headless=True,
            args=['--no-sandbox', '--disable-dev-shm-usage']
        )
        
        page = await browser.new_page()
        
        print("🚀 Iniciando mapeamento da página de Controle de OS...")
        
        # ETAPA 1: Fazer login e navegar até página de OS
        print("🔐 Fazendo login...")
        await page.goto("https://eace.org.br/login?login=login")
        await page.wait_for_timeout(3000)
        
        await page.fill('//input[@placeholder="seuemail@email.com"]', "raiseupbt@gmail.com")
        await page.fill('//input[@type="password"]', "@Uujpgi8u")
        await page.click('//button[contains(text(), "Log In")]')
        await page.wait_for_timeout(5000)
        
        # Selecionar perfil se necessário
        if await page.locator('//*[contains(text(), "Fornecedor")]').count() > 0:
            await page.click('//*[contains(text(), "Fornecedor")]')
            await page.wait_for_timeout(5000)
        
        await page.screenshot(path=f"{screenshots_dir}/os_map_01_dashboard.png")
        
        # ETAPA 2: Navegar para página de Controle de OS (usando método que já funciona)
        print("🔍 Navegando para página de Controle de OS...")
        
        # Expandir menu hambúrguer
        menu_expanded = False
        menu_selectors = [
            "button[focusable='true']",
            "//button[@focusable='true']",
            "//button[1]",
            "//div[contains(@class, 'generic')]//button[1]"
        ]
        
        for selector in menu_selectors:
            try:
                if selector.startswith("//"):
                    elements = await page.locator(selector).count()
                else:
                    elements = await page.locator(selector).count()
                
                if elements > 0:
                    print(f"📍 Expandindo menu com: {selector}")
                    if selector.startswith("//"):
                        await page.locator(selector).click()
                    else:
                        await page.locator(selector).click()
                    await page.wait_for_timeout(2000)
                    menu_expanded = True
                    break
            except Exception as e:
                continue
        
        if not menu_expanded:
            print("❌ Não conseguiu expandir o menu")
            return {"error": "Menu não expandido"}
        
        await page.screenshot(path=f"{screenshots_dir}/os_map_02_menu_expanded.png")
        
        # Procurar por "Gerenciar chamados"
        chamados_selectors = [
            "//button[contains(text(), 'Gerenciar chamados')]",
            "//a[contains(text(), 'Gerenciar chamados')]",
            "//*[contains(text(), 'Gerenciar chamados')]"
        ]
        
        os_page_reached = False
        for selector in chamados_selectors:
            try:
                elements = await page.locator(selector).count()
                if elements > 0:
                    print(f"✅ Clicando em 'Gerenciar chamados': {selector}")
                    await page.locator(selector).click()
                    await page.wait_for_timeout(5000)
                    os_page_reached = True
                    break
            except Exception as e:
                continue
        
        if not os_page_reached:
            print("❌ Não conseguiu chegar na página de OS")
            return {"error": "Página de OS não alcançada"}
        
        await page.screenshot(path=f"{screenshots_dir}/os_map_03_os_page_reached.png")
        
        # ETAPA 3: Mapear a página de Controle de OS
        print("🔍 Mapeando página de Controle de OS...")
        
        current_url = page.url
        print(f"📍 URL atual: {current_url}")
        
        # Analisar todos os elementos da página
        page_elements = await page.evaluate("""
            () => {
                const elements = [];
                const selectors = ['button', 'a', 'input', 'div', 'span', 'h1', 'h2', 'h3', 'p'];
                
                selectors.forEach(selector => {
                    document.querySelectorAll(selector).forEach((el, index) => {
                        const rect = el.getBoundingClientRect();
                        const text = el.textContent?.trim() || '';
                        const visible = rect.width > 0 && rect.height > 0 && el.offsetParent !== null;
                        
                        if (visible && text.length > 0) {
                            elements.push({
                                tagName: el.tagName.toLowerCase(),
                                text: text,
                                classes: el.className || '',
                                id: el.id || '',
                                type: el.type || '',
                                href: el.href || '',
                                onclick: el.onclick ? 'true' : 'false',
                                left: rect.left,
                                top: rect.top,
                                width: rect.width,
                                height: rect.height,
                                focusable: el.getAttribute('focusable') || '',
                                ariaLabel: el.getAttribute('aria-label') || '',
                                title: el.getAttribute('title') || ''
                            });
                        }
                    });
                });
                
                return elements;
            }
        """)
        
        print(f"📋 Total de elementos encontrados: {len(page_elements)}")
        
        # ETAPA 4: Procurar especificamente pelo botão "Adicionar nova OS"
        print("🔍 Procurando pelo botão 'Adicionar nova OS'...")
        
        adicionar_os_buttons = []
        for element in page_elements:
            text_lower = element['text'].lower()
            if ('adicionar' in text_lower and 'os' in text_lower) or \
               ('nova' in text_lower and 'os' in text_lower) or \
               ('criar' in text_lower and 'os' in text_lower) or \
               ('novo' in text_lower and 'os' in text_lower):
                adicionar_os_buttons.append(element)
        
        print(f"🎯 Botões relacionados a 'Adicionar OS' encontrados: {len(adicionar_os_buttons)}")
        
        # Salvar análise completa
        analysis_data = {
            'url': current_url,
            'timestamp': datetime.now().isoformat(),
            'total_elements': len(page_elements),
            'adicionar_os_buttons': adicionar_os_buttons,
            'all_buttons': [el for el in page_elements if el['tagName'] == 'button'],
            'all_links': [el for el in page_elements if el['tagName'] == 'a'],
            'form_elements': [el for el in page_elements if el['tagName'] in ['input', 'textarea', 'select']]
        }
        
        with open(f"{screenshots_dir}/os_page_analysis.json", "w") as f:
            json.dump(analysis_data, f, indent=2)
        
        # ETAPA 5: Tentar clicar no botão "Adicionar nova OS" se encontrado
        button_clicked = False
        if adicionar_os_buttons:
            target_button = adicionar_os_buttons[0]  # Primeiro botão encontrado
            print(f"🎯 Tentando clicar no botão: {target_button['text']}")
            
            try:
                # Tentar diferentes métodos para clicar
                click_methods = [
                    f"text='{target_button['text']}'",
                    f"button:has-text('{target_button['text'][:20]}')",
                    f"//button[contains(text(), '{target_button['text'][:20]}')]"
                ]
                
                for method in click_methods:
                    try:
                        if method.startswith("//"):
                            await page.locator(method).click()
                        else:
                            await page.click(method)
                        await page.wait_for_timeout(3000)
                        button_clicked = True
                        print(f"✅ Clique realizado com método: {method}")
                        break
                    except Exception as e:
                        continue
                
                if button_clicked:
                    await page.screenshot(path=f"{screenshots_dir}/os_map_04_button_clicked.png")
                    
                    # Verificar se navegou para formulário
                    new_url = page.url
                    if new_url != current_url:
                        print(f"✅ Navegou para nova página: {new_url}")
                        
                        # Mapear formulário rapidamente
                        await page.wait_for_timeout(3000)
                        form_elements = await page.evaluate("""
                            () => {
                                const inputs = [];
                                document.querySelectorAll('input, textarea, select').forEach(el => {
                                    const rect = el.getBoundingClientRect();
                                    if (rect.width > 0 && rect.height > 0) {
                                        inputs.push({
                                            tagName: el.tagName.toLowerCase(),
                                            type: el.type || '',
                                            name: el.name || '',
                                            id: el.id || '',
                                            placeholder: el.placeholder || '',
                                            required: el.required || false,
                                            classes: el.className || ''
                                        });
                                    }
                                });
                                return inputs;
                            }
                        """)
                        
                        await page.screenshot(path=f"{screenshots_dir}/os_map_05_form_page.png")
                        
                        analysis_data['form_reached'] = True
                        analysis_data['form_url'] = new_url
                        analysis_data['form_elements_detailed'] = form_elements
                        
                        with open(f"{screenshots_dir}/os_page_analysis.json", "w") as f:
                            json.dump(analysis_data, f, indent=2)
                        
                        print(f"✅ Formulário mapeado com {len(form_elements)} campos")
                    else:
                        print("ℹ️ Permaneceu na mesma página após clique")
                        
            except Exception as e:
                print(f"❌ Erro ao clicar no botão: {e}")
        
        # Screenshot final
        await page.screenshot(path=f"{screenshots_dir}/os_map_06_final.png")
        
        # Resultado final
        result = {
            'success': True,
            'current_url': page.url,
            'os_buttons_found': len(adicionar_os_buttons),
            'button_clicked': button_clicked,
            'form_reached': analysis_data.get('form_reached', False),
            'total_elements_analyzed': len(page_elements)
        }
        
        if adicionar_os_buttons:
            result['target_button'] = adicionar_os_buttons[0]
        
        print(f"✅ Mapeamento concluído: {result}")
        return result
        
    except Exception as e:
        print(f"❌ Erro no mapeamento: {e}")
        await page.screenshot(path=f"{screenshots_dir}/os_map_error.png")
        return {"error": str(e)}
    
    finally:
        await browser.close()
        await playwright.stop()

if __name__ == "__main__":
    result = asyncio.run(map_os_page())
    print(json.dumps(result, indent=2))
'''
                
                # Executar código Python
                result = subprocess.run([
                    'python3', '-c', os_mapping_code
                ], env=env, capture_output=True, text=True, timeout=300)
                
                logger.info(f"Mapeamento de OS executado - Return code: {result.returncode}")
                logger.info(f"Stdout: {result.stdout}")
                if result.stderr:
                    logger.error(f"Stderr: {result.stderr}")
                    
            except Exception as e:
                logger.error(f"Erro ao executar mapeamento de OS: {e}")
        
        # Executar em thread separada
        thread = threading.Thread(target=run_os_mapping_test)
        thread.daemon = True
        thread.start()
        
        return jsonify({
            'status': 'success',
            'message': 'Mapeamento da página de OS iniciado',
            'note': 'Mapeia a página "Controle de OS" e procura pelo botão "Adicionar nova OS"',
            'objectives': [
                '1. Navegar para página de Controle de OS',
                '2. Mapear todos os elementos da página',
                '3. Encontrar botão "Adicionar nova OS"', 
                '4. Tentar clicar no botão',
                '5. Mapear formulário se alcançado',
                '6. Salvar análise completa em JSON'
            ],
            'outputs': [
                'Screenshots do processo completo',
                'Arquivo os_page_analysis.json com análise detalhada',
                'Mapeamento de elementos do formulário (se encontrado)'
            ]
        })
        
    except Exception as e:
        logger.error(f"Erro ao iniciar mapeamento de OS: {e}")
        return jsonify({
            'status': 'error',
            'message': f'Erro ao iniciar mapeamento de OS: {e}'
        }), 500

@app.route('/test-simple', methods=['GET'])
def test_simple():
    """Endpoint simples para teste"""
    return jsonify({
        'message': 'Endpoint funcionando!',
        'timestamp': datetime.now().isoformat(),
        'status': 'OK'
    })

@app.route('/debug-os-mapping', methods=['GET', 'POST'])
def debug_os_mapping():
    """Debug do mapeamento de OS com logs detalhados"""
    try:
        def run_debug_test():
            try:
                # Configurar ambiente
                env = os.environ.copy()
                env['DISPLAY'] = ':99'
                
                # Código simplificado para debug
                debug_code = '''
import asyncio
import json
from playwright.async_api import async_playwright
import os
from datetime import datetime

async def debug_os_mapping():
    """Debug do mapeamento de OS com logs detalhados"""
    
    screenshots_dir = "/tmp/screenshots"
    os.makedirs(screenshots_dir, exist_ok=True)
    
    # Log detalhado
    log_file = f"{screenshots_dir}/debug_log.txt"
    
    def log_message(message):
        print(message)
        with open(log_file, "a") as f:
            f.write(f"{datetime.now()}: {message}\\n")
    
    playwright = await async_playwright().start()
    
    try:
        log_message("🚀 Iniciando debug do mapeamento...")
        
        # Configurar browser
        browser = await playwright.chromium.launch(
            headless=True,
            args=['--no-sandbox', '--disable-dev-shm-usage']
        )
        
        page = await browser.new_page()
        log_message("✅ Browser iniciado")
        
        # ETAPA 1: Login
        log_message("🔐 Iniciando login...")
        await page.goto("https://eace.org.br/login?login=login")
        await page.wait_for_timeout(3000)
        log_message("✅ Página de login carregada")
        
        await page.fill('//input[@placeholder="seuemail@email.com"]', "raiseupbt@gmail.com")
        await page.fill('//input[@type="password"]', "@Uujpgi8u")
        log_message("✅ Credenciais preenchidas")
        
        await page.click('//button[contains(text(), "Log In")]')
        await page.wait_for_timeout(5000)
        log_message("✅ Login realizado")
        
        # Screenshot 1
        await page.screenshot(path=f"{screenshots_dir}/debug_01_login.png")
        log_message("📸 Screenshot 1 - Login")
        
        # ETAPA 2: Seleção de perfil
        log_message("👤 Verificando seleção de perfil...")
        if await page.locator('//*[contains(text(), "Fornecedor")]').count() > 0:
            await page.click('//*[contains(text(), "Fornecedor")]')
            await page.wait_for_timeout(5000)
            log_message("✅ Perfil Fornecedor selecionado")
        else:
            log_message("ℹ️ Perfil já selecionado ou não necessário")
        
        # Screenshot 2
        await page.screenshot(path=f"{screenshots_dir}/debug_02_perfil.png")
        log_message("📸 Screenshot 2 - Perfil")
        
        # ETAPA 3: Expandir menu
        log_message("🔍 Tentando expandir menu...")
        menu_expanded = False
        
        menu_selectors = [
            "button[focusable='true']",
            "//button[@focusable='true']",
            "//button[1]"
        ]
        
        for i, selector in enumerate(menu_selectors):
            try:
                log_message(f"🔍 Tentando seletor {i+1}: {selector}")
                
                if selector.startswith("//"):
                    elements = await page.locator(selector).count()
                else:
                    elements = await page.locator(selector).count()
                
                log_message(f"📊 Elementos encontrados: {elements}")
                
                if elements > 0:
                    log_message(f"✅ Clicando com seletor: {selector}")
                    if selector.startswith("//"):
                        await page.locator(selector).click()
                    else:
                        await page.locator(selector).click()
                    await page.wait_for_timeout(2000)
                    menu_expanded = True
                    log_message("✅ Menu expandido com sucesso")
                    break
                else:
                    log_message(f"❌ Nenhum elemento encontrado com: {selector}")
                    
            except Exception as e:
                log_message(f"❌ Erro com seletor {selector}: {e}")
                continue
        
        # Screenshot 3
        await page.screenshot(path=f"{screenshots_dir}/debug_03_menu.png")
        log_message("📸 Screenshot 3 - Menu")
        
        if not menu_expanded:
            log_message("❌ ERRO: Menu não foi expandido")
            return {"error": "Menu não expandido", "step": "menu_expansion"}
        
        # ETAPA 4: Procurar "Gerenciar chamados"
        log_message("🔍 Procurando 'Gerenciar chamados'...")
        
        chamados_selectors = [
            "//button[contains(text(), 'Gerenciar chamados')]",
            "//a[contains(text(), 'Gerenciar chamados')]",
            "//*[contains(text(), 'Gerenciar chamados')]",
            "//*[contains(text(), 'chamados')]"
        ]
        
        os_page_reached = False
        for i, selector in enumerate(chamados_selectors):
            try:
                log_message(f"🔍 Tentando seletor chamados {i+1}: {selector}")
                elements = await page.locator(selector).count()
                log_message(f"📊 Elementos 'chamados' encontrados: {elements}")
                
                if elements > 0:
                    log_message(f"✅ Clicando em 'Gerenciar chamados': {selector}")
                    await page.locator(selector).click()
                    await page.wait_for_timeout(5000)
                    os_page_reached = True
                    log_message("✅ Página de OS alcançada")
                    break
                else:
                    log_message(f"❌ Nenhum elemento 'chamados' encontrado com: {selector}")
                    
            except Exception as e:
                log_message(f"❌ Erro com seletor chamados {selector}: {e}")
                continue
        
        # Screenshot 4
        await page.screenshot(path=f"{screenshots_dir}/debug_04_os_page.png")
        log_message("📸 Screenshot 4 - Página OS")
        
        if not os_page_reached:
            log_message("❌ ERRO: Página de OS não foi alcançada")
            return {"error": "Página de OS não alcançada", "step": "os_navigation"}
        
        # ETAPA 5: Analisar página atual
        log_message("🔍 Analisando página atual...")
        current_url = page.url
        log_message(f"📍 URL atual: {current_url}")
        
        # Buscar botões relacionados a OS
        buttons_info = await page.evaluate("""
            () => {
                const buttons = [];
                document.querySelectorAll('button, a').forEach((el, index) => {
                    const rect = el.getBoundingClientRect();
                    const text = el.textContent?.trim() || '';
                    const visible = rect.width > 0 && rect.height > 0;
                    
                    if (visible && text.length > 0) {
                        buttons.push({
                            index: index,
                            text: text,
                            tagName: el.tagName.toLowerCase(),
                            classes: el.className || '',
                            id: el.id || ''
                        });
                    }
                });
                return buttons;
            }
        """)
        
        log_message(f"📊 Total de botões encontrados: {len(buttons_info)}")
        
        # Procurar botão "Adicionar nova OS"
        os_buttons = []
        for button in buttons_info:
            text_lower = button['text'].lower()
            if ('adicionar' in text_lower and 'os' in text_lower) or \
               ('nova' in text_lower and 'os' in text_lower) or \
               ('novo' in text_lower and 'os' in text_lower):
                os_buttons.append(button)
                log_message(f"🎯 Botão OS encontrado: {button['text']}")
        
        log_message(f"📊 Botões de OS encontrados: {len(os_buttons)}")
        
        # Screenshot 5
        await page.screenshot(path=f"{screenshots_dir}/debug_05_analysis.png")
        log_message("📸 Screenshot 5 - Análise")
        
        # Salvar dados completos
        debug_data = {
            'timestamp': datetime.now().isoformat(),
            'current_url': current_url,
            'menu_expanded': menu_expanded,
            'os_page_reached': os_page_reached,
            'total_buttons': len(buttons_info),
            'os_buttons_found': len(os_buttons),
            'os_buttons': os_buttons,
            'all_buttons': buttons_info[:10]  # Primeiros 10 para não sobrecarregar
        }
        
        with open(f"{screenshots_dir}/debug_analysis.json", "w") as f:
            json.dump(debug_data, f, indent=2)
        
        log_message("✅ Debug concluído com sucesso")
        
        return {
            'success': True,
            'current_url': current_url,
            'os_buttons_found': len(os_buttons),
            'total_buttons': len(buttons_info),
            'menu_expanded': menu_expanded,
            'os_page_reached': os_page_reached
        }
        
    except Exception as e:
        log_message(f"❌ ERRO GERAL: {e}")
        await page.screenshot(path=f"{screenshots_dir}/debug_error.png")
        return {"error": str(e), "step": "general_error"}
    
    finally:
        await browser.close()
        await playwright.stop()
        log_message("🔚 Browser fechado")

if __name__ == "__main__":
    result = asyncio.run(debug_os_mapping())
    print(json.dumps(result, indent=2))
'''
                
                # Executar código Python
                result = subprocess.run([
                    'python3', '-c', debug_code
                ], env=env, capture_output=True, text=True, timeout=300)
                
                logger.info(f"Debug executado - Return code: {result.returncode}")
                logger.info(f"Stdout: {result.stdout}")
                if result.stderr:
                    logger.error(f"Stderr: {result.stderr}")
                    
            except Exception as e:
                logger.error(f"Erro ao executar debug: {e}")
        
        # Executar em thread separada
        thread = threading.Thread(target=run_debug_test)
        thread.daemon = True
        thread.start()
        
        return jsonify({
            'status': 'success',
            'message': 'Debug do mapeamento de OS iniciado',
            'note': 'Versão com logs detalhados para identificar onde está falhando',
            'outputs': [
                'debug_log.txt - Log detalhado de cada etapa',
                'debug_analysis.json - Análise completa dos elementos',
                'Screenshots numerados de cada etapa',
                'Identificação do ponto de falha'
            ]
        })
        
    except Exception as e:
        logger.error(f"Erro ao iniciar debug: {e}")
        return jsonify({
            'status': 'error',
            'message': f'Erro ao iniciar debug: {e}'
        }), 500

@app.route('/map-adicionar-os-button', methods=['GET', 'POST'])
def map_adicionar_os_button():
    """Mapeia o botão 'Adicionar nova OS' usando navegação funcional do test-expandable-menu"""
    try:
        def run_os_button_mapping():
            try:
                # Configurar ambiente
                env = os.environ.copy()
                env['DISPLAY'] = ':99'
                
                # Código baseado no test-expandable-menu que funciona
                os_button_mapping_code = '''
import asyncio
import json
from playwright.async_api import async_playwright
import os
from datetime import datetime

async def map_adicionar_os_button():
    """Mapeia o botão 'Adicionar nova OS' na página de Controle de OS"""
    
    screenshots_dir = "/tmp/screenshots"
    os.makedirs(screenshots_dir, exist_ok=True)
    
    playwright = await async_playwright().start()
    
    try:
        # Configurar browser
        browser = await playwright.chromium.launch(
            headless=True,
            args=['--no-sandbox', '--disable-dev-shm-usage']
        )
        
        page = await browser.new_page()
        
        print("🚀 Mapeando botão 'Adicionar nova OS' - baseado no test-expandable-menu")
        
        # ETAPA 1: Login (idêntico ao test-expandable-menu)
        print("🔐 Fazendo login...")
        await page.goto("https://eace.org.br/login?login=login")
        await page.wait_for_timeout(3000)
        
        await page.fill('//input[@placeholder="seuemail@email.com"]', "raiseupbt@gmail.com")
        await page.fill('//input[@type="password"]', "@Uujpgi8u")
        await page.click('//button[contains(text(), "Log In")]')
        await page.wait_for_timeout(5000)
        
        # Selecionar perfil se necessário
        if await page.locator('//*[contains(text(), "Fornecedor")]').count() > 0:
            await page.click('//*[contains(text(), "Fornecedor")]')
            await page.wait_for_timeout(5000)
        
        await page.screenshot(path=f"{screenshots_dir}/os_btn_01_dashboard.png")
        
        # ETAPA 2: Expandir menu (usando método que funciona)
        print("🔍 Expandindo menu hambúrguer...")
        
        menu_expanded = False
        menu_selectors = [
            "button[focusable='true']",
            "//button[@focusable='true']",
            "//button[1]",
            "//div[contains(@class, 'generic')]//button[1]"
        ]
        
        for selector in menu_selectors:
            try:
                if selector.startswith("//"):
                    elements = await page.locator(selector).count()
                else:
                    elements = await page.locator(selector).count()
                
                if elements > 0:
                    print(f"📍 Expandindo menu com: {selector}")
                    if selector.startswith("//"):
                        await page.locator(selector).click()
                    else:
                        await page.locator(selector).click()
                    await page.wait_for_timeout(2000)
                    menu_expanded = True
                    break
            except Exception as e:
                continue
        
        if not menu_expanded:
            print("❌ Não conseguiu expandir o menu")
            return {"error": "Menu não expandido"}
        
        await page.screenshot(path=f"{screenshots_dir}/os_btn_02_menu_expanded.png")
        
        # ETAPA 3: Procurar e clicar em "Gerenciar chamados"
        print("🔍 Procurando 'Gerenciar chamados'...")
        
        chamados_selectors = [
            "//button[contains(text(), 'Gerenciar chamados')]",
            "//a[contains(text(), 'Gerenciar chamados')]",
            "//*[contains(text(), 'Gerenciar chamados')]"
        ]
        
        os_page_reached = False
        for selector in chamados_selectors:
            try:
                elements = await page.locator(selector).count()
                if elements > 0:
                    print(f"✅ Clicando em 'Gerenciar chamados': {selector}")
                    await page.locator(selector).click()
                    await page.wait_for_timeout(5000)
                    os_page_reached = True
                    break
            except Exception as e:
                continue
        
        if not os_page_reached:
            print("❌ Não conseguiu chegar na página de OS")
            return {"error": "Página de OS não alcançada"}
        
        # ETAPA 4: Análise estrutural do menu (método que funciona)
        print("🔍 Analisando estrutura do menu expandido...")
        
        menu_elements = await page.evaluate("""
            () => {
                const elements = [];
                const selectors = ['button', 'a', '[role="button"]', 'div[onclick]'];
                
                selectors.forEach(selector => {
                    document.querySelectorAll(selector).forEach((el, index) => {
                        const rect = el.getBoundingClientRect();
                        const text = el.textContent?.trim() || '';
                        
                        // Focar no menu lateral esquerdo
                        if (rect.left < 200 && rect.width > 10 && rect.height > 10 && text.length > 0) {
                            elements.push({
                                tagName: el.tagName.toLowerCase(),
                                text: text,
                                classes: el.className,
                                href: el.href || '',
                                left: rect.left,
                                top: rect.top,
                                index: index
                            });
                        }
                    });
                });
                
                return elements.sort((a, b) => a.top - b.top);
            }
        """)
        
        print(f"📋 Elementos encontrados no menu: {len(menu_elements)}")
        
        # Clicar no segundo elemento (método que funciona)
        if len(menu_elements) >= 2:
            target_element = menu_elements[1]  # Segundo elemento (índice 1)
            print(f"🎯 Clicando no segundo elemento: {target_element}")
            
            try:
                if target_element['text']:
                    await page.click(f"text='{target_element['text']}'")
                    await page.wait_for_timeout(3000)
                    
                    current_url = page.url
                    if 'os' in current_url.lower() or 'chamados' in current_url.lower() or 'controle' in current_url.lower():
                        print(f"✅ Sucesso! Chegou na página de OS: {current_url}")
                        os_page_reached = True
                    else:
                        print(f"❌ URL não parece ser de OS: {current_url}")
                        return {"error": "URL não reconhecida como página de OS"}
                        
            except Exception as e:
                print(f"❌ Erro ao clicar no segundo elemento: {e}")
                return {"error": f"Erro ao clicar: {e}"}
        
        await page.screenshot(path=f"{screenshots_dir}/os_btn_03_os_page.png")
        
        # ETAPA 5: MAPEAR PÁGINA DE CONTROLE DE OS
        print("🔍 Mapeando página de Controle de OS...")
        
        current_url = page.url
        print(f"📍 URL da página de OS: {current_url}")
        
        # Mapear todos os elementos da página
        page_elements = await page.evaluate("""
            () => {
                const elements = [];
                const selectors = ['button', 'a', 'div', 'span', 'input'];
                
                selectors.forEach(selector => {
                    document.querySelectorAll(selector).forEach((el, index) => {
                        const rect = el.getBoundingClientRect();
                        const text = el.textContent?.trim() || '';
                        const visible = rect.width > 0 && rect.height > 0 && el.offsetParent !== null;
                        
                        if (visible && text.length > 0) {
                            elements.push({
                                tagName: el.tagName.toLowerCase(),
                                text: text,
                                classes: el.className || '',
                                id: el.id || '',
                                type: el.type || '',
                                href: el.href || '',
                                left: rect.left,
                                top: rect.top,
                                width: rect.width,
                                height: rect.height,
                                focusable: el.getAttribute('focusable') || '',
                                onclick: el.onclick ? 'true' : 'false'
                            });
                        }
                    });
                });
                
                return elements;
            }
        """)
        
        print(f"📊 Total de elementos na página: {len(page_elements)}")
        
        # ETAPA 6: PROCURAR ESPECIFICAMENTE PELO BOTÃO "ADICIONAR NOVA OS"
        print("🎯 Procurando botão 'Adicionar nova OS'...")
        
        adicionar_os_buttons = []
        for element in page_elements:
            text_lower = element['text'].lower()
            if ('adicionar' in text_lower and ('os' in text_lower or 'nova' in text_lower)) or \
               ('nova' in text_lower and 'os' in text_lower) or \
               ('criar' in text_lower and 'os' in text_lower) or \
               ('novo' in text_lower and 'os' in text_lower) or \
               ('adicionar nova' in text_lower):
                adicionar_os_buttons.append(element)
                print(f"🎯 Botão encontrado: '{element['text']}' - {element['tagName']}")
        
        print(f"📊 Botões 'Adicionar OS' encontrados: {len(adicionar_os_buttons)}")
        
        # ETAPA 7: TENTAR CLICAR NO BOTÃO SE ENCONTRADO
        button_clicked = False
        form_reached = False
        
        if adicionar_os_buttons:
            target_button = adicionar_os_buttons[0]
            print(f"🎯 Tentando clicar no botão: '{target_button['text']}'")
            
            try:
                # Diferentes métodos para clicar
                click_methods = [
                    f"text='{target_button['text']}'",
                    f"button:has-text('{target_button['text']}')",
                    f"//button[contains(text(), '{target_button['text'][:15]}')]",
                    f"//*[contains(text(), '{target_button['text'][:15]}')]"
                ]
                
                for method in click_methods:
                    try:
                        print(f"🔍 Tentando método: {method}")
                        if method.startswith("//"):
                            await page.locator(method).click()
                        else:
                            await page.click(method)
                        await page.wait_for_timeout(3000)
                        button_clicked = True
                        print(f"✅ Clique realizado com: {method}")
                        break
                    except Exception as e:
                        print(f"❌ Falha com método {method}: {e}")
                        continue
                
                if button_clicked:
                    await page.screenshot(path=f"{screenshots_dir}/os_btn_04_button_clicked.png")
                    
                    # Verificar se chegou no formulário
                    new_url = page.url
                    if new_url != current_url:
                        print(f"✅ Navegou para nova página: {new_url}")
                        form_reached = True
                        
                        # Aguardar carregamento do formulário
                        await page.wait_for_timeout(3000)
                        
                        # Mapear campos do formulário
                        form_fields = await page.evaluate("""
                            () => {
                                const fields = [];
                                document.querySelectorAll('input, textarea, select').forEach(el => {
                                    const rect = el.getBoundingClientRect();
                                    if (rect.width > 0 && rect.height > 0) {
                                        fields.push({
                                            tagName: el.tagName.toLowerCase(),
                                            type: el.type || '',
                                            name: el.name || '',
                                            id: el.id || '',
                                            placeholder: el.placeholder || '',
                                            required: el.required || false,
                                            classes: el.className || '',
                                            value: el.value || ''
                                        });
                                    }
                                });
                                return fields;
                            }
                        """)
                        
                        await page.screenshot(path=f"{screenshots_dir}/os_btn_05_form_page.png")
                        print(f"✅ Formulário mapeado com {len(form_fields)} campos")
                        
                        # Salvar dados do formulário
                        form_data = {
                            'form_url': new_url,
                            'form_fields': form_fields,
                            'field_count': len(form_fields)
                        }
                        
                        with open(f"{screenshots_dir}/form_mapping.json", "w") as f:
                            json.dump(form_data, f, indent=2)
                    else:
                        print("ℹ️ Permaneceu na mesma página após clique")
                        
            except Exception as e:
                print(f"❌ Erro ao clicar no botão: {e}")
        else:
            print("❌ Nenhum botão 'Adicionar OS' encontrado")
        
        # Screenshot final
        await page.screenshot(path=f"{screenshots_dir}/os_btn_06_final.png")
        
        # Salvar análise completa
        analysis_data = {
            'timestamp': datetime.now().isoformat(),
            'current_url': current_url,
            'total_elements': len(page_elements),
            'adicionar_os_buttons': adicionar_os_buttons,
            'button_clicked': button_clicked,
            'form_reached': form_reached,
            'all_buttons': [el for el in page_elements if el['tagName'] == 'button'][:10],
            'success': button_clicked and form_reached
        }
        
        with open(f"{screenshots_dir}/os_button_analysis.json", "w") as f:
            json.dump(analysis_data, f, indent=2)
        
        result = {
            'success': button_clicked,
            'form_reached': form_reached,
            'current_url': page.url,
            'os_buttons_found': len(adicionar_os_buttons),
            'total_elements': len(page_elements),
            'target_button': adicionar_os_buttons[0] if adicionar_os_buttons else None
        }
        
        print(f"✅ Mapeamento concluído: {result}")
        return result
        
    except Exception as e:
        print(f"❌ Erro geral: {e}")
        await page.screenshot(path=f"{screenshots_dir}/os_btn_error.png")
        return {"error": str(e)}
    
    finally:
        await browser.close()
        await playwright.stop()

if __name__ == "__main__":
    result = asyncio.run(map_adicionar_os_button())
    print(json.dumps(result, indent=2))
'''
                
                # Executar código Python
                result = subprocess.run([
                    'python3', '-c', os_button_mapping_code
                ], env=env, capture_output=True, text=True, timeout=300)
                
                logger.info(f"Mapeamento botão OS executado - Return code: {result.returncode}")
                logger.info(f"Stdout: {result.stdout}")
                if result.stderr:
                    logger.error(f"Stderr: {result.stderr}")
                    
            except Exception as e:
                logger.error(f"Erro ao executar mapeamento botão OS: {e}")
        
        # Executar em thread separada
        thread = threading.Thread(target=run_os_button_mapping)
        thread.daemon = True
        thread.start()
        
        return jsonify({
            'status': 'success',
            'message': 'Mapeamento do botão "Adicionar nova OS" iniciado',
            'note': 'Baseado no test-expandable-menu que funciona 100%',
            'objectives': [
                '1. Usar navegação funcional do test-expandable-menu',
                '2. Chegar na página de Controle de OS',
                '3. Mapear todos os elementos da página',
                '4. Encontrar botão "Adicionar nova OS"',
                '5. Tentar clicar no botão',
                '6. Mapear formulário de criação se encontrado'
            ],
            'outputs': [
                'os_btn_01_dashboard.png até os_btn_06_final.png',
                'os_button_analysis.json - Análise completa',
                'form_mapping.json - Mapeamento do formulário (se encontrado)'
            ]
        })
        
    except Exception as e:
        logger.error(f"Erro ao iniciar mapeamento botão OS: {e}")
        return jsonify({
            'status': 'error',
            'message': f'Erro ao iniciar mapeamento botão OS: {e}'
        }), 500

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