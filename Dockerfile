# Usa uma imagem oficial e leve do Python
FROM python:3.11-slim

# Define o diretório de trabalho dentro do container
WORKDIR /app

# Copia apenas o arquivo de requisitos primeiro (ajuda no cache do Docker)
COPY requirements.txt .

# Instala as dependências sem armazenar cache para manter a imagem pequena
RUN pip install --no-cache-dir -r requirements.txt

# Copia o restante dos arquivos do projeto para o diretório de trabalho
COPY . .

# Comando que será executado quando o container for iniciado
CMD ["python", "-u", "main.py"]
