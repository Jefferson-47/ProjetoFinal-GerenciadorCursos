-- =====================================================
-- PROJETO FINAL - ETAPA 5
-- Gerenciador de Cursos e Alunos
-- Recursos Avançados PostgreSQL
-- =====================================================


-- ===============================
-- VIEW
-- ===============================
-- Finalidade:
-- Facilitar a consulta frequente de alunos matriculados
-- com informações do curso e da turma.

CREATE OR REPLACE VIEW vw_alunos_matriculados AS
SELECT
    a.nome              AS nome_aluno,
    a.email             AS email_aluno,
    c.nome              AS nome_curso,
    t.semestre          AS semestre,
    m.nota              AS nota,
    m.situacao          AS situacao
FROM matricula m
JOIN aluno a   ON m.matricula_aluno = a.matricula_aluno
JOIN turma t   ON m.id_turma = t.id_turma
JOIN curso c   ON t.codigo_curso = c.codigo_curso;



-- ===============================
-- VIEW MATERIALIZADA
-- ===============================
-- Finalidade:
-- Gerar relatório com média de notas por curso,
-- quantidade de alunos e desempenho geral.
-- Pode melhorar desempenho em consultas frequentes.

CREATE MATERIALIZED VIEW mv_relatorio_media_curso AS
SELECT
    c.nome AS nome_curso,
    COUNT(m.id_matricula) AS total_alunos,
    ROUND(AVG(m.nota), 2) AS media_notas
FROM curso c
JOIN turma t ON c.codigo_curso = t.codigo_curso
JOIN matricula m ON t.id_turma = m.id_turma
GROUP BY c.nome;



-- ===============================
-- TRIGGERS
-- ===============================

-- -----------------------------------------------------
-- TABELA AUXILIAR DE LOG
-- -----------------------------------------------------
-- Finalidade:
-- Registrar inserções de matrícula no sistema.

CREATE TABLE IF NOT EXISTS log_matricula (
    id_log SERIAL PRIMARY KEY,
    id_matricula INTEGER,
    data_operacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    operacao VARCHAR(20)
);


-- -----------------------------------------------------
-- TRIGGER BEFORE
-- -----------------------------------------------------
-- Finalidade:
-- Definir automaticamente a situação do aluno
-- com base na nota inserida ou atualizada.

CREATE OR REPLACE FUNCTION fn_definir_situacao()
RETURNS TRIGGER AS $$
BEGIN
    IF NEW.nota >= 7 THEN
        NEW.situacao := 'Aprovado';
    ELSIF NEW.nota < 7 THEN
        NEW.situacao := 'Reprovado';
    END IF;

    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trg_before_matricula
BEFORE INSERT OR UPDATE ON matricula
FOR EACH ROW
WHEN (NEW.nota IS NOT NULL)
EXECUTE FUNCTION fn_definir_situacao();



-- -----------------------------------------------------
-- TRIGGER AFTER
-- -----------------------------------------------------
-- Finalidade:
-- Registrar log após inserção de nova matrícula.

CREATE OR REPLACE FUNCTION fn_log_matricula()
RETURNS TRIGGER AS $$
BEGIN
    INSERT INTO log_matricula (id_matricula, operacao)
    VALUES (NEW.id_matricula, 'INSERT');

    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trg_after_matricula
AFTER INSERT ON matricula
FOR EACH ROW
EXECUTE FUNCTION fn_log_matricula();



-- ===============================
-- PROCEDURE
-- ===============================
-- Finalidade:
-- Encerrar automaticamente turmas ativas
-- alterando o status para 'Encerrada'.

CREATE OR REPLACE PROCEDURE pr_encerrar_turmas()
LANGUAGE plpgsql
AS $$
BEGIN
    UPDATE turma
    SET status_turma = 'Encerrada'
    WHERE status_turma = 'Ativa';
END;
$$;


-- =====================================================
-- FIM DO SCRIPT - ETAPA 5
-- =====================================================