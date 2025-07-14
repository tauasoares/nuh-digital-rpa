FROM python:3.11-slim

# Instalar dependências do sistema
RUN apt-get update && apt-get install -y \
    wget \
    curl \
    unzip \
    gnupg \
    xvfb \
    && rm -rf /var/lib/apt/lists/*

# Instalar Chrome e dependências para Playwright
RUN wget -q -O - https://dl.google.com/linux/linux_signing_key.pub | apt-key add - \
    && echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google-chrome.list \
    && apt-get update \
    && apt-get install -y google-chrome-stable \
    && rm -rf /var/lib/apt/lists/*

# Definir diretório de trabalho
WORKDIR /app

# Copiar requirements e instalar dependências Python
COPY requirements_webhook.txt .
RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r requirements_webhook.txt

# Instalar browsers do Playwright
RUN playwright install chromium \
    && playwright install-deps chromium

# Copiar código da aplicação
COPY . .

# Criar diretórios necessários
RUN mkdir -p logs data screenshots_sistema /tmp/screenshots

# Expor porta
EXPOSE 5000

# Variáveis de ambiente para Chrome
ENV DISPLAY=:99
ENV CHROME_BIN=/usr/bin/google-chrome
ENV CHROMEDRIVER_PATH=/usr/local/bin/chromedriver

# Comando para iniciar aplicação
CMD ["python", "webhook_simple.py"]