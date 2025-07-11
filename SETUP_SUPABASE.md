# 🔧 **SETUP DO SUPABASE - INSTRUÇÕES**

## 📋 **PASSO A PASSO**

### **1. Executar SQL para Adicionar Campos**

No painel do Supabase, vá em **SQL Editor** e execute:

```sql
-- Adiciona campos EACE na tabela tickets
ALTER TABLE tickets 
ADD COLUMN IF NOT EXISTS eace_status VARCHAR(20),
ADD COLUMN IF NOT EXISTS eace_os_numero VARCHAR(50),
ADD COLUMN IF NOT EXISTS eace_processado_em TIMESTAMP;

-- Adiciona índices para performance
CREATE INDEX IF NOT EXISTS idx_tickets_eace_status ON tickets(eace_status);
CREATE INDEX IF NOT EXISTS idx_tickets_eace_os_numero ON tickets(eace_os_numero);

-- Adiciona comentários para documentação
COMMENT ON COLUMN tickets.eace_status IS 'Status do processamento EACE: PROCESSANDO, CONCLUIDO, ERRO';
COMMENT ON COLUMN tickets.eace_os_numero IS 'Número da OS criada no EACE (ex: 20250008125)';
COMMENT ON COLUMN tickets.eace_processado_em IS 'Timestamp do processamento no EACE';
```

### **2. Verificar se os Campos foram Criados**

```sql
-- Verifica se os campos foram adicionados
SELECT 
    column_name,
    data_type,
    is_nullable,
    column_default
FROM information_schema.columns 
WHERE table_name = 'tickets' 
AND column_name IN ('eace_status', 'eace_os_numero', 'eace_processado_em')
ORDER BY ordinal_position;
```

### **3. Criar Trigger para Webhook**

⚠️ **IMPORTANTE**: Antes de executar, substitua `https://seu-servidor.com/webhook/eace` pela URL real do seu servidor.

```sql
-- Habilita a extensão pg_net se ainda não estiver habilitada
CREATE EXTENSION IF NOT EXISTS pg_net;

-- Cria função para chamar webhook
CREATE OR REPLACE FUNCTION call_eace_webhook()
RETURNS TRIGGER AS $$
DECLARE
    webhook_url TEXT;
    payload JSONB;
    request_id BIGINT;
BEGIN
    -- URL do webhook (SUBSTITUA PELA URL DO SEU SERVIDOR)
    webhook_url := 'https://seu-servidor.com/webhook/eace';
    
    -- Monta payload com dados do ticket
    payload := jsonb_build_object(
        'type', 'INSERT',
        'table', 'tickets',
        'record', to_jsonb(NEW),
        'timestamp', NOW()
    );
    
    -- Chama webhook usando pg_net (assíncrono)
    SELECT INTO request_id
        net.http_post(
            url := webhook_url,
            headers := jsonb_build_object(
                'Content-Type', 'application/json',
                'User-Agent', 'Supabase-Webhook/1.0'
            ),
            body := payload
        );
    
    -- Log da requisição (opcional)
    RAISE NOTICE 'Webhook chamado para ticket % - Request ID: %', NEW.id, request_id;
    
    RETURN NEW;
    
EXCEPTION WHEN OTHERS THEN
    -- Log erro mas não falha a inserção do ticket
    RAISE WARNING 'Erro ao chamar webhook para ticket %: %', NEW.id, SQLERRM;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Remove trigger existente se houver
DROP TRIGGER IF EXISTS ticket_webhook_trigger ON tickets;

-- Cria trigger que executa webhook após INSERT
CREATE TRIGGER ticket_webhook_trigger
    AFTER INSERT ON tickets
    FOR EACH ROW
    EXECUTE FUNCTION call_eace_webhook();
```

### **4. Verificar se o Trigger foi Criado**

```sql
-- Verifica se o trigger foi criado
SELECT 
    trigger_name,
    event_manipulation,
    event_object_table,
    action_timing
FROM information_schema.triggers 
WHERE trigger_name = 'ticket_webhook_trigger';
```

## 🎯 **ESTRUTURA FINAL DA TABELA `tickets`**

Após executar os comandos, sua tabela `tickets` terá:

```sql
tickets:
├── id (PK)
├── incidente_id (FK)
├── descricao_enviada
├── data_abertura
├── eace_status          -- 🆕 PROCESSANDO, CONCLUIDO, ERRO
├── eace_os_numero       -- 🆕 Ex: 20250008125
└── eace_processado_em   -- 🆕 Timestamp do processamento
```

## 🔄 **COMO FUNCIONA**

1. **Inserção de Ticket:**
   ```sql
   INSERT INTO tickets (incidente_id, descricao_enviada) 
   VALUES (123, 'Equipamento offline - Site: INEP - 31382221');
   ```

2. **Trigger Executa Automaticamente:**
   - Função `call_eace_webhook()` é chamada
   - Payload é montado com dados do ticket
   - Webhook é chamado via `pg_net.http_post()`

3. **Webhook Processa:**
   - Extrai INEP do nome do site
   - Executa automação EACE
   - Atualiza campos `eace_status`, `eace_os_numero`, `eace_processado_em`

## 🧪 **TESTE APÓS SETUP**

```sql
-- Teste de inserção
INSERT INTO tickets (incidente_id, descricao_enviada) 
VALUES (999, 'Teste webhook - Site: INEP - 31382221');

-- Verificar se foi processado
SELECT 
    id,
    descricao_enviada,
    eace_status,
    eace_os_numero,
    eace_processado_em
FROM tickets 
WHERE id = (SELECT MAX(id) FROM tickets);
```

## ⚠️ **OBSERVAÇÕES IMPORTANTES**

1. **URL do Webhook:** Substitua `https://seu-servidor.com/webhook/eace` pela URL real
2. **Extensão pg_net:** Necessária para fazer chamadas HTTP
3. **Tratamento de Erros:** Webhook falha não impede inserção do ticket
4. **Logs:** Mensagens de debug aparecem nos logs do Supabase

## 📋 **CHECKLIST**

- [ ] Executar SQL para adicionar campos
- [ ] Verificar se campos foram criados
- [ ] Atualizar URL do webhook no trigger
- [ ] Executar SQL para criar trigger
- [ ] Verificar se trigger foi criado
- [ ] Testar com inserção de ticket
- [ ] Verificar logs do Supabase

**Pronto! Supabase configurado para webhook em tempo real.** 🚀