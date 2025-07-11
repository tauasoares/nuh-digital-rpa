# 🚀 **INSTRUÇÕES DE DEPLOY - HOSTINGER EASYPANEL**

## 📋 **PASSO A PASSO COMPLETO**

### **1. 📦 PREPARAR ARQUIVOS LOCALMENTE**

```bash
# Copiar .env.example para .env
cp .env.example .env

# Editar .env com suas credenciais reais
nano .env
```

**Configurar .env:**
```env
SUPABASE_URL=https://seu-projeto.supabase.co
SUPABASE_KEY=sua_anon_key_aqui
EACE_USERNAME=seu_usuario_eace
EACE_PASSWORD=sua_senha_eace
WEBHOOK_URL=https://eace-webhook.seu-dominio.com/webhook/eace
PORT=5000
LOG_LEVEL=INFO
```

### **2. 🌐 CONFIGURAR DOMÍNIO**

**Opção A: Subdomínio**
```
eace-webhook.seu-dominio.com
```

**Opção B: Subdiretório**
```
seu-dominio.com/eace-webhook
```

### **3. 📤 UPLOAD DOS ARQUIVOS**

**Via FTP/SFTP:**
```bash
# Criar diretório na VPS
mkdir -p /home/usuario/eace-webhook

# Upload dos arquivos essenciais:
- Dockerfile
- docker-compose.yml
- .env
- webhook_realtime.py
- eace_automation.py
- requirements_webhook.txt
- todos os arquivos .py do projeto
```

**Via SCP:**
```bash
scp -r rpa_eace/ usuario@sua-vps.com:/home/usuario/eace-webhook/
```

### **4. 🎛️ CONFIGURAR NO EASYPANEL**

#### **A. Criar Nova Aplicação**
1. Acesse EasyPanel
2. Clique em **"Create Service"**
3. Selecione **"App"**

#### **B. Configurar Source**
```yaml
Name: eace-webhook
Type: Docker
Build Method: Dockerfile
```

#### **C. Configurar Build**
```yaml
# Build Settings
Source: Upload/Git
Build Path: /home/usuario/eace-webhook
Dockerfile: Dockerfile
```

#### **D. Configurar Environment Variables**
```yaml
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

#### **E. Configurar Networking**
```yaml
# Port Mapping
Container Port: 5000
Public Port: 80 (via proxy)
```

#### **F. Configurar Domain**
```yaml
Domain: eace-webhook.seu-dominio.com
Path: /
```

#### **G. Configurar Volumes (Opcional)**
```yaml
# Para persistir logs
/app/logs → /var/lib/eace-webhook/logs
/app/data → /var/lib/eace-webhook/data
/app/screenshots_sistema → /var/lib/eace-webhook/screenshots
```

### **5. 🚀 DEPLOY**

1. **Clique em "Deploy"**
2. **Aguarde o build** (pode demorar 5-10 minutos)
3. **Verificar logs** em tempo real

### **6. ✅ TESTAR APLICAÇÃO**

```bash
# Teste básico
curl https://eace-webhook.seu-dominio.com/status

# Teste webhook
curl -X POST https://eace-webhook.seu-dominio.com/webhook/test \
  -H "Content-Type: application/json" \
  -d '{"ticket_id": 123}'
```

### **7. 🔧 CONFIGURAR TRIGGER NO SUPABASE**

**Atualizar URL no SQL:**
```sql
-- Executar no SQL Editor do Supabase
CREATE OR REPLACE FUNCTION call_eace_webhook()
RETURNS TRIGGER AS $$
DECLARE
    webhook_url TEXT;
    payload JSONB;
    request_id BIGINT;
BEGIN
    -- URL REAL DO EASYPANEL
    webhook_url := 'https://eace-webhook.seu-dominio.com/webhook/eace';
    
    payload := jsonb_build_object(
        'type', 'INSERT',
        'table', 'tickets',
        'record', to_jsonb(NEW),
        'timestamp', NOW()
    );
    
    SELECT INTO request_id
        net.http_post(
            url := webhook_url,
            headers := jsonb_build_object(
                'Content-Type', 'application/json',
                'User-Agent', 'Supabase-Webhook/1.0'
            ),
            body := payload
        );
    
    RETURN NEW;
EXCEPTION WHEN OTHERS THEN
    RAISE WARNING 'Erro ao chamar webhook: %', SQLERRM;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;
```

### **8. 🧪 TESTE COMPLETO**

```sql
-- Inserir ticket de teste
INSERT INTO tickets (incidente_id, descricao_enviada) 
VALUES (999, 'Teste EasyPanel - Site: INEP - 31382221');

-- Verificar processamento
SELECT * FROM tickets WHERE id = (SELECT MAX(id) FROM tickets);
```

---

## 🎯 **ALTERNATIVA: DOCKER COMPOSE DIRETO**

Se preferir usar Docker Compose diretamente na VPS:

```bash
# Na VPS
cd /home/usuario/eace-webhook

# Configurar .env
cp .env.example .env
nano .env

# Iniciar aplicação
docker-compose up -d

# Verificar status
docker-compose ps
docker-compose logs -f eace-webhook
```

---

## 📊 **MONITORAMENTO**

### **Via EasyPanel:**
- **Logs:** Services → eace-webhook → Logs
- **Métricas:** Services → eace-webhook → Metrics
- **Restart:** Services → eace-webhook → Restart

### **Via SSH:**
```bash
# Logs da aplicação
docker logs eace-webhook -f

# Status do container
docker ps

# Usar curl para teste
curl https://eace-webhook.seu-dominio.com/status
```

---

## 🔍 **TROUBLESHOOTING**

### **Build Falha:**
```bash
# Verificar logs de build
# Comum: falta de memória ou timeout
# Solução: aumentar timeout no EasyPanel
```

### **Aplicação não responde:**
```bash
# Verificar variáveis de ambiente
# Verificar se porta 5000 está exposta
# Verificar logs do container
```

### **Webhook não funciona:**
```bash
# Verificar se URL está correta no trigger
# Verificar se aplicação está acessível externamente
# Verificar logs do Supabase
```

---

## 🏆 **RESULTADO FINAL**

**Aplicação rodando em:**
- **URL:** https://eace-webhook.seu-dominio.com
- **Health Check:** https://eace-webhook.seu-dominio.com/status
- **Webhook:** https://eace-webhook.seu-dominio.com/webhook/eace

**Sistema 100% funcional:**
- ✅ **Container Docker** rodando no EasyPanel
- ✅ **Webhook em tempo real** funcionando
- ✅ **Integração com Supabase** configurada
- ✅ **Monitoramento** via EasyPanel
- ✅ **Logs persistentes** salvos
- ✅ **Auto-restart** em caso de falha

**Próximo passo:** Integrar com n8n para complete o fluxo! 🚀