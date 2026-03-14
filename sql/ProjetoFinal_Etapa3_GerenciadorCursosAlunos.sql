-- =====================================================
-- PROJETO FINAL - ETAPA 3
-- Gerenciador de Cursos e Alunos
-- =====================================================

-- =========================
-- CRIAÇÃO DAS TABELAS
-- =========================

CREATE TABLE curso (
    codigo_curso VARCHAR(10) PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    carga_horaria INTEGER NOT NULL,
    ementa TEXT
);

CREATE TABLE aluno (
    matricula_aluno VARCHAR(15) PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    email VARCHAR(100) NOT NULL
);

CREATE TABLE turma (
    id_turma SERIAL PRIMARY KEY,
    codigo_curso VARCHAR(10) NOT NULL,
    semestre VARCHAR(10) NOT NULL,
    horarios VARCHAR(50),
    vagas_maximas INTEGER NOT NULL,
    status_turma VARCHAR(20),
    local VARCHAR(50),
    CONSTRAINT fk_turma_curso
        FOREIGN KEY (codigo_curso)
        REFERENCES curso (codigo_curso)
);

CREATE TABLE pre_requisito (
    id_pre_requisito SERIAL PRIMARY KEY,
    codigo_curso VARCHAR(10) NOT NULL,
    codigo_curso_requisito VARCHAR(10) NOT NULL,
    CONSTRAINT fk_pre_req_curso
        FOREIGN KEY (codigo_curso)
        REFERENCES curso (codigo_curso),
    CONSTRAINT fk_pre_req_curso_req
        FOREIGN KEY (codigo_curso_requisito)
        REFERENCES curso (codigo_curso)
);

CREATE TABLE matricula (
    id_matricula SERIAL PRIMARY KEY,
    matricula_aluno VARCHAR(15) NOT NULL,
    id_turma INTEGER NOT NULL,
    frequencia NUMERIC(5,2),
    situacao VARCHAR(20),
    nota NUMERIC(4,2),
    CONSTRAINT fk_matricula_aluno
        FOREIGN KEY (matricula_aluno)
        REFERENCES aluno (matricula_aluno),
    CONSTRAINT fk_matricula_turma
        FOREIGN KEY (id_turma)
        REFERENCES turma (id_turma)
);

-- =====================================================
-- ETAPA 3 - PROJETO FINAL
-- CARGA DE DADOS (INSERTs)
-- =====================================================

-- Inserindo Cursos
INSERT INTO curso (codigo_curso, nome, carga_horaria, ementa) VALUES
('ADS', 'Análise e Desenvolvimento de Sistemas', 2400, 'Curso focado em desenvolvimento de software'),
('BD', 'Banco de Dados', 1800, 'Modelagem e administração de dados'),
('ENG', 'Engenharia de Software', 3000, 'Projetos e processos de software');

-- Inserindo Alunos
INSERT INTO aluno (matricula_aluno, nome, email) VALUES
('2023001', 'Ana Silva', 'ana@email.com'),
('2023002', 'Bruno Costa', 'bruno@email.com'),
('2023003', 'Carla Souza', 'carla@email.com'),
('2023004', 'Diego Lima', 'diego@email.com'); -- Aluno sem matrícula para testar o LEFT JOIN

-- Inserindo Turmas
INSERT INTO turma (codigo_curso, semestre, horarios, vagas_maximas, status_turma, local) VALUES
('ADS', '2024.1', 'Seg/Qua 19h', 30, 'Ativa', 'Sala 101'),
('BD', '2024.1', 'Ter/Qui 18h', 25, 'Ativa', 'Sala 202'),
('ENG', '2024.1', 'Sex 14h', 20, 'Planejada', 'Sala 303');

-- Inserindo Pré-requisitos
INSERT INTO pre_requisito (codigo_curso, codigo_curso_requisito) VALUES
('ENG', 'ADS'),
('BD', 'ADS'),
('ENG', 'BD');

-- Inserindo Matrículas
INSERT INTO matricula (matricula_aluno, id_turma, frequencia, situacao, nota) VALUES
('2023001', 1, 85.5, 'Aprovado', 8.5),
('2023002', 2, 78.0, 'Aprovado', 7.2),
('2023003', 1, 60.0, 'Reprovado', 5.0);

-- =====================================================
-- CONSULTAS (SELECT)
-- =====================================================

-- Consulta 1: Listar alunos matriculados com seus nomes, nomes dos cursos e semestre (INNER JOIN entre 4 tabelas)
SELECT 
    a.nome AS nome_aluno, 
    c.nome AS nome_curso, 
    t.semestre AS semestre_turma
FROM matricula AS m
JOIN aluno AS a ON m.matricula_aluno = a.matricula_aluno
JOIN turma AS t ON m.id_turma = t.id_turma
JOIN curso AS c ON t.codigo_curso = c.codigo_curso;

-- Consulta 2: Listar cursos e suas respectivas turmas filtrando apenas turmas 'Ativas' (JOIN + WHERE)
SELECT 
    c.nome AS nome_curso, 
    t.semestre, 
    t.status_turma
FROM curso AS c
JOIN turma AS t ON c.codigo_curso = t.codigo_curso
WHERE t.status_turma = 'Ativa';

-- Consulta 3: Mostrar apenas alunos aprovados com nota superior a 7.0 (Filtro WHERE em campos numéricos e texto)
SELECT 
    a.nome AS nome_aluno, 
    m.nota AS nota_final
FROM matricula AS m
JOIN aluno AS a ON m.matricula_aluno = a.matricula_aluno
WHERE m.situacao = 'Aprovado' AND m.nota >= 7.0;

-- Consulta 4: Listar todos os alunos da base e seus IDs de matrícula, incluindo quem não está matriculado (LEFT JOIN)
SELECT 
    a.nome AS nome_aluno, 
    m.id_matricula AS protocolo
FROM aluno AS a
LEFT JOIN matricula AS m ON a.matricula_aluno = m.matricula_aluno;

-- Consulta 5: Mostrar os pré-requisitos de cada curso relacionando a tabela curso consigo mesma (Auto-referência via JOIN)
SELECT 
    c.nome AS curso_principal, 
    cr.nome AS curso_requisito
FROM pre_requisito AS p
JOIN curso AS c ON p.codigo_curso = c.codigo_curso
JOIN curso AS cr ON p.codigo_curso_requisito = cr.codigo_curso;