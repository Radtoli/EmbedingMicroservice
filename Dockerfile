# Imagem base oficial do Python
FROM python:3.10-slim

# Diretório de trabalho
WORKDIR /app

# Copia o arquivo main.py para o container
COPY main.py .

# Instala as dependências necessárias
RUN pip install --no-cache-dir fastapi uvicorn sentence-transformers

# Expõe a porta padrão do FastAPI/Uvicorn
EXPOSE 8000

# Comando para iniciar o servidor
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]