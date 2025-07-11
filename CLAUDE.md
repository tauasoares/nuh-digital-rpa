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

## Próximos Passos
1. [x] Instalar Selenium WebDriver - **CONCLUÍDO**
2. [x] Testar script de login com Selenium - **CONCLUÍDO**
3. [x] Resolver problema na seleção de perfil - **CONCLUÍDO**
4. [ ] Mapear interface pós-login
5. [ ] Identificar fluxo de criação de tickets
6. [ ] Implementar automação completa de tickets
7. [ ] Criar interface de linha de comando

## 🎉 MARCO IMPORTANTE - LOGIN COMPLETO FUNCIONANDO!
**Data**: 2025-07-11
**Status**: ✅ AUTOMAÇÃO DE LOGIN 100% FUNCIONAL
- Login automático: ✅ Funcionando
- Seleção de perfil: ✅ Funcionando
- Acesso ao dashboard: ✅ Funcionando
- URL final: `https://eace.org.br/dashboard_fornecedor/[ID]`

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