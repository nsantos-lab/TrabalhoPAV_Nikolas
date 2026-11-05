# 1. Usa uma imagem oficial e leve do Python
FROM python:3.11-slim

# 2. Define o diretório de trabalho dentro do container
WORKDIR /app

# 3. Evita que o Python escreva os arquivos .pyc no disco
ENV PYTHONDONTWRITEBYTECODE=1

# 4. Garante que os logs do Flask saiam direto no terminal sem atraso (buffer)
ENV PYTHONUNBUFFERED=1

# 5. Copia primeiro apenas o requirements.txt (melhora o cache do Docker)
COPY requirements.txt .

# 6. Instala as dependências do Python
RUN pip install --no-cache-dir -r requirements.txt

# 7. Copia o restante do código da API para dentro do container
COPY manage.py .
COPY src ./src

# 8. Informa que o container escuta na porta 5000 (padrão do Flask)
EXPOSE 5000

# 9. Comando para rodar a API usando o servidor de produção do Flask
    # aparentemente o "run" é um servidor de desenvolvimento.
    #CMD ["flask", "run", "--host=0.0.0.0", "--port=5000"]
CMD ["flask", "--app", "manage", "run", "--host=0.0.0.0", "--port=5000"]
