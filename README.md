# Bot de Suporte e Atendimento via Token (Discord)

Um bot completo para Discord desenvolvido em Python que cria um sistema profissional de tickets e suporte utilizando chats temporarios, geracao de tokens unicos (ex: TK-8F3A91) e armazenamento seguro em MySQL.

## Funcionalidades

- Gerador de Tokens Unicos: Cada atendimento possui uma credencial de seguranca.
- Canais Privados e Temporarios: Cria canais com permissoes exclusivas que sao deletados ao fim do atendimento.
- Controle de Acesso: Somente Administradores ou cargos de Suporte podem assumir e encerrar chamados.
- Auditoria e Logs em MySQL: Armazena historico completo de quem abriu, quem atendeu, horarios e todas as mensagens trocadas.
- Exportacao de Relatorios: Gera relatorios do atendimento em arquivo .txt enviados por DM, logs ou via comando de resgate.
- Arquitetura Segura: Estrutura modular e uso de .env (variaveis de ambiente) para protecao de credenciais.

## Tecnologias Utilizadas

- Python 3.10+
- discord.py (Interacao com a API do Discord)
- MySQL (Persistencia de dados)
- python-dotenv (Gestao de variaveis de ambiente)

---

## Como instalar e rodar localmente

### 1. Clonar o repositorio
\`\`\`bash
git clone https://github.com/SEU_USUARIO/bot-suporte-discord.git
cd bot-suporte-discord
\`\`\`

### 2. Instalar as dependencias
Recomenda-se o uso de um ambiente virtual (venv):
\`\`\`bash
pip install -r requirements.txt
\`\`\`

### 3. Configurar o Banco de Dados MySQL
1. Abra seu cliente MySQL (ex: phpMyAdmin, MySQL Workbench, DBeaver).
2. Execute o conteudo do arquivo database.sql para criar o banco de dados e as tabelas chamados e mensagens_chamados.

### 4. Configurar as Variaveis de Ambiente
1. Renomeie o arquivo .env.example para .env (ou crie um novo arquivo .env).
2. Preencha as configuracoes com os dados reais do seu servidor e banco:
\`\`\`ini
DISCORD_TOKEN=seu_token_aqui
GUILD_ID=id_do_seu_servidor
CATEGORY_ID=id_da_categoria_de_tickets
CANAL_LOGS_ID=id_do_canal_de_relatorios
NOME_CARGO_SUPORTE=Suporte

DB_HOST=localhost
DB_USER=root
DB_PASSWORD=sua_senha
DB_NAME=bot_atendimento
\`\`\`

### 5. Iniciar o Bot
\`\`\`bash
python main.py
\`\`\`
Se tudo estiver correto, o terminal exibira: Bot ativo como SeuBot#1234.

---

## Comandos Disponiveis

- !painel - Gera o painel de suporte com o botao "Abrir Atendimento" (Apenas Admins).
- !relatorio TK-XXXXXX - Exporta manualmente o historico em .txt de um chamado especifico (Apenas Admins).

## Seguranca

- Este projeto faz uso de Connection Pooling no banco de dados para suportar multiplos chamados simultaneos sem sobrecarga.
- O arquivo .env esta incluido no .gitignore para prevenir o vazamento de chaves (tokens e senhas) em repositorios publicos.

## Licenca

Este projeto esta sob a licenca MIT. Sinta-se a vontade para utiliza-lo e modifica-lo conforme necessario.
