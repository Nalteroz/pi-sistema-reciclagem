# Sistema de gerenciamento para centro de reciclagem
## Introdução
Esse trabalho foi criado como solução para o projeto integrador da UNIVESP. Trata-se de um sistema de gerenciamento simples construido em Python usando Flask para um centro de reciclagem. 

## Requerimentos
Todos os requerimentos estão listados [aqui](app/requirements.txt). Para instalar, execute `pip install -r requirements.txt`.

## Execução
Para executar, primeiro crie um arquivo *.env* com o URI do banco Postgre e o segredo do JWT. Como a seguir
```env
BI_DATABASE_URI = postgresql://<user>:<password>@<host>:<port>/<db>
JWT_SECRET_KEY=<sha256 secret>
```
Após configurar o arquivo, execute no terminal `flask db upgrade` para executar as *migrations* do banco. Em seguida basta executar o código com `flask run`.