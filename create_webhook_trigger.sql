-- ===================================================
-- CRIAR TRIGGER PARA WEBHOOK EACE
-- ===================================================

-- Habilita a extensão pg_net se ainda não estiver habilitada
-- (necessária para fazer chamadas HTTP)
CREATE EXTENSION IF NOT EXISTS pg_net;

-- Cria função para chamar webhook
CREATE OR REPLACE FUNCTION call_eace_webhook()
RETURNS TRIGGER AS $$
DECLARE
    webhook_url TEXT;
    payload JSONB;
    request_id BIGINT;
BEGIN
    -- URL do webhook (substitua pela URL do seu servidor)
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

-- Verifica se o trigger foi criado
SELECT 
    trigger_name,
    event_manipulation,
    event_object_table,
    action_timing
FROM information_schema.triggers 
WHERE trigger_name = 'ticket_webhook_trigger';