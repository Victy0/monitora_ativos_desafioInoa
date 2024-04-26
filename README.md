# MONITORA ATIVOS
Repositório referente ao desafio para o processo seletivo da empresa Inoa Sistemas.

**Em resumo:** O objetivo do sistema é auxiliar um investidor nas suas decisões de comprar/vender ativos. Para tal, o sistema deve registrar periodicamente a cotação atual de ativos da B3 e também avisar, via e-mail, caso haja oportunidade de negociação.

Para recuperar a cotação atual, decidi recuperar as informações do Yahoo Finances, portanto o repositório está configurado para utilizae tal fonte pública.

Implementado por:
 - Victor Rodrigues Marques

# Requisitos

 - Python 3.9.7 ou superior

# Instalação

**1** - Clonar o repositório:

    git clone https://github.com/Victy0/monitora_ativos_desafioInoa.git

**2** - Criar venv:

    pyton -m venv venv

**3** - Ativar venv:

    venv/Scripts/activate

**4** - Instalar dependências:

    pip install -r requirements.txt

**5** - Realize a migração de banco de dados:

    python manage.py migrate

Para conseguir enviar os emails é necessário configurar as variáveis presente no arquivo .env no diretório raiz do projeto, com configurações desejadas de e-mail. Se quiser, pode utilizar a configuração de e-mail utilizada por mim em testes:

    EMAIL_HOST=smtp.gmail.com
    EMAIL_HOST_USER=sem.barreiras.vagas@gmail.com
    EMAIL_HOST_PASSWORD=dahsvzxgznmfivmc
    EMAIL_PORT=587

Porém com tais configurações, pode ser que seja bloqueado o uso do e-mail por restrições do Google. Por isso, é aconselhável configurar com um e-mail que você tenha controle.

# Utilização

**OBS:** Para esse, necessário estar com a venv ativada, passo 3 da Instalação.

Rodar servidor na venv (geralmente é possível acessar a aplicação pela porta 8000):

    python manage.py runserver

# Utilização sem ser em DEBUG

Por padrão o repositório está definido em sua configuração com DEBUG = True, caso queira alterar, é necessário um passo adicionar antes de usar o sistema.

**1** - alterar valor em monitoraAtivos/setting.py da variável DEBUG para False

    DEBUG = False

**2**- executar comando para criar diretório de arquivos estáticos que serão utilizados:

    py manage.py collectstatic

**3** - iniciar server normalmente

    python manage.py runserver

#  Estrutura de diretórios

O projeto se econtra dividido em 7 principais diretórios:

:small_blue_diamond: **monitoraAtivos**: configurações do sistema e do django utilizado.

:small_blue_diamond: **users**: app com todas as funcionalidades de gerenciamento de usuários para uso do sistema.

:small_blue_diamond: **stocks**: app com todas as funcionalidades de gerenciamento de ativos para uso do sistema.

:small_blue_diamond: **emails**: app de gerenciamento de e-mail (atualmente só envia e-mail).

:small_blue_diamond: **taskscheduler**: app de gerenciamento das tarefas agendadas.

:small_blue_diamond: **templates**: diretório que consta os templates básicos do sitema e que pode ser utilizado pelos apps.

:small_blue_diamond: **static**: diretório com arquivos estáticos de estilização (css) e imagens, que podem ser utilizados pelos apps.

    |____emais

    |____monitoraAtivos

    |____static
        |____css
        |____images

    |____tasksheculer

    |____templates
    
    |____users
