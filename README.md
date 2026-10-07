# AV5

# Passo a Passo Github:

git clone "link do repositorio"

cd "nome do repositório"

git config user.name "nome de usuario"

git config user.email "email do usuario"

git add *

git commit -m "Comentário sobre o commit"

git push


# Passo a Passo pra baixar Repositório e rodar:

git clone "link do repositorio"

Criar arquivo chamado ".env" com as seguintes informações:

MYSQL_USER=XXXX

MYSQL_PASSWORD="XXXX"

MYSQL_PORT=XXXX

MYSQL_HOST=XXXXXXXX

MYSQL_DATABASE=XXXXXX

uv run index.py
