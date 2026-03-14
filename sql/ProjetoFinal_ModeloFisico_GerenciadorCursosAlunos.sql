CREATE TABLE curso (
    codigo_curso VARCHAR(10) PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    carga_horaria INTEGER NOT NULL
);

CREATE TABLE aluno (
    matricula_aluno VARCHAR(15) PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    email VARCHAR(100) NOT NULL UNIQUE
);

CREATE TABLE turma (
    id_turma SERIAL PRIMARY KEY,
    codigo_curso VARCHAR(10) NOT NULL,
    semestre VARCHAR(10) NOT NULL,
    vagas INTEGER NOT NULL,
    CONSTRAINT fk_turma_curso
        FOREIGN KEY (codigo_curso)
        REFERENCES curso (codigo_curso)
        ON DELETE RESTRICT
        ON UPDATE CASCADE
);

CREATE TABLE pre_requisito (
    codigo_curso VARCHAR(10) NOT NULL,
    codigo_curso_pre_requisito VARCHAR(10) NOT NULL,
    CONSTRAINT pk_pre_requisito
        PRIMARY KEY (codigo_curso, codigo_curso_pre_requisito),
    CONSTRAINT fk_pre_requisito_curso
        FOREIGN KEY (codigo_curso)
        REFERENCES curso (codigo_curso)
        ON DELETE RESTRICT
        ON UPDATE CASCADE,
    CONSTRAINT fk_pre_requisito_curso_req
        FOREIGN KEY (codigo_curso_pre_requisito)
        REFERENCES curso (codigo_curso)
        ON DELETE RESTRICT
        ON UPDATE CASCADE
);

CREATE TABLE matricula (
    id_matricula SERIAL PRIMARY KEY,
    matricula_aluno VARCHAR(15) NOT NULL,
    id_turma INTEGER NOT NULL,
    nota NUMERIC(4,2),
    frequencia NUMERIC(5,2),
    CONSTRAINT fk_matricula_aluno
        FOREIGN KEY (matricula_aluno)
        REFERENCES aluno (matricula_aluno)
        ON DELETE CASCADE
        ON UPDATE CASCADE,
    CONSTRAINT fk_matricula_turma
        FOREIGN KEY (id_turma)
        REFERENCES turma (id_turma)
        ON DELETE CASCADE
        ON UPDATE CASCADE
);
