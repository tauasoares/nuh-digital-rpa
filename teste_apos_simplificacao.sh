#!/bin/bash

echo "🧪 TESTE APÓS SIMPLIFICAÇÃO DAS DEPENDÊNCIAS"
echo "============================================"

URL="https://automacoes-rpa-eace-nuhdigital.6pwqgx.easypanel.host"

echo "⏰ $(date) - Testando: $URL"
echo ""

# Aguardar um pouco para dar tempo do rebuild
echo "⏰ Aguardando 30 segundos para rebuild..."
sleep 30

echo "🏥 HEALTH CHECK:"
curl -s -o /dev/null -w "Status: %{http_code} | Time: %{time_total}s\n" "$URL/status"

echo ""
echo "📋 RESPOSTA (primeiras 3 linhas):"
curl -s "$URL/status" | head -3

echo ""
echo "============================================"
echo "✅ Se status = 200, aplicação funcionando!"
echo "❌ Se status = 502, ainda há problemas"
echo "⏰ $(date) - Teste concluído"