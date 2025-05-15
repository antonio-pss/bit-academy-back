# Dockerfile para projeto Django usando Alpine Linux

# Imagem base com Python
FROM python:3.10-alpine

# Variáveis de ambiente para otimização
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Instala dependências do sistema usando apk (Alpine)
RUN apk add --no-cache \
    build-base \
    libpq \
    && apk add --no-cache --virtual .build-deps gcc musl-dev

# Diretório de trabalho
WORKDIR /app

# Copia o requirements e instala os pacotes Python
COPY requirements.txt /app/
RUN pip install --upgrade pip \
    && pip install -r requirements.txt

# Copia todo o código do projeto para dentro do container
COPY . /app/

# Expondo a porta padrão do Django
EXPOSE 8000

# Comando padrão: aplica migrations e inicia o servidor de desenvolvimento
CMD ["sh", "-c", "python manage.py migrate --noinput && python manage.py runserver 0.0.0.0:8000"]