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
            'screenshots_gallery': '/screenshots/gallery',
            'run_test': '/run-test',
            'inspect_page': '/inspect-page',
            'test_menu_navigation': '/test-menu-navigation'
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