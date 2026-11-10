SET GLOBAL event_scheduler = ON;

CREATE TABLE IF NOT EXISTS cliente (
    id_cliente INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    cpf VARCHAR(11) UNIQUE NOT NULL,
    email VARCHAR(150) UNIQUE NOT NULL,
    telefone VARCHAR(15),
    dados_publicos BOOLEAN DEFAULT false,
    data_nascimento DATE,
    data_cadastro TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);


CREATE TABLE IF NOT EXISTS ambiente (
	id_ambiente INT AUTO_INCREMENT PRIMARY KEY,
    id_cliente INT NOT NULL,
    ar_oxigenio DECIMAL(7,3) NOT NULL,
    ar_carbonico DECIMAL(7,3) NOT NULL,
    ar_poluentes DECIMAL(7,3) NOT NULL,
    ar_umidade DECIMAL(7,3) NOT NULL,
    ar_temperatura DECIMAL(7,3) NOT NULL,
    dados_publicos BOOLEAN DEFAULT false,
    data_cadastro TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_pedido_cliente
        FOREIGN KEY (id_cliente)
        REFERENCES cliente(id_cliente)
        ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS ambiente_tempo (
  id_ambiente_tempo int NOT NULL AUTO_INCREMENT,
  id_ambiente int NOT NULL,
  ar_oxigenio decimal(7,3) NOT NULL,
  ar_carbonico decimal(7,3) NOT NULL,
  ar_poluentes decimal(7,3) NOT NULL,
  ar_umidade decimal(7,3) NOT NULL,
  ar_temperatura decimal(7,3) NOT NULL,
  data_cadastro timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (id_ambiente_tempo),
  KEY fk_ambiente_tempo (id_ambiente),
  CONSTRAINT fk_ambiente_tempo 
    FOREIGN KEY (id_ambiente) 
        REFERENCES ambiente (id_ambiente) 
        ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS banco (
	id_banco INT AUTO_INCREMENT PRIMARY KEY,
    id_cliente INT NOT NULL UNIQUE,
    dinheiro DECIMAL(10,3) NOT NULL,
    senha VARCHAR(20) NOT NULL,
    CONSTRAINT fk_perfil_cliente
        FOREIGN KEY (id_cliente)
        REFERENCES cliente(id_cliente)
        ON DELETE CASCADE 
);

CREATE TABLE IF NOT EXISTS produto (
	id_produto INT AUTO_INCREMENT PRIMARY KEY,
    id_ambiente INT NOT NULL,
    tipo VARCHAR(20) NOT NULL,
    preco DECIMAL(7,3) NOT NULL,
    potencia DECIMAL(7,3) NOT NULL,
    CONSTRAINT fk_produto_ambiente
        FOREIGN KEY (id_ambiente)
        REFERENCES ambiente(id_ambiente)
        ON DELETE CASCADE 
);

DELIMITER $$
CREATE PROCEDURE IF NOT EXISTS SalvarDadosAmbiente() 
BEGIN
	INSERT INTO ambiente_tempo (id_ambiente, ar_oxigenio, ar_carbonico, ar_poluentes, ar_umidade, ar_temperatura)
	SELECT id_ambiente, ar_oxigenio, ar_carbonico, ar_poluentes, ar_umidade, ar_temperatura
	FROM ambiente;
END$$
DELIMITER ;

DELIMITER $$
CREATE PROCEDURE AtivarProdutos()
BEGIN
	SET SQL_SAFE_UPDATES = 0;
    UPDATE ambiente a
    /*
		'ROX' = -0.1 oxigenio
        'RCA' = -0.1 carbono
		'RPO' = -0.1 poluente
        'RUM' = -0.1 umidade
        'RTE' = -0.1 temperatura
        
        'AOX' = +0.1 oxigenio
        'ACA' = +0.1 carbono
        'APO' = +0.1 poluente
        'AUM' = +0.1 umidade
        'ATE' = +0.1 temperatura
        
		'OPC' = -0.1 oxigenio, +0.1 carbono
        'CPO' = +0.1 oxigenio, -0.1 carbono
        
        'ROX' ,'RCA', 'RPO', 'RUM', 'AOX', 'ACA', 'APO', 'AUM', 'OPC', 'CPO'
    */
    INNER JOIN (
        SELECT 
            id_ambiente,
            SUM(CASE 
                WHEN tipo = 'ROX' THEN -0.1
                WHEN tipo = 'AOX' THEN +0.1
                WHEN tipo = 'OPC' THEN -0.1        
                WHEN tipo = 'CPO' THEN +0.1
                ELSE 0 
            END) AS total_oxigenio,
            
            SUM(CASE 
                WHEN tipo = 'RCA' THEN -0.1
                WHEN tipo = 'ACA' THEN +0.1
                WHEN tipo = 'OPC' THEN +0.1
                WHEN tipo = 'CPO' THEN -0.1
                ELSE 0 
            END) AS total_carbonico,
            
            SUM(CASE 
                WHEN tipo = 'RPO' THEN -0.1
                WHEN tipo = 'APO' THEN +0.1
                ELSE 0 
            END) AS total_poluentes,
            
            SUM(CASE 
                WHEN tipo = 'RUM' THEN -0.1
                WHEN tipo = 'AUM' THEN +0.1
                ELSE 0 
            END) AS total_umidade,

            SUM(CASE 
                WHEN tipo = 'RTE' THEN -0.1
                WHEN tipo = 'ATE' THEN +0.1
                ELSE 0 
            END) AS total_temperaturas
        FROM produto
        GROUP BY id_ambiente
    ) p ON a.id_ambiente = p.id_ambiente
    
    SET 
		a.ar_oxigenio    = GREATEST(0, a.ar_oxigenio + p.total_oxigenio),
        a.ar_carbonico   = GREATEST(0, a.ar_carbonico + p.total_carbonico),
        a.ar_poluentes   = GREATEST(0, a.ar_poluentes + p.total_poluentes),
        a.ar_umidade     = GREATEST(0, a.ar_umidade + p.total_umidade),
        a.ar_temperatura = GREATEST(0, a.ar_temperatura + p.total_temperatura);
        
	SET SQL_SAFE_UPDATES = 1;
END$$
DELIMITER ;

CREATE EVENT evento_salvar_ambiente
ON SCHEDULE EVERY 10 MINUTE
STARTS CURRENT_TIMESTAMP
DO CALL SalvarDadosAmbiente();

CREATE EVENT evento_ativar_produto
ON SCHEDULE EVERY 5 MINUTE
STARTS CURRENT_TIMESTAMP
DO CALL AtivarProdutos();

INSERT INTO cliente
	(nome, cpf, email, telefone, dados_publicos, data_nascimento)
VALUES
	('Ana Silva', '12345678901', 'ana@email.com', '21999998888', true, '1995-05-20'),
	('Carlos Par', '12345178901', 'cal@email.com', '21979998888', true, '1996-11-11'),
	('Mariana Souza', '23456789012', 'mariana.souza@email.com', '21988887777', true, '1992-04-15'),
	('Lucas Oliveira', '34567890123', 'lucas.oliveira@email.com', '21977776666', false, '1988-08-23'),
	('Fernanda Lima', '45678901234', 'fernanda.lima@email.com', '21966665555', true, '2001-01-30'),
	('Rafael Costa', '56789012345', 'rafael.costa@email.com', '21955554444', false, '1995-12-05'),
	('Beatriz Santos', '67890123456', 'beatriz.santos@email.com', '21944443333', true, '1999-07-18');


INSERT INTO ambiente
	(id_cliente, ar_oxigenio, ar_carbonico, ar_poluentes, ar_umidade, ar_densidade, dados_publicos)
VALUES
	(1, 12.5, 12.5, 4.56, 2.34, 1.00, true),
    (1, 12.500, 12.500, 4.560, 2.340, 1.000, true),
    (3, 20.950, 0.040, 0.120, 45.500, 1.225, true),
    (4, 19.800, 0.080, 1.450, 60.200, 1.180, false),
    (5, 21.000, 0.030, 0.050, 50.000, 1.200, true),
    (6, 18.500, 0.150, 2.300, 75.800, 1.150, false),
    (7, 20.500, 0.050, 0.800, 40.000, 1.210, true),
    (2, 17.200, 0.200, 3.100, 82.300, 1.140, false),
    (2, 21.200, 0.035, 0.020, 48.000, 1.205, true);   

INSERT INTO banco
	(id_cliente, dinheiro, senha)
VALUES
	(1, 155.65, '1234'),
    (2, 2500.000, '1234'),
    (3, 850.500,  '1234'),
    (4, 12000.750, '1234'),
    (5, 430.200,  '1234'),
    (6, 3100.000, '1234'),
    (7, 95.800,   '1234');
 
    
INSERT INTO produto
	(id_ambiente, tipo, preco, potencia)
VALUES
	(1, 'OPC', 55.99, 1.0),
    (1, 'RPO', 55.99, 1.0),
    (1, 'AOX', 55.99, 1.0),
    (2, 'ROX', 45.500, 1.0),
    (2, 'RCA', 50.000, 1.5),
    (3, 'RPO', 55.990, 1.0),
    (3, 'RUM', 62.300, 2.0),
    (4, 'AOX', 78.900, 1.2),
    (4, 'ACA', 85.000, 2.5),
    (5, 'APO', 40.000, 1.0),
    (5, 'AUM', 95.500, 3.0),
    (6, 'OPC', 55.990, 1.0),
    (6, 'CPO', 110.000, 2.0),
    (7, 'ROX', 48.750, 1.0),
    (7, 'AOX', 80.000, 1.5),
    (8, 'RCA', 52.000, 1.2),
    (8, 'ACA', 88.400, 2.0),
    (9, 'RUM', 65.000, 1.0),
    (9, 'CPO', 115.500, 2.5);   
    
INSERT INTO ambiente_tempo
	(id_ambiente, ar_oxigenio, ar_carbonico, ar_poluentes, ar_umidade, ar_densidade)
VALUES
	(1, 12.5, 12.5, 4.56, 2.34, 1.00);

