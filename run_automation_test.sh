#!/bin/bash

echo "🚀 Executando teste de automação EACE..."
echo "📸 Os screenshots serão salvos em /tmp/screenshots"
echo ""

# Definir variáveis de ambiente
export EACE_USERNAME="raiseupbt@gmail.com"
export EACE_PASSWORD="@Uujpgi8u"
export DISPLAY=":99"

# Iniciar Xvfb se não estiver rodando
if ! pgrep -f "Xvfb :99" > /dev/null; then
    echo "🖥️ Iniciando Xvfb..."
    Xvfb :99 -screen 0 1024x768x24 &
    sleep 2
fi

# Executar teste
echo "🔍 Executando automação..."
python3 run_test_automation.py

echo ""
echo "✅ Teste concluído!"
echo "🌐 Acesse os screenshots em:"
echo "   - https://automacoes-rpa-eace-nuhdigital.6pwqgx.easypanel.host/screenshots/gallery"
echo "   - https://automacoes-rpa-eace-nuhdigital.6pwqgx.easypanel.host/screenshots"