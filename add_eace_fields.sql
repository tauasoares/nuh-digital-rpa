-- ===================================================
-- ADICIONAR CAMPOS EACE NA TABELA TICKETS
-- ===================================================

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