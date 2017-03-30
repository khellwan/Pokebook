CREATE TABLE artistacinematografico (
    id character varying(4) NOT NULL,
    endereco character varying(15) NOT NULL,
    telefone character varying(9) NOT NULL
);

CREATE TABLE artistamusical (
    id integer NOT NULL,
    nome_artistico character varying(100),
    "país" character varying(50),
    "gênero" character varying(50)
);

CREATE TABLE ator (
    id_artista character varying(4) NOT NULL,
    id_filme character varying(50) NOT NULL
);

CREATE TABLE banda (
    id_artista integer NOT NULL
);

CREATE TABLE bloqueia (
    login_bloqueador character varying(100) NOT NULL,
    login_bloqueado character varying(100) NOT NULL,
    motivo_spam boolean NOT NULL,
    motivo_abusivo boolean NOT NULL,
    motivo_pessoal boolean NOT NULL,
    motivo_outros character varying(100)
);

CREATE TABLE cantor (
    id_artista integer NOT NULL
);

CREATE TABLE categoria (
    nome_categoria character varying(50) NOT NULL,
    supercategoria character varying(50) NOT NULL
);

CREATE TABLE conhecido (
    login character varying(100) NOT NULL
);

CREATE TABLE diretor (
    id_artista character varying(4) NOT NULL,
    id_filme character varying(50) NOT NULL
);

CREATE TABLE filme (
    id character varying(50) NOT NULL,
    nome character varying(50) NOT NULL,
    data_de_lancamento date NOT NULL,
    nome_categoria character varying(50) NOT NULL
);

CREATE TABLE musico (
    nome_real character varying(100) NOT NULL,
    estilo_musical character varying(50),
    data_de_nascimento character varying(20),
    id_cantor integer,
    id_banda integer
);

CREATE TABLE participacao (
    id_ator character varying(4) NOT NULL,
    id_filme character varying(50) NOT NULL,
    id_diretor character varying(4) NOT NULL
);

CREATE TABLE pessoa (
    cidade_natal character varying(100) NOT NULL,
    nome_completo character varying(100) NOT NULL,
    login character varying(100) NOT NULL
);

CREATE TABLE registra (
    login_registrador character varying(100) NOT NULL,
    login_registrado character varying(100) NOT NULL
);

ALTER TABLE ONLY artistacinematografico
    ADD CONSTRAINT artistacinematografico_pkey PRIMARY KEY (id);

ALTER TABLE ONLY artistamusical
    ADD CONSTRAINT artistamusical_pkey PRIMARY KEY (id);

ALTER TABLE ONLY ator
    ADD CONSTRAINT ator_pkey PRIMARY KEY (id_artista, id_filme);

ALTER TABLE ONLY banda
    ADD CONSTRAINT banda_pkey PRIMARY KEY (id_artista);

ALTER TABLE ONLY bloqueia
    ADD CONSTRAINT bloqueia_pkey PRIMARY KEY (login_bloqueador, login_bloqueado);

ALTER TABLE ONLY cantor
    ADD CONSTRAINT cantor_pkey PRIMARY KEY (id_artista);

ALTER TABLE ONLY categoria
    ADD CONSTRAINT categoria_pkey PRIMARY KEY (nome_categoria);

ALTER TABLE ONLY conhecido
    ADD CONSTRAINT conhecido_pkey PRIMARY KEY (login);

ALTER TABLE ONLY diretor
    ADD CONSTRAINT diretor_pkey PRIMARY KEY (id_artista, id_filme);

ALTER TABLE ONLY filme
    ADD CONSTRAINT filme_pkey PRIMARY KEY (id);

ALTER TABLE ONLY musico
    ADD CONSTRAINT musico_pkey PRIMARY KEY (nome_real);

ALTER TABLE ONLY participacao
    ADD CONSTRAINT participacao_pkey PRIMARY KEY (id_ator, id_filme);

ALTER TABLE ONLY pessoa
    ADD CONSTRAINT pessoa_pkey PRIMARY KEY (login);

ALTER TABLE ONLY registra
    ADD CONSTRAINT registra_pkey PRIMARY KEY (login_registrador, login_registrado);

ALTER TABLE ONLY ator
    ADD CONSTRAINT ator_id_artista_fkey FOREIGN KEY (id_artista) REFERENCES artistacinematografico(id) ON DELETE CASCADE;

ALTER TABLE ONLY ator
    ADD CONSTRAINT ator_id_filme_fkey FOREIGN KEY (id_filme) REFERENCES filme(id);

ALTER TABLE ONLY banda
    ADD CONSTRAINT banda_id_artista_fkey FOREIGN KEY (id_artista) REFERENCES artistamusical(id);

ALTER TABLE ONLY bloqueia
    ADD CONSTRAINT bloqueia_login_bloqueado_fkey FOREIGN KEY (login_bloqueado) REFERENCES pessoa(login) ON DELETE CASCADE;

ALTER TABLE ONLY bloqueia
    ADD CONSTRAINT bloqueia_login_bloqueador_fkey FOREIGN KEY (login_bloqueador) REFERENCES pessoa(login) ON DELETE CASCADE;

ALTER TABLE ONLY cantor
    ADD CONSTRAINT cantor_id_artista_fkey FOREIGN KEY (id_artista) REFERENCES artistamusical(id);

ALTER TABLE ONLY categoria
    ADD CONSTRAINT categoria_supercategoria_fkey FOREIGN KEY (supercategoria) REFERENCES categoria(nome_categoria) ON DELETE CASCADE;

ALTER TABLE ONLY conhecido
    ADD CONSTRAINT conhecido_login_fkey FOREIGN KEY (login) REFERENCES pessoa(login);

ALTER TABLE ONLY diretor
    ADD CONSTRAINT diretor_id_artista_fkey FOREIGN KEY (id_artista) REFERENCES artistacinematografico(id) ON DELETE CASCADE;

ALTER TABLE ONLY diretor
    ADD CONSTRAINT diretor_id_filme_fkey FOREIGN KEY (id_filme) REFERENCES filme(id);

ALTER TABLE ONLY filme
    ADD CONSTRAINT filme_nome_categoria_fkey FOREIGN KEY (nome_categoria) REFERENCES categoria(nome_categoria);

ALTER TABLE ONLY musico
    ADD CONSTRAINT musico_id_banda_fkey FOREIGN KEY (id_banda) REFERENCES banda(id_artista);

ALTER TABLE ONLY musico
    ADD CONSTRAINT musico_id_cantor_fkey FOREIGN KEY (id_cantor) REFERENCES cantor(id_artista);

ALTER TABLE ONLY participacao
    ADD CONSTRAINT participacao_id_ator_fkey FOREIGN KEY (id_ator) REFERENCES artistacinematografico(id);


ALTER TABLE ONLY participacao
    ADD CONSTRAINT participacao_id_diretor_fkey FOREIGN KEY (id_diretor) REFERENCES artistacinematografico(id);


ALTER TABLE ONLY participacao
    ADD CONSTRAINT participacao_id_filme_fkey FOREIGN KEY (id_filme) REFERENCES filme(id);

ALTER TABLE ONLY registra
    ADD CONSTRAINT registra_login_registrado_fkey FOREIGN KEY (login_registrado) REFERENCES pessoa(login) ON DELETE CASCADE;

ALTER TABLE ONLY registra
    ADD CONSTRAINT registra_login_registrador_fkey FOREIGN KEY (login_registrador) REFERENCES pessoa(login) ON DELETE CASCADE;

INSERT INTO artistacinematografico (id, endereco, telefone) VALUES ('2501', 'Rua da Lua, 12', '3351-1018');
INSERT INTO artistacinematografico (id, endereco, telefone) VALUES ('5536', 'Rua do Sol, 15', '3514-5521');
INSERT INTO artistacinematografico (id, endereco, telefone) VALUES ('6689', 'Rua de Marte, 2', '3411-1519');
INSERT INTO artistacinematografico (id, endereco, telefone) VALUES ('5588', 'Rua do Ze, 21', '3214-8985');
INSERT INTO artistacinematografico (id, endereco, telefone) VALUES ('NONE', 'NONE', 'NONE');

INSERT INTO artistamusical (id, nome_artistico, "país", "gênero") VALUES (0, 'Thiago Butterfly', 'Namíbia', 'masculino');
INSERT INTO artistamusical (id, nome_artistico, "país", "gênero") VALUES (1, 'Toyololi', 'Aniworld', 'masculino');
INSERT INTO artistamusical (id, nome_artistico, "país", "gênero") VALUES (2, 'Pepsi Alien', 'Barretolandia', 'masculino');
INSERT INTO artistamusical (id, nome_artistico, "país", "gênero") VALUES (3, 'Doutor Barbeiro', 'Disney', 'masculino');
INSERT INTO artistamusical (id, nome_artistico, "país", "gênero") VALUES (4, 'bill plays', 'Twitch', 'masculino');
INSERT INTO artistamusical (id, nome_artistico, "país", "gênero") VALUES (5, 'Huewertin', 'Sertao', 'masculino');
INSERT INTO artistamusical (id, nome_artistico, "país", "gênero") VALUES (6, 'Eliheader', 'Piraquara', 'masculino');
INSERT INTO artistamusical (id, nome_artistico, "país", "gênero") VALUES (9999, 'NONE', 'NONE', 'NONE');

INSERT INTO ator (id_artista, id_filme) VALUES ('2501', '45451');
INSERT INTO ator (id_artista, id_filme) VALUES ('5536', '45451');
INSERT INTO ator (id_artista, id_filme) VALUES ('6689', '45451');

INSERT INTO banda (id_artista) VALUES (3);
INSERT INTO banda (id_artista) VALUES (5);
INSERT INTO banda (id_artista) VALUES (6);
INSERT INTO banda (id_artista) VALUES (9999);

INSERT INTO bloqueia (login_bloqueador, login_bloqueado, motivo_spam, motivo_abusivo, motivo_pessoal, motivo_outros) VALUES ('pepsitwist@alien.universe', 'tbdc@uol.com.br', false, true, false, NULL);
INSERT INTO bloqueia (login_bloqueador, login_bloqueado, motivo_spam, motivo_abusivo, motivo_pessoal, motivo_outros) VALUES ('tbdc@uol.com.br', 'PoncioJr69', true, false, false, NULL);
INSERT INTO bloqueia (login_bloqueador, login_bloqueado, motivo_spam, motivo_abusivo, motivo_pessoal, motivo_outros) VALUES ('toyomano@niconico.co.jp', 'PoncioJr69', true, false, false, NULL);
INSERT INTO bloqueia (login_bloqueador, login_bloqueado, motivo_spam, motivo_abusivo, motivo_pessoal, motivo_outros) VALUES ('guantagamera@brturbo.com.br', 'PoncioJr69', true, false, false, NULL);
INSERT INTO bloqueia (login_bloqueador, login_bloqueado, motivo_spam, motivo_abusivo, motivo_pessoal, motivo_outros) VALUES ('Robcru45', 'PoncioJr69', true, false, false, NULL);
INSERT INTO bloqueia (login_bloqueador, login_bloqueado, motivo_spam, motivo_abusivo, motivo_pessoal, motivo_outros) VALUES ('rafaiene24', 'PoncioJr69', false, false, true, 'Me xingou');

INSERT INTO cantor (id_artista) VALUES (0);
INSERT INTO cantor (id_artista) VALUES (3);
INSERT INTO cantor (id_artista) VALUES (4);
INSERT INTO cantor (id_artista) VALUES (9999);

INSERT INTO categoria (nome_categoria, supercategoria) VALUES ('NONE', 'NONE');
INSERT INTO categoria (nome_categoria, supercategoria) VALUES ('Suspense', 'NONE');
INSERT INTO categoria (nome_categoria, supercategoria) VALUES ('Drama', 'NONE');
INSERT INTO categoria (nome_categoria, supercategoria) VALUES ('Acao', 'NONE');
INSERT INTO categoria (nome_categoria, supercategoria) VALUES ('Historico', 'NONE');
INSERT INTO categoria (nome_categoria, supercategoria) VALUES ('Terror', 'Suspense');
INSERT INTO categoria (nome_categoria, supercategoria) VALUES ('Comédia', 'Drama');
INSERT INTO categoria (nome_categoria, supercategoria) VALUES ('Tragédia', 'Drama');
INSERT INTO categoria (nome_categoria, supercategoria) VALUES ('Perseguicao Policial', 'Acao');
INSERT INTO categoria (nome_categoria, supercategoria) VALUES ('Documentario', 'Historico');

INSERT INTO conhecido (login) VALUES ('pepsitwist@alien.universe');
INSERT INTO conhecido (login) VALUES ('rafaiene24');
INSERT INTO conhecido (login) VALUES ('guantagamera@brturbo.com.br');
INSERT INTO conhecido (login) VALUES ('toyomano@niconico.co.jp');
INSERT INTO conhecido (login) VALUES ('tbdc@uol.com.br');

INSERT INTO diretor (id_artista, id_filme) VALUES ('5588', '45451');
INSERT INTO diretor (id_artista, id_filme) VALUES ('5588', '12345');
INSERT INTO diretor (id_artista, id_filme) VALUES ('5588', '54321');

INSERT INTO filme (id, nome, data_de_lancamento, nome_categoria) VALUES ('12345', 'A morte do Defunto', '1986-04-01', 'Terror');
INSERT INTO filme (id, nome, data_de_lancamento, nome_categoria) VALUES ('54321', 'O Rio sem Peixes', '1999-12-07', 'Perseguicao Policial');
INSERT INTO filme (id, nome, data_de_lancamento, nome_categoria) VALUES ('45451', 'O Euler Perdido', '2012-10-15', 'Documentario');

INSERT INTO musico (nome_real, estilo_musical, data_de_nascimento, id_cantor, id_banda) VALUES ('Rafael Gama', 'Musica Caipira', '1997-06-07 00:00:00', 3, 9999);
INSERT INTO musico (nome_real, estilo_musical, data_de_nascimento, id_cantor, id_banda) VALUES ('Thiago Oliveira', 'Eletrofunk', '1997-02-02 00:00:00', 0, 9999);
INSERT INTO musico (nome_real, estilo_musical, data_de_nascimento, id_cantor, id_banda) VALUES ('Willian Lima', 'Musica Classica', '1997-08-01 00:00:00', 4, 9999);

INSERT INTO participacao (id_ator, id_filme, id_diretor) VALUES ('2501', '12345', 'NONE');
INSERT INTO participacao (id_ator, id_filme, id_diretor) VALUES ('5536', '54321', 'NONE');
INSERT INTO participacao (id_ator, id_filme, id_diretor) VALUES ('NONE', '45451', '5588');

INSERT INTO pessoa (cidade_natal, nome_completo, login) VALUES ('Piraquara', 'Thiago Bispo', 'tbdc@uol.com.br');
INSERT INTO pessoa (cidade_natal, nome_completo, login) VALUES ('Jundiaí', 'Toyomito', 'toyomano@niconico.co.jp');
INSERT INTO pessoa (cidade_natal, nome_completo, login) VALUES ('Quixeramobim', 'Rafael Gama', 'guantagamera@brturbo.com.br');
INSERT INTO pessoa (cidade_natal, nome_completo, login) VALUES ('Istambul', 'Lucas Amin', 'pepsitwist@alien.universe');
INSERT INTO pessoa (cidade_natal, nome_completo, login) VALUES ('Curitiba', 'Robson Cruzenato Taborda', 'Robcru45');
INSERT INTO pessoa (cidade_natal, nome_completo, login) VALUES ('Rolandia', 'Rafaello Gana Pallonge', 'rafaiene24');
INSERT INTO pessoa (cidade_natal, nome_completo, login) VALUES ('Jaqueira do Norte', 'Feliponcio Fagundes Junior', 'PoncioJr69');

INSERT INTO registra (login_registrador, login_registrado) VALUES ('tbdc@uol.com.br', 'toyomano@niconico.co.jp');
INSERT INTO registra (login_registrador, login_registrado) VALUES ('toyomano@niconico.co.jp', 'tbdc@uol.com.br');
INSERT INTO registra (login_registrador, login_registrado) VALUES ('tbdc@uol.com.br', 'guantagamera@brturbo.com.br');
INSERT INTO registra (login_registrador, login_registrado) VALUES ('Robcru45', 'rafaiene24');
INSERT INTO registra (login_registrador, login_registrado) VALUES ('pepsitwist@alien.universe', 'toyomano@niconico.co.jp');
INSERT INTO registra (login_registrador, login_registrado) VALUES ('toyomano@niconico.co.jp', 'Robcru45');

