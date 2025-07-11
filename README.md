# 🚀 NUH Digital RPA - Sistema EACE Webhook

## 📋 Resumo
Sistema completo de automação para abertura de tickets no portal EACE (eace.org.br) com webhook em tempo real integrado ao n8n.

## ✅ Status do Projeto - COMPLETO
- **Webhook em tempo real** funcionando
- **Automação EACE** completa
- **Integração Supabase** via triggers
- **Deploy Docker** otimizado
- **Sistema n8n** integrado

## 🎯 Funcionalidades
- **Webhook /eace** - Processa tickets automaticamente
- **Extração INEP** - Extrai número INEP dos nomes de sites
- **Automação Selenium** - Cria OS no sistema EACE
- **Logs detalhados** - Monitoramento completo
- **Deploy EasyPanel** - Container Docker

## 🐳 Arquivos Principais
- `webhook_realtime.py` - Servidor webhook Flask
- `eace_automation.py` - Automação do sistema EACE
- `Dockerfile` - Container com Chrome + Python
- `docker-compose.yml` - Orquestração do sistema
- `*.sql` - Scripts para configuração do Supabase

## 🚀 Deploy
Sistema pronto para deploy no EasyPanel via GitHub:
1. **Container Docker** com todas as dependências
2. **Deploy automático** a cada push
3. **Variáveis de ambiente** configuráveis
4. **SSL automático** via Let's Encrypt

## 🔧 Configuração
```bash
# Copiar template
cp .env.example .env

# Configurar variáveis
SUPABASE_URL=https://seu-projeto.supabase.co
SUPABASE_KEY=sua_anon_key
EACE_USERNAME=seu_usuario
EACE_PASSWORD=sua_senha
WEBHOOK_URL=https://seu-dominio.com/webhook/eace
```

## 🎛️ Integração n8n
Sistema integrado com n8n para:
- Detectar dispositivos offline
- Criar tickets no ITSM
- Disparar webhook automaticamente
- Criar OS no EACE em tempo real

## 📊 Tecnologias
- Python 3.11 + Flask
- Selenium WebDriver + Chrome
- Docker + docker-compose
- PostgreSQL + Supabase
- GitHub + EasyPanel
- n8n Workflow

---
*Sistema desenvolvido em 2025-07-11 com Claude Code*
