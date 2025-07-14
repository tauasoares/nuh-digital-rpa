#!/usr/bin/env python3
"""
Script para executar teste de automação e gerar screenshots
"""

import asyncio
import os
import sys
from datetime import datetime
from loguru import logger
from eace_automation import EaceAutomation

async def run_automation_test():
    """Executa teste de automação com screenshots"""
    logger.info("🚀 Iniciando teste de automação EACE...")
    
    # Criar instância da automação
    automation = EaceAutomation()
    
    try:
        # Verificar se diretório de screenshots existe
        screenshots_dir = automation.screenshots_dir
        if not os.path.exists(screenshots_dir):
            os.makedirs(screenshots_dir, exist_ok=True)
            logger.info(f"📁 Diretório criado: {screenshots_dir}")
        
        # Inicializar browser
        logger.info("🌐 Inicializando navegador...")
        await automation.init_browser()
        
        # Executar login com screenshots
        logger.info("🔐 Iniciando processo de login...")
        login_success = await automation.login()
        
        if login_success:
            logger.success("✅ Login realizado com sucesso!")
            
            # Aguardar para garantir que página carregou
            await automation.page.wait_for_timeout(5000)
            
            # Screenshot final do dashboard
            await automation.take_screenshot("dashboard_complete", "Dashboard carregado - processo concluído")
            
            # Explorar elementos da página
            await automation.take_screenshot("page_elements", "Capturando elementos da página")
            
            # Verificar URL atual
            current_url = automation.page.url
            logger.info(f"📍 URL atual: {current_url}")
            
            # Listar screenshots criados
            screenshots = []
            if os.path.exists(screenshots_dir):
                screenshots = [f for f in os.listdir(screenshots_dir) if f.endswith('.png')]
                screenshots.sort()
            
            logger.info(f"📸 Screenshots gerados: {len(screenshots)}")
            for screenshot in screenshots:
                logger.info(f"   - {screenshot}")
            
            logger.info("🌐 Acesse os screenshots em:")
            logger.info("   - Lista JSON: https://automacoes-rpa-eace-nuhdigital.6pwqgx.easypanel.host/screenshots")
            logger.info("   - Galeria HTML: https://automacoes-rpa-eace-nuhdigital.6pwqgx.easypanel.host/screenshots/gallery")
            logger.info("   - Último screenshot: https://automacoes-rpa-eace-nuhdigital.6pwqgx.easypanel.host/screenshots/latest")
            
        else:
            logger.error("❌ Falha no login")
            
    except Exception as e:
        logger.error(f"❌ Erro durante teste: {e}")
        await automation.take_screenshot("error_state", f"Erro durante execução: {str(e)}")
        
    finally:
        # Fechar browser
        await automation.close()
        logger.info("🔚 Teste finalizado")

def main():
    """Função principal"""
    # Configurar logging
    logger.remove()  # Remove handler padrão
    logger.add(sys.stdout, format="{time:YYYY-MM-DD HH:mm:ss} | {level: <8} | {message}")
    logger.add("automation_test.log", rotation="1 day", retention="7 days", level="INFO")
    
    # Executar teste
    asyncio.run(run_automation_test())

if __name__ == "__main__":
    main()