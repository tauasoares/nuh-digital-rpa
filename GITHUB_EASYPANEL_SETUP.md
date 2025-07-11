# 🚀 **SETUP GITHUB + EASYPANEL - DEPLOY AUTOMÁTICO**

## 🎯 **ESTRATÉGIA DE DEPLOY**

**EasyPanel suporta deploy direto do GitHub**, eliminando necessidade de upload manual de arquivos.

---

## 📋 **PASSO 1: CONFIGURAR GITHUB**

### **1. Criar Repositório**
```bash
# Inicializar git no projeto
git init

# Adicionar remote do GitHub
git remote add origin https://github.com/seu-usuario/rpa-eace-webhook.git

# Criar branch main
git checkout -b main
```

### **2. Preparar Arquivos**
```bash
# Adicionar arquivos essenciais
git add .env.example .gitignore Dockerfile docker-compose.yml
git add webhook_realtime.py eace_automation.py requirements_webhook.txt
git add *.sql *.md

# Commit inicial
git commit -m "Initial commit - EACE Webhook System"

# Push para GitHub
git push -u origin main
```

### **3. Configurar Repository Settings**
```yaml
# GitHub Repository Settings
Name: rpa-eace-webhook
Description: Sistema de webhook para automação EACE
Visibility: Private (recomendado)
```

---

## 🎛️ **PASSO 2: CONFIGURAR EASYPANEL**

### **1. Criar Nova Aplicação**
```yaml
# EasyPanel Dashboard
Create Service → App
Name: eace-webhook
Type: App
```

### **2. Configurar Source (GitHub)**
```yaml
# Source Configuration
Source Type: GitHub
Repository: seu-usuario/rpa-eace-webhook
Branch: main
Auto Deploy: ON (deploy automático em push)
```

### **3. Configurar Build**
```yaml
# Build Configuration
Build Method: Dockerfile
Dockerfile Path: ./Dockerfile
Build Context: .
```

### **4. Configurar Environment Variables**
```yaml
# Environment Variables (NÃO COMMITAR NO GITHUB)
SUPABASE_URL: https://seu-projeto.supabase.co
SUPABASE_KEY: sua_anon_key_aqui
EACE_USERNAME: seu_usuario_eace
EACE_PASSWORD: sua_senha_eace
WEBHOOK_URL: https://eace-webhook.seu-dominio.com/webhook/eace
PORT: 5000
LOG_LEVEL: INFO
PYTHONUNBUFFERED: 1
TZ: America/Sao_Paulo
```

### **5. Configurar Domain**
```yaml
# Domain Configuration
Domain: eace-webhook.seu-dominio.com
Port: 5000
SSL: Auto (Let's Encrypt)
```

### **6. Configurar Volumes**
```yaml
# Volumes (para persistir dados)
Container Path: /app/logs
Host Path: /var/lib/eace-webhook/logs

Container Path: /app/data  
Host Path: /var/lib/eace-webhook/data
```

---

## 🔧 **PASSO 3: CONFIGURAR DOCKERFILE OTIMIZADO**

O Dockerfile já está otimizado e inclui todas as dependências necessárias:

```dockerfile
# ✅ Já inclui:
- Python 3.11
- Chrome + ChromeDriver
- Todas as bibliotecas do sistema necessárias
- Configuração de usuário não-root
- Instalação das dependências Python
- Configuração de diretórios
```

**Nenhuma instalação manual necessária** - tudo está no container!

---

## 🚀 **PASSO 4: DEPLOY AUTOMÁTICO**

### **1. Primeira Deploy**
```bash
# EasyPanel detecta automaticamente
- Dockerfile
- docker-compose.yml (opcional)
- requirements_webhook.txt
- Código Python

# Build automático inicia
- Download do código do GitHub
- Build da imagem Docker
- Deploy do container
```

### **2. Deploys Subsequentes**
```bash
# A cada push no GitHub:
git add .
git commit -m "Update webhook system"
git push origin main

# EasyPanel automaticamente:
- Detecta mudanças
- Faz rebuild
- Redeploy automático
```

---

## 📊 **VANTAGENS DO GITHUB + EASYPANEL**

### **✅ Automação Total**
- **Deploy automático** em cada push
- **Rollback fácil** para commits anteriores
- **Versioning** completo do código
- **CI/CD** integrado

### **🔧 Gerenciamento**
- **Logs centralizados** no EasyPanel
- **Monitoring** integrado
- **SSL automático** (Let's Encrypt)
- **Backup** automático via GitHub

### **🔒 Segurança**
- **Variáveis de ambiente** seguras (não no código)
- **Secrets** gerenciados pelo EasyPanel
- **Código privado** no GitHub
- **Container isolado**

---

## 📋 **CONFIGURAÇÃO FINAL NO EASYPANEL**

### **Service Configuration:**
```yaml
# General
Name: eace-webhook
Type: App
Status: Running

# Source
Repository: github.com/seu-usuario/rpa-eace-webhook
Branch: main
Auto Deploy: Enabled

# Build
Build Command: docker build -t eace-webhook .
Start Command: python webhook_realtime.py

# Network
Domain: eace-webhook.seu-dominio.com
Port: 5000
SSL: Auto

# Environment
Variables: [configuradas via interface]

# Resources
Memory: 512MB (mínimo)
CPU: 0.5 vCPU (mínimo)
```

---

## 🧪 **TESTE PÓS-DEPLOY**

### **1. Verificar Aplicação**
```bash
# Health check
curl https://eace-webhook.seu-dominio.com/status

# Teste webhook
curl -X POST https://eace-webhook.seu-dominio.com/webhook/test \
  -H "Content-Type: application/json" \
  -d '{"ticket_id": 123}'
```

### **2. Verificar Logs**
```bash
# Via EasyPanel
Services → eace-webhook → Logs

# Via SSH (se necessário)
docker logs eace-webhook -f
```

### **3. Atualizar Supabase**
```sql
-- Executar no SQL Editor
CREATE OR REPLACE FUNCTION call_eace_webhook()
RETURNS TRIGGER AS $$
BEGIN
    webhook_url := 'https://eace-webhook.seu-dominio.com/webhook/eace';
    -- resto da função...
END;
$$ LANGUAGE plpgsql;
```

---

## 🏆 **RESULTADO FINAL**

**Sistema completo com:**
- ✅ **Deploy automático** via GitHub
- ✅ **SSL/HTTPS** automático
- ✅ **Monitoring** integrado
- ✅ **Rollback** em 1 clique
- ✅ **Logs centralizados**
- ✅ **Zero downtime** deploys
- ✅ **Webhook funcionando** 24/7

**Workflow de desenvolvimento:**
1. Código local → Push GitHub
2. EasyPanel detecta → Build automático
3. Deploy automático → Aplicação online
4. Webhook integrado → Sistema funcionando

**Próximo passo:** Executar limpeza e configurar GitHub! 🚀