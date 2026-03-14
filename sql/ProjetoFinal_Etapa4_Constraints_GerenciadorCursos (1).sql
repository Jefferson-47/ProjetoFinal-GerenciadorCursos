-- =====================================================
-- PROJETO FINAL - ETAPA 4
-- Gerenciador de Cursos e Alunos
-- Disciplina: Banco de Dados
-- =====================================================

-- -----------------------------------------------------
-- 1) CHECK CONSTRAINTS
-- Objetivo: Garantir que os dados numéricos e de status 
-- sigam regras de negócio lógicas.
-- -----------------------------------------------------

-- Validação de nota (0 a 10)
ALTER TABLE matricula
ADD CONSTRAINT ck_matricula_nota
CHECK (nota >= 0 AND nota <= 10);

-- Validação de frequência (0% a 100%)
ALTER TABLE matricula
ADD CONSTRAINT ck_matricula_frequencia
CHECK (frequencia >= 0 AND frequencia <= 100);

-- Restrição de valores permitidos para o status da turma
ALTER TABLE turma
ADD CONSTRAINT ck_turma_status
CHECK (status_turma IN ('Ativa', 'Planejada', 'Encerrada'));

-- Restrição de valores para a situação do aluno na matrícula
ALTER TABLE matricula
ADD CONSTRAINT ck_matricula_situacao
CHECK (situacao IN ('Matriculado', 'Aprovado', 'Reprovado', 'Trancado'));


-- -----------------------------------------------------
-- 2) UNIQUE CONSTRAINT
-- Objetivo: Impedir duplicidade de dados sensíveis.
-- -----------------------------------------------------

-- Garante que cada e-mail no sistema seja exclusivo de um aluno
ALTER TABLE aluno
ADD CONSTRAINT uk_aluno_email
UNIQUE (email);


-- -----------------------------------------------------
-- 3) DEFAULT VALUES
-- Objetivo: Facilitar a inserção de novos registros 
-- definindo um estado inicial padrão.
-- -----------------------------------------------------

-- Define 'Planejada' como status inicial para novas turmas
ALTER TABLE turma
ALTER COLUMN status_turma SET DEFAULT 'Planejada';

-- Define 'Matriculado' como situação inicial para novas matrículas
ALTER TABLE matricula
ALTER COLUMN situacao SET DEFAULT 'Matriculado';


-- -----------------------------------------------------
-- 4) REGRAS ON DELETE / ON UPDATE
-- Objetivo: Manter a integridade referencial entre as tabelas.
-- -----------------------------------------------------

-- [FK Matrícula -> Aluno]
-- Se um aluno for removido, suas matrículas são excluídas (CASCADE)
ALTER TABLE matricula DROP CONSTRAINT fk_matricula_aluno;
ALTER TABLE matricula
ADD CONSTRAINT fk_matricula_aluno
FOREIGN KEY (matricula_aluno)
REFERENCES aluno(matricula_aluno)
ON DELETE CASCADE
ON UPDATE CASCADE;

-- [FK Matrícula -> Turma]
-- Se uma turma for removida, as matrículas vinculadas são apagadas (CASCADE)
ALTER TABLE matricula DROP CONSTRAINT fk_matricula_turma;
ALTER TABLE matricula
ADD CONSTRAINT fk_matricula_turma
FOREIGN KEY (id_turma)
REFERENCES turma(id_turma)
ON DELETE CASCADE
ON UPDATE CASCADE;

-- [FK Turma -> Curso]
-- Impede a exclusão de um curso que possua turmas cadastradas (RESTRICT)
-- para preservar o histórico acadêmico.
ALTER TABLE turma DROP CONSTRAINT fk_turma_curso;
ALTER TABLE turma
ADD CONSTRAINT fk_turma_curso
FOREIGN KEY (codigo_curso)
REFERENCES curso(codigo_curso)
ON DELETE RESTRICT
ON UPDATE CASCADE;

-- =====================================================
-- FIM DO SCRIPT - ETAPA 4
-- =====================================================