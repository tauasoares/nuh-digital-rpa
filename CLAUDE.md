# Projeto RPA EACE - Automação de Tickets

## Objetivo
Automatizar o acesso ao sistema EACE (https://eace.org.br) para abertura de tickets de forma automática, já que o sistema não possui API.

## Credenciais de Acesso
- **URL**: https://eace.org.br/login?login=login
- **Usuário**: raiseupbt@gmail.com
- **Senha**: @Uujpgi8u
- **Perfil**: Fornecedor

## Status Atual dos Testes
### ✅ Análise Completa do Sistema
- **Plataforma identificada**: Bubble.io
- **API funcionando**: `/api/1.1/init/data` (200 OK)
- **Session UID**: Gerado dinamicamente
- **Dados de usuário**: Estrutura JSON mapeada

### ✅ Login Automatizado (Selenium)
- Login com email e senha: **FUNCIONANDO PERFEITAMENTE**
- Selenium configurado e testado com sucesso
- Screenshots gerados: login_page.png, pos_login.png
- Seletores XPath funcionais:
  - Email: `//input[@placeholder='seuemail@email.com']`
  - Senha: `//input[@type='password']`
  - Botão Login: `//button[contains(text(), 'Log In')]`

### ✅ Seleção de Perfil
- Após login, aparece opção "Selecione o perfil Fornecedor"
- **RESOLVIDO**: Elemento é uma `div`, não um `button`
- Seletor funcionando: `//*[contains(text(), 'Fornecedor')]`
- Redirecionamento para dashboard: ✅ Funcionando
- **STATUS**: CONCLUÍDO - Automação completa funcionando!

### ✅ Navegação para "Controle de OS" (NOVO MARCO!)
- **Data**: 2025-07-14
- **STATUS**: ✅ NAVEGAÇÃO PARA PÁGINA DE OS 100% FUNCIONAL!
- **Método**: Abordagem de duas fases (expandir menu + clicar item)
- **Endpoint**: `/test-expandable-menu` - FUNCIONANDO PERFEITAMENTE
- **Screenshots de sucesso**: `expandable_05_second_element.png` e `expandable_06_final.png`
- **Técnica implementada**:
  - Fase 1: Identifica e clica no botão do menu hambúrguer
  - Fase 2: Procura por "Gerenciar chamados" no menu expandido
  - Fase 3: Análise estrutural e clique no segundo elemento do menu lateral
- **URL de destino**: `https://eace.org.br/dashboard_fornecedor/[ID]` → Página "Controle de OS"

## 📋 ESTADO ATUAL DO PROJETO (2025-07-15)
### ✅ O que está funcionando 100%:
1. **Login completo**: Email + senha + seleção de perfil Fornecedor
2. **Navegação para página de OS**: Menu hambúrguer → "Gerenciar chamados" → Controle de OS
3. **Sistema de monitoramento visual**: Screenshots automáticos de cada etapa
4. **Webhook funcionando**: Endpoints para testes via browser
5. **Deploy automático**: GitHub → EasyPanel → VPS
6. **Interface HTML organizada**: Página com todos os endpoints categorizados
7. **Endpoint `/test-expandable-menu`**: 100% funcional, chega na página de Controle de OS

### 🎯 Próximo passo imediato:
**Executar análise sistemática com endpoint `/analyze-dashboard-elements`** para:
- Identificar o botão correto do menu hambúrguer
- Testar todos os candidatos a menu sistematicamente
- Verificar qual expande o menu e mostra "Gerenciar chamados"
- Navegar corretamente para a página "Controle de OS"
- Após navegação bem-sucedida, mapear o botão "Adicionar nova OS"

### 🔧 Endpoints Ativos:
- `/test-expandable-menu` - ✅ Navegação completa até página de OS
- `/map-os-button-fixed` - ✅ **FUNCIONA**: Usa código idêntico ao test-expandable-menu
- `/analyze-dashboard-elements` - 🔍 Análise sistemática completa do dashboard
- `/realtime-analysis` - 🖥️ **NOVO**: Visualização em tempo real com logs e screenshots
- `/debug-step-by-step` - ❌ **PROBLEMA**: Para no dashboard, não navega para OS
- Interface HTML `/` - 📱 Página visual com todos os endpoints

### 📁 Arquivos principais:
- `webhook_simple.py`: Endpoint `/test-expandable-menu` (FUNCIONANDO) + `/analyze-dashboard-elements` (NOVO)
- `endpoints.html`: Interface HTML atualizada com novo endpoint
- `CLAUDE.md`: Este arquivo (documentação atualizada)
- Screenshots em `/tmp/screenshots` via galeria web

### 🔍 Análise dos Endpoints:

#### ✅ **Endpoints que FUNCIONAM**:
1. **`/test-expandable-menu`**: Navegação completa para página de OS
   - Usa lógica robusta com múltiplos seletores
   - Verifica expansão do menu efetivamente
   - Procura por "Gerenciar chamados" após expansão
   - **RESULTADO**: Gera `expandable_05_second_element.png` e `expandable_06_final.png` na página de OS

2. **`/map-os-button-fixed`**: Código idêntico ao test-expandable-menu
   - Mesma lógica de expansão de menu
   - Mesma verificação de "Gerenciar chamados"
   - **RESULTADO**: Gera `expandable_01_dashboard.png`, `expandable_02_menu_not_expanded.png`, `expandable_05_second_element.png`, `expandable_06_final.png`

#### ❌ **Endpoint com PROBLEMA**:
1. **`/debug-step-by-step`**: Para no dashboard, não navega para OS
   - Usa lógica diferente e limitada (apenas 3 seletores)
   - Critério diferente para verificar expansão (>15 elementos)
   - **RESULTADO**: Gera apenas `step_01_login_page.png`, `step_02_credentials_filled.png`, `step_03_after_login.png`, `step_04_profile_selected.png`, `step_05_dashboard.png`, `step_07_final_debug.png`

#### 🖥️ **Endpoints de Visualização**:
1. **`/realtime-analysis`**: Interface visual em tempo real
   - Visualiza logs ao vivo durante execução
   - Mostra screenshots conforme são gerados
   - Usa código que funciona do `/map-os-button-fixed`
   - Interface terminal verde com progresso visual
   - Atualização automática de imagens a cada 10 segundos

2. **`/visual-step-by-step`**: **NOVO** - Passo a passo visual detalhado
   - **8 passos visuais** desde login até análise da página de OS
   - **Progresso em tempo real** com barra visual e indicadores
   - **Análise da página de Controle de OS**: Mapeia botões, elementos, URLs
   - **Interface moderna**: Estilo GitHub dark com animações
   - **Mapeamento completo**: Identifica botão "Adicionar nova OS"
   - **Screenshots ordenados**: `detailed_step_01.png` até `detailed_step_08.png`
   - **Análise JSON**: Salva `os_page_analysis.json` com elementos mapeados

## Próximos Passos
1. [x] Instalar Selenium WebDriver - **CONCLUÍDO**
2. [x] Testar script de login com Selenium - **CONCLUÍDO**
3. [x] Resolver problema na seleção de perfil - **CONCLUÍDO**
4. [x] Mapear interface pós-login - **CONCLUÍDO**
5. [x] Navegação para página de controle de OS - **CONCLUÍDO**
6. [ ] **PRÓXIMO**: Mapear interface da página "Controle de OS"
7. [ ] Identificar fluxo de criação de tickets
8. [ ] Implementar automação completa de tickets
9. [ ] Criar interface de linha de comando

## 🎉 MARCO IMPORTANTE - NAVEGAÇÃO COMPLETA FUNCIONANDO!
**Data**: 2025-07-14
**Status**: ✅ AUTOMAÇÃO COMPLETA ATÉ PÁGINA DE OS!
- Login automático: ✅ Funcionando
- Seleção de perfil: ✅ Funcionando
- Acesso ao dashboard: ✅ Funcionando
- **Navegação para "Controle de OS": ✅ FUNCIONANDO!**
- URL inicial: `https://eace.org.br/dashboard_fornecedor/[ID]`
- URL final: Página "Controle de OS" (segunda tela do sistema)

## Instalações Realizadas
### ✅ Ambiente Python
- Python 3.12.3 configurado
- Ambiente virtual criado e ativado
- Dependências instaladas:
  - selenium, webdriver-manager, requests
  - beautifulsoup4, lxml, urllib3, certifi, python-dotenv

### ✅ Sistema WSL
- Chromium browser instalado
- Bibliotecas do sistema para ChromeDriver:
  - libnss3, libxi6, libxcursor1, libxcomposite1
  - libxdamage1, libxtst6, libxrandr2, libasound2t64
  - libatk1.0-0t64, libgtk-3-0t64

## Estrutura do Projeto
```
rpa_eace/
├── CLAUDE.md (este arquivo)
├── login_automation.py (a criar)
├── ticket_automation.py (a criar)
└── utils/ (a criar)
```

## Tecnologias a Utilizar
- Python
- Selenium WebDriver
- BeautifulSoup (se necessário)
- Requests (para simulação de requisições)

## Observações Técnicas
- **Plataforma**: Bubble.io (aplicação no-code)
- **Arquitetura**: Elementos dinâmicos gerados por JavaScript
- **Segurança**: Bloqueio de ferramentas de desenvolvedor
- **API**: Sistema interno do Bubble.io (https://eace.org.br/api/1.1/)
- **Autenticação**: Fluxo multi-perfil após login inicial
- **Seletores funcionais**:
  - Email: `//input[@placeholder='seuemail@email.com']`
  - Senha: `//input[@type='password']`
  - Login: `//button[contains(text(), 'Log In')]`
  - Perfil: `//button[contains(., 'Fornecedor')]`