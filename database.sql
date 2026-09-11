CREATE DATABASE IF NOT EXISTS bot_atendimento;
USE bot_atendimento;

CREATE TABLE IF NOT EXISTS chamados (
    id INT AUTO_INCREMENT PRIMARY KEY,
    token VARCHAR(12) NOT NULL UNIQUE,
    usuario_id BIGINT NOT NULL,
    usuario_nome VARCHAR(100) NOT NULL,
    atendente_id BIGINT NULL,
    atendente_nome VARCHAR(100) NULL,
    canal_id BIGINT NOT NULL,
    status ENUM('ABERTO', 'EM_ANDAMENTO', 'FECHADO') DEFAULT 'ABERTO',
    data_abertura DATETIME DEFAULT CURRENT_TIMESTAMP,
    data_fechamento DATETIME NULL
);

CREATE TABLE IF NOT EXISTS mensagens_chamados (
    id INT AUTO_INCREMENT PRIMARY KEY,
    token VARCHAR(12) NOT NULL,
    autor_id BIGINT NOT NULL,
    autor_nome VARCHAR(100) NOT NULL,
    conteudo TEXT NOT NULL,
    data_envio DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (token) REFERENCES chamados(token) ON DELETE CASCADE
);