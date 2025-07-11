# 🔧 **DIAGNÓSTICO EASYPANEL - ERRO 502**

## 🚨 **PROBLEMA ATUAL**
- **URL:** https://automacoes-rpa-eace-nuhdigital.6pwqgx.easypanel.host/
- **Erro:** 502 Bad Gateway
- **Causa:** Container não está respondendo

## 🔍 **CHECKLIST DE DIAGNÓSTICO**

### **1. Verificar Logs no EasyPanel**
```
EasyPanel Dashboard → Services → automacoes-rpa-eace-nuhdigital → Logs
```

**Erros comuns:**
- ❌ `ModuleNotFoundError` - Dependências não instaladas
- ❌ `Chrome/ChromeDriver` - Problemas com navegador
- ❌ `Port 5000` - Porta não disponível
- ❌ `Environment variables` - Variáveis não configuradas

### **2. Verificar Variáveis de Ambiente**
```yaml
# No EasyPanel, verificar se estão configuradas:
SUPABASE_URL: https://seu-projeto.supabase.co
SUPABASE_KEY: sua_anon_key_aqui
EACE_USERNAME: seu_usuario_eace
EACE_PASSWORD: sua_senha_eace
WEBHOOK_URL: https://automacoes-rpa-eace-nuhdigital.6pwqgx.easypanel.host/webhook/eace
PORT: 5000
LOG_LEVEL: INFO
PYTHONUNBUFFERED: 1
```

### **3. Verificar Build**
```yaml
# No EasyPanel, verificar:
Build Method: Dockerfile
Build Path: .
Port: 5000
```

## 🛠️ **SOLUÇÕES POSSÍVEIS**

### **Solução 1: Rebuild da Aplicação**
```
1. EasyPanel → Services → automacoes-rpa-eace-nuhdigital
2. Clique em "Rebuild"
3. Aguarde build completar
4. Verificar logs novamente
```

### **Solução 2: Configurar Variáveis de Ambiente**
```
1. EasyPanel → Services → automacoes-rpa-eace-nuhdigital → Settings
2. Environment Variables → Add Variable
3. Adicionar todas as variáveis necessárias
4. Restart da aplicação
```

### **Solução 3: Verificar Dockerfile**
```dockerfile
# Nosso Dockerfile deve ter:
FROM python:3.11-slim
RUN apt-get update && apt-get install -y wget curl unzip gnupg
# ... instalação do Chrome
EXPOSE 5000
CMD ["python", "webhook_realtime.py"]
```

## 🧪 **TESTE LOCAL PRIMEIRO**

### **1. Rodar Localmente**
```bash
# No seu WSL
cd /mnt/c/Users/tauas/Documents/rpa_eace

# Instalar dependências
pip install -r requirements_webhook.txt

# Configurar .env
cp .env.example .env
# Editar .env com credenciais reais

# Rodar webhook
python webhook_realtime.py
```

### **2. Testar Endpoints**
```bash
# Health check
curl http://localhost:5000/status

# Teste webhook
curl -X POST http://localhost:5000/webhook/test \
  -H "Content-Type: application/json" \
  -d '{"ticket_id": 123}'
```

### **3. Script de Teste**
```bash
# Executar diagnóstico completo
python test_webhook_local.py
```

## 🔧 **CONFIGURAÇÃO CORRETA DO EASYPANEL**

### **Service Settings:**
```yaml
Name: automacoes-rpa-eace-nuhdigital
Type: App
Source: GitHub
Repository: tauasoares/nuh-digital-rpa
Branch: main
Auto Deploy: ON
```

### **Build Settings:**
```yaml
Build Method: Dockerfile
Build Path: .
Build Command: (deixar vazio)
Start Command: (deixar vazio - usa CMD do Dockerfile)
```

### **Network Settings:**
```yaml
Domain: automacoes-rpa-eace-nuhdigital.6pwqgx.easypanel.host
Port: 5000
```

## 📊 **MONITORAMENTO**

### **Verificar Status:**
```bash
# Aplicação online
curl -I https://automacoes-rpa-eace-nuhdigital.6pwqgx.easypanel.host/status

# Deve retornar 200 OK
```

### **Logs em Tempo Real:**
```
EasyPanel → Services → automacoes-rpa-eace-nuhdigital → Logs → Real-time
```

## 🎯 **PRÓXIMOS PASSOS**

1. **Verificar logs** no EasyPanel
2. **Configurar variáveis** de ambiente
3. **Fazer rebuild** se necessário
4. **Testar localmente** se problema persistir
5. **Verificar configuração** do GitHub repository

## 🏆 **QUANDO FUNCIONAR**

**Testes para fazer:**
```bash
# 1. Health check
curl https://automacoes-rpa-eace-nuhdigital.6pwqgx.easypanel.host/status

# 2. Webhook test
curl -X POST https://automacoes-rpa-eace-nuhdigital.6pwqgx.easypanel.host/webhook/test \
  -H "Content-Type: application/json" \
  -d '{"ticket_id": 123}'

# 3. Webhook EACE (simular ticket)
curl -X POST https://automacoes-rpa-eace-nuhdigital.6pwqgx.easypanel.host/webhook/eace \
  -H "Content-Type: application/json" \
  -d '{
    "type": "INSERT",
    "table": "tickets", 
    "record": {
      "id": 999,
      "descricao_enviada": "Teste - Site: INEP - 31382221"
    }
  }'
```

**Resultado esperado:**
- Status 200 OK
- Logs detalhados
- Resposta JSON válida