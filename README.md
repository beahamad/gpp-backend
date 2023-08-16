# gpp-backend

um backend para o aplicativo do guardinha do parque do povo
 
## configuração do banco de dados local

Para executar o aplicativo, é necessário ter o postgresql instalado e configurado corretamente.

Primeiro, instale o postgresql

```
sudo apt install postgresql postgresql-contrib
```

Isso automaticamente criará um user padrão para o postgres, mude para ele

```
sudo -i -u postgres
```

Agora para configurar o novo user

```
psql
```

Crie um outro user para acessar o banco de dados. 

Aqui está como criar um super user, pois ele já tem todas as permissões necessárias

```
create role [nome do usuario] with login superuser password ['senha'];
```

Resta alterar as informações dentro do arquivo `dbconfig.ini`, colocando o seu user e senha. se não existir um bd, o programa criará um com o nome que você colocar em `database`

agora rode o script de inicialização do bd

```
python3 init_db.py
```

Pronto. O bd deve ter sido criado e estar rodando. agora pode executar o backend normalmente

```
python3 app.py
```
