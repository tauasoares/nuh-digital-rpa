#!/bin/bash

# Script para testar EasyPanel após correção
echo "🧪 TESTANDO EASYPANEL APÓS CORREÇÃO"
echo "====================================="

URL="https://automacoes-rpa-eace-nuhdigital.6pwqgx.easypanel.host"

echo "🔍 Testando aplicação: $URL"
echo ""

# Teste 1: Health Check
echo "1. 🏥 HEALTH CHECK"
curl -s -o /dev/null -w "Status: %{http_code}\n" "$URL/status"
echo ""

# Teste 2: Resposta com conteúdo
echo "2. 📋 RESPOSTA HEALTH CHECK"
curl -s "$URL/status" | head -5
echo ""

# Teste 3: Webhook Test
echo "3. 🎯 WEBHOOK TEST"
curl -s -X POST "$URL/webhook/test" \
  -H "Content-Type: application/json" \
  -d '{"ticket_id": 999, "test": true}' \
  -w "Status: %{http_code}\n"
echo ""

# Teste 4: Webhook EACE (simulação)
echo "4. 🤖 WEBHOOK EACE SIMULAÇÃO"
curl -s -X POST "$URL/webhook/eace" \
  -H "Content-Type: application/json" \
  -d '{
    "type": "INSERT",
    "table": "tickets",
    "record": {
      "id": 999,
      "descricao_enviada": "Teste webhook - Site: INEP - 31382221"
    }
  }' \
  -w "Status: %{http_code}\n"

echo ""
echo "====================================="
echo "✅ TESTES CONCLUÍDOS"
echo "📋 Se status = 200, aplicação está funcionando!"
echo "📋 Se status = 502, ainda há problema no build"