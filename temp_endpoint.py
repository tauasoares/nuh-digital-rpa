@app.route('/test-expandable-real-working', methods=['GET'])
def test_expandable_real_working():
    """Endpoint baseado EXATAMENTE no código que funciona + logs reais"""
    import threading
    import time
    import json
    from datetime import datetime
    
    # Sistema de logs em tempo real
    global_logs = []
    
    def add_real_log(message, level="info"):
        timestamp = datetime.now().strftime("%H:%M:%S")
        global_logs.append({
            "timestamp": timestamp,
            "message": message,
            "level": level
        })
        logger.info(f"[{timestamp}] {message}")
    
    def run_exact_working_code():
        """Executa o código EXATO do /test-expandable-menu que funciona"""
        try:
            add_real_log("🚀 Iniciando teste com código EXATO que funciona 100%", "success")
            
            # Configurar ambiente
            env = os.environ.copy()
            env['DISPLAY'] = ':99'
            
            # Código Python EXATO do endpoint que funciona
            working_code = '''
import asyncio
import json
import sys
from playwright.async_api import async_playwright
import os
from datetime import datetime

def log_real_action(message, level="info"):
    """Log com timestamp real"""
    timestamp = datetime.now().strftime("%H:%M:%S")
    print(f"[{timestamp}] [{level.upper()}] {message}")
    sys.stdout.flush()

async def run_exact_working_test():
    """Código EXATO do /test-expandable-menu que funciona"""
    
    # Configurar diretório de screenshots
    screenshots_dir = "/tmp/screenshots"
    os.makedirs(screenshots_dir, exist_ok=True)
    
    log_real_action("📁 Diretório de screenshots configurado", "info")
    
    playwright = await async_playwright().start()
    
    try:
        log_real_action("🌐 Iniciando navegador Chromium...", "info")
        
        # Configurar browser EXATO
        browser = await playwright.chromium.launch(
            headless=True,
            args=['--no-sandbox', '--disable-dev-shm-usage']
        )
        
        page = await browser.new_page()
        log_real_action("✅ Navegador iniciado com sucesso", "success")
        
        # ===================
        # FAZER LOGIN (CÓDIGO EXATO)
        # ===================
        log_real_action("🔐 Navegando para página de login...", "info")
        await page.goto("https://eace.org.br/login?login=login")
        await page.wait_for_timeout(3000)
        
        log_real_action("📝 Preenchendo credenciais...", "info")
        
        # Preencher email (seletor EXATO)
        email_selector = '//input[@placeholder="seuemail@email.com"]'
        await page.fill(email_selector, "raiseupbt@gmail.com")
        log_real_action(f"✅ Email preenchido usando: {email_selector}", "success")
        
        # Preencher senha (seletor EXATO)
        password_selector = '//input[@type="password"]'
        await page.fill(password_selector, "@Uujpgi8u")
        log_real_action(f"✅ Senha preenchida usando: {password_selector}", "success")
        
        # Clicar no botão de login (seletor EXATO)
        login_button_selector = '//button[contains(text(), "Log In")]'
        await page.click(login_button_selector)
        log_real_action(f"✅ Botão de login clicado: {login_button_selector}", "success")
        
        await page.wait_for_timeout(5000)
        
        # Selecionar perfil se necessário (código EXATO)
        profile_selector = '//*[contains(text(), "Fornecedor")]'
        profile_count = await page.locator(profile_selector).count()
        
        if profile_count > 0:
            await page.click(profile_selector)
            log_real_action(f"✅ Perfil Fornecedor selecionado: {profile_selector}", "success")
            await page.wait_for_timeout(5000)
        else:
            log_real_action("ℹ️ Seleção de perfil não necessária", "info")
        
        # Screenshot do dashboard (nome EXATO)
        dashboard_screenshot = f"{screenshots_dir}/working_01_dashboard.png"
        await page.screenshot(path=dashboard_screenshot)
        log_real_action(f"📸 Screenshot do dashboard: {dashboard_screenshot}", "success")
        
        # ===================
        # FASE 1: EXPANDIR MENU (CÓDIGO EXATO)
        # ===================
        log_real_action("🔍 FASE 1: Procurando e expandindo o menu hambúrguer...", "info")
        
        menu_expanded = False
        
        # Seletores EXATOS do código que funciona
        menu_toggle_selectors = [
            "button[class*='menu']",
            "button[class*='hamburger']", 
            "button[class*='toggle']",
            "button[aria-label*='menu']",
            "button[focusable='true']",
            "//button[contains(@class, 'menu')]",
            "//button[@focusable='true']",
            "//button[contains(@aria-label, 'menu')]",
            "//button[1]",
            "//div[contains(@class, 'generic')]//button[1]"
        ]
        
        for selector in menu_toggle_selectors:
            try:
                log_real_action(f"🔍 Testando seletor de menu: {selector}", "info")
                
                if selector.startswith("//"):
                    elements = await page.locator(selector).count()
                else:
                    elements = await page.locator(selector).count()
                
                log_real_action(f"📊 Elementos encontrados com {selector}: {elements}", "info")
                
                if elements > 0:
                    log_real_action(f"🎯 Clicando no menu com: {selector}", "info")
                    
                    if selector.startswith("//"):
                        await page.locator(selector).click()
                    else:
                        await page.locator(selector).click()
                    
                    await page.wait_for_timeout(2000)
                    
                    # Screenshot do menu expandido
                    menu_screenshot = f"{screenshots_dir}/working_02_menu_expanded.png"
                    await page.screenshot(path=menu_screenshot)
                    log_real_action(f"📸 Screenshot do menu expandido: {menu_screenshot}", "success")
                    
                    # Verificar se menu foi expandido (código EXATO)
                    visible_elements = await page.evaluate("""
                        () => {
                            const elements = document.querySelectorAll('a, button, [role="button"]');
                            return Array.from(elements).filter(el => {
                                const rect = el.getBoundingClientRect();
                                return rect.width > 0 && rect.height > 0;
                            }).length;
                        }
                    """)
                    
                    log_real_action(f"📊 Elementos visíveis após expansão: {visible_elements}", "info")
                    
                    if visible_elements > 10:  # Threshold EXATO
                        log_real_action(f"✅ Menu expandido com sucesso usando: {selector}", "success")
                        menu_expanded = True
                        break
                    else:
                        log_real_action(f"❌ Menu não expandiu suficientemente com: {selector}", "error")
                        
            except Exception as e:
                log_real_action(f"❌ Erro ao expandir menu com {selector}: {e}", "error")
                continue
        
        # ===================
        # FASE 2: PROCURAR "GERENCIAR CHAMADOS" (CÓDIGO EXATO)
        # ===================
        log_real_action("🔍 FASE 2: Procurando item 'Gerenciar chamados' ou similar...", "info")
        
        os_found = False
        
        # Seletores EXATOS do código que funciona
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
                log_real_action(f"🔍 Testando seletor para chamados: {selector}", "info")
                
                elements = await page.locator(selector).count()
                log_real_action(f"📊 Elementos encontrados com {selector}: {elements}", "info")
                
                if elements > 0:
                    log_real_action(f"✅ Encontrado 'Gerenciar chamados' com: {selector}", "success")
                    
                    # Obter o texto do elemento antes de clicar
                    element_text = await page.locator(selector).first.text_content()
                    log_real_action(f"📝 Texto do elemento: '{element_text}'", "info")
                    
                    await page.locator(selector).click()
                    await page.wait_for_timeout(3000)
                    
                    # Screenshot após clicar
                    chamados_screenshot = f"{screenshots_dir}/working_03_chamados_clicked.png"
                    await page.screenshot(path=chamados_screenshot)
                    log_real_action(f"📸 Screenshot após clicar: {chamados_screenshot}", "success")
                    
                    # Verificar se navegou para página de OS/chamados (código EXATO)
                    current_url = page.url
                    log_real_action(f"🌐 URL atual após clique: {current_url}", "info")
                    
                    if 'os' in current_url.lower() or 'chamados' in current_url.lower() or 'controle' in current_url.lower():
                        log_real_action(f"✅ SUCESSO! Navegou para página de OS: {current_url}", "success")
                        os_found = True
                        break
                    else:
                        log_real_action(f"❌ URL não corresponde a página de OS: {current_url}", "error")
                        
            except Exception as e:
                log_real_action(f"❌ Erro ao clicar em {selector}: {e}", "error")
                continue
        
        # ===================
        # FASE 3: ANÁLISE ESTRUTURAL (CÓDIGO EXATO)
        # ===================
        if not os_found:
            log_real_action("🔍 FASE 3: Analisando estrutura do menu expandido...", "info")
            
            # Mapear elementos (código EXATO)
            menu_elements = await page.evaluate("""
                () => {
                    const elements = [];
                    const selectors = ['button', 'a', '[role="button"]', 'div[onclick]'];
                    
                    selectors.forEach(selector => {
                        document.querySelectorAll(selector).forEach((el, index) => {
                            const rect = el.getBoundingClientRect();
                            const text = el.textContent?.trim() || '';
                            
                            // Focar no menu lateral esquerdo (código EXATO)
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
            
            log_real_action(f"📊 Elementos encontrados no menu lateral: {len(menu_elements)}", "info")
            
            # Log detalhado dos elementos encontrados
            for i, element in enumerate(menu_elements[:5]):  # Primeiros 5 elementos
                log_real_action(f"📋 Elemento {i+1}: '{element['text']}' ({element['tagName']}) - classes: {element['classes']}", "info")
            
            # Procurar pelo segundo elemento (código EXATO)
            if len(menu_elements) >= 2:
                target_element = menu_elements[1]  # Segundo elemento (índice 1)
                log_real_action(f"🎯 Tentando segundo elemento: '{target_element['text']}' ({target_element['tagName']})", "info")
                
                try:
                    # Tentar clicar no elemento por texto (código EXATO)
                    if target_element['text']:
                        await page.click(f"text='{target_element['text']}'")
                        await page.wait_for_timeout(3000)
                        
                        # Screenshot do segundo elemento
                        second_screenshot = f"{screenshots_dir}/working_04_second_element.png"
                        await page.screenshot(path=second_screenshot)
                        log_real_action(f"📸 Screenshot do segundo elemento: {second_screenshot}", "success")
                        
                        current_url = page.url
                        log_real_action(f"🌐 URL após clicar no segundo elemento: {current_url}", "info")
                        
                        if 'os' in current_url.lower() or 'chamados' in current_url.lower() or 'controle' in current_url.lower():
                            log_real_action(f"✅ SUCESSO com segundo elemento! URL: {current_url}", "success")
                            os_found = True
                        else:
                            log_real_action(f"❌ Segundo elemento não levou à página de OS: {current_url}", "error")
                            
                except Exception as e:
                    log_real_action(f"❌ Erro ao clicar no segundo elemento: {e}", "error")
            else:
                log_real_action("❌ Menos de 2 elementos encontrados no menu", "error")
        
        # Screenshot final
        final_screenshot = f"{screenshots_dir}/working_05_final.png"
        await page.screenshot(path=final_screenshot)
        log_real_action(f"📸 Screenshot final: {final_screenshot}", "success")
        
        final_url = page.url
        log_real_action(f"🌐 URL final: {final_url}", "info")
        
        if os_found:
            log_real_action("🎉 TESTE CONCLUÍDO COM SUCESSO! Navegação para Controle de OS realizada!", "success")
        else:
            log_real_action("❌ TESTE FALHOU: Não conseguiu navegar para página de OS/chamados", "error")
        
        return {
            "success": os_found,
            "final_url": final_url,
            "menu_expanded": menu_expanded,
            "elements_found": len(menu_elements) if 'menu_elements' in locals() else 0
        }
        
    except Exception as e:
        log_real_action(f"❌ ERRO CRÍTICO no teste: {e}", "error")
        error_screenshot = f"{screenshots_dir}/working_error.png"
        await page.screenshot(path=error_screenshot)
        log_real_action(f"📸 Screenshot do erro: {error_screenshot}", "error")
        return {"error": str(e)}
    
    finally:
        log_real_action("🔄 Fechando navegador...", "info")
        await browser.close()
        await playwright.stop()
        log_real_action("✅ Navegador fechado com sucesso", "success")

if __name__ == "__main__":
    result = asyncio.run(run_exact_working_test())
    print(json.dumps(result, indent=2))
'''
            
            add_real_log("🔧 Executando código Python com Playwright...", "info")
            
            # Executar código Python
            result = subprocess.run([
                'python3', '-c', working_code
            ], env=env, capture_output=True, text=True, timeout=300)
            
            # Processar saída do código
            if result.stdout:
                for line in result.stdout.strip().split('\n'):
                    if line.strip():
                        add_real_log(f"📝 {line}", "info")
            
            if result.stderr:
                for line in result.stderr.strip().split('\n'):
                    if line.strip():
                        add_real_log(f"❌ {line}", "error")
            
            if result.returncode == 0:
                add_real_log("✅ Teste executado com sucesso!", "success")
            else:
                add_real_log(f"❌ Teste falhou com código: {result.returncode}", "error")
            
        except Exception as e:
            add_real_log(f"❌ Erro durante execução: {e}", "error")
    
    # Executar teste em thread separada
    thread = threading.Thread(target=run_exact_working_code)
    thread.daemon = True
    thread.start()
    
    # Aguardar um pouco para os logs iniciais
    time.sleep(2)
    
    # Gerar HTML com logs reais
    html_content = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Test Expandable Menu - Código Exato Que Funciona</title>
        <meta charset="UTF-8">
        <meta http-equiv="refresh" content="3">
        <style>
            body {{ font-family: Arial, sans-serif; margin: 20px; background: #f0f0f0; }}
            .container {{ max-width: 1400px; margin: 0 auto; background: white; padding: 20px; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }}
            .header {{ text-align: center; margin-bottom: 30px; }}
            .status {{ padding: 15px; margin: 10px 0; border-radius: 5px; font-weight: bold; }}
            .status-success {{ background: #d4edda; color: #155724; border: 1px solid #c3e6cb; }}
            .terminal {{ background: #000; color: #00ff00; padding: 20px; border-radius: 5px; font-family: 'Courier New', monospace; height: 500px; overflow-y: auto; border: 2px solid #333; }}
            .log-entry {{ margin: 3px 0; padding: 2px; }}
            .log-success {{ color: #00ff00; }}
            .log-error {{ color: #ff0000; }}
            .log-info {{ color: #ffff00; }}
            .screenshots {{ margin: 30px 0; }}
            .screenshot {{ margin: 15px; display: inline-block; vertical-align: top; }}
            .screenshot img {{ max-width: 280px; border: 2px solid #ddd; border-radius: 5px; box-shadow: 0 2px 5px rgba(0,0,0,0.1); }}
            .screenshot h4 {{ text-align: center; margin: 10px 0; color: #333; }}
            .refresh-btn {{ background: #007bff; color: white; padding: 10px 20px; border: none; border-radius: 5px; cursor: pointer; margin: 10px 0; }}
            .refresh-btn:hover {{ background: #0056b3; }}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>🔧 Test Expandable Menu - Código Exato Que Funciona</h1>
                <p>Baseado no código EXATO do /test-expandable-menu que funciona 100%</p>
                <button class="refresh-btn" onclick="location.reload()">🔄 Atualizar Logs</button>
            </div>
            
            <div class="status status-success">
                ✅ Usando o código EXATO do endpoint que funciona<br>
                🎯 Navegação: Login → Perfil → Menu Hambúrguer → Gerenciar Chamados → Controle de OS<br>
                🔄 Página atualiza automaticamente a cada 3 segundos
            </div>
            
            <div class="terminal" id="terminal">
                <div class="log-entry log-success">[LOG SYSTEM] Logs reais do código EXATO em execução:</div>
    """
    
    # Adicionar logs reais
    for log_entry in global_logs:
        level_class = f"log-{log_entry['level']}"
        html_content += f'<div class="log-entry {level_class}">[{log_entry["timestamp"]}] {log_entry["message"]}</div>\n'
    
    html_content += f"""
            </div>
            
            <div class="screenshots">
                <h2>📸 Screenshots em Tempo Real:</h2>
                <div class="screenshot">
                    <h4>Dashboard</h4>
                    <img src="/screenshot/working_01_dashboard.png" alt="Dashboard">
                </div>
                <div class="screenshot">
                    <h4>Menu Expandido</h4>
                    <img src="/screenshot/working_02_menu_expanded.png" alt="Menu Expandido">
                </div>
                <div class="screenshot">
                    <h4>Chamados Clicado</h4>
                    <img src="/screenshot/working_03_chamados_clicked.png" alt="Chamados">
                </div>
                <div class="screenshot">
                    <h4>Segundo Elemento</h4>
                    <img src="/screenshot/working_04_second_element.png" alt="Segundo Elemento">
                </div>
                <div class="screenshot">
                    <h4>Controle de OS (Final)</h4>
                    <img src="/screenshot/working_05_final.png" alt="Final">
                </div>
            </div>
            
            <div class="status status-success">
                🌐 <strong>Galeria completa:</strong> <a href="/screenshots/gallery" target="_blank">Ver todos os screenshots</a><br>
                📋 <strong>Lista JSON:</strong> <a href="/screenshots" target="_blank">Ver JSON</a>
            </div>
        </div>
    </body>
    </html>
    """
    
    return html_content