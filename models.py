"""
models.py
---------
Mapeamento ORM das tabelas do Gerenciador de Cursos e Alunos.
Cada classe representa uma tabela do banco de dados PostgreSQL.

Tabelas mapeadas:
    - Curso
    - Aluno
    - Turma
    - PreRequisito
    - Matricula
"""

from sqlalchemy import (
    Column, String, Integer, Numeric, Text,
    ForeignKey, CheckConstraint, UniqueConstraint
)
from sqlalchemy.orm import relationship
from database import Base


# ===========================================================
# ENTIDADE: Curso
# Representa a tabela 'curso' do banco de dados.
# Relacionamentos:
#   - 1 Curso possui N Turmas (OneToMany)
#   - 1 Curso pode ter N Pré-Requisitos (OneToMany)
# ===========================================================
class Curso(Base):
    __tablename__ = "curso"

    codigo_curso  = Column(String(10), primary_key=True)
    nome          = Column(String(100), nullable=False)
    carga_horaria = Column(Integer, nullable=False)
    ementa        = Column(Text)

    # Relacionamento 1-N: um curso possui várias turmas
    turmas = relationship("Turma", back_populates="curso", cascade="all, delete-orphan")

    # Relacionamento 1-N: um curso pode ter vários pré-requisitos definidos
    pre_requisitos = relationship(
        "PreRequisito",
        foreign_keys="PreRequisito.codigo_curso",
        back_populates="curso"
    )

    def __repr__(self):
        return f"<Curso(codigo='{self.codigo_curso}', nome='{self.nome}')>"


# ===========================================================
# ENTIDADE: Aluno
# Representa a tabela 'aluno' do banco de dados.
# Relacionamentos:
#   - 1 Aluno possui N Matrículas (OneToMany)
# ===========================================================
class Aluno(Base):
    __tablename__ = "aluno"

    __table_args__ = (
        UniqueConstraint("email", name="uk_aluno_email"),
    )

    matricula_aluno = Column(String(15), primary_key=True)
    nome            = Column(String(100), nullable=False)
    email           = Column(String(100), nullable=False)

    # Relacionamento 1-N: um aluno pode ter várias matrículas em turmas
    matriculas = relationship("Matricula", back_populates="aluno", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Aluno(matricula='{self.matricula_aluno}', nome='{self.nome}')>"


# ===========================================================
# ENTIDADE: Turma
# Representa a tabela 'turma' do banco de dados.
# Relacionamentos:
#   - N Turmas pertencem a 1 Curso (ManyToOne)
#   - 1 Turma possui N Matrículas (OneToMany)
# ===========================================================
class Turma(Base):
    __tablename__ = "turma"

    __table_args__ = (
        CheckConstraint(
            "status_turma IN ('Ativa', 'Planejada', 'Encerrada')",
            name="ck_turma_status"
        ),
    )

    id_turma      = Column(Integer, primary_key=True, autoincrement=True)
    codigo_curso  = Column(String(10), ForeignKey("curso.codigo_curso", ondelete="RESTRICT", onupdate="CASCADE"), nullable=False)
    semestre      = Column(String(10), nullable=False)
    horarios      = Column(String(50))
    vagas_maximas = Column(Integer, nullable=False)
    status_turma  = Column(String(20), default="Planejada")
    local         = Column(String(50))

    # Relacionamento N-1: muitas turmas pertencem a um curso
    curso = relationship("Curso", back_populates="turmas")

    # Relacionamento 1-N: uma turma tem várias matrículas
    matriculas = relationship("Matricula", back_populates="turma", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Turma(id={self.id_turma}, semestre='{self.semestre}', status='{self.status_turma}')>"


# ===========================================================
# ENTIDADE: PreRequisito
# Representa a tabela 'pre_requisito' do banco de dados.
# Relacionamentos:
#   - N Pré-Requisitos referenciam 1 Curso principal (ManyToOne)
#   - N Pré-Requisitos referenciam 1 Curso requisito (ManyToOne)
# ===========================================================
class PreRequisito(Base):
    __tablename__ = "pre_requisito"

    id_pre_requisito      = Column(Integer, primary_key=True, autoincrement=True)
    codigo_curso          = Column(String(10), ForeignKey("curso.codigo_curso"), nullable=False)
    codigo_curso_requisito = Column(String(10), ForeignKey("curso.codigo_curso"), nullable=False)

    # Relacionamento N-1: referência ao curso principal
    curso = relationship("Curso", foreign_keys=[codigo_curso], back_populates="pre_requisitos")

    # Relacionamento N-1: referência ao curso que é pré-requisito
    curso_requisito = relationship("Curso", foreign_keys=[codigo_curso_requisito])

    def __repr__(self):
        return f"<PreRequisito(curso='{self.codigo_curso}', requisito='{self.codigo_curso_requisito}')>"


# ===========================================================
# ENTIDADE: Matricula
# Representa a tabela 'matricula' do banco de dados.
# Relacionamentos:
#   - N Matrículas pertencem a 1 Aluno (ManyToOne)
#   - N Matrículas pertencem a 1 Turma (ManyToOne)
# ===========================================================
class Matricula(Base):
    __tablename__ = "matricula"

    __table_args__ = (
        CheckConstraint("nota >= 0 AND nota <= 10",           name="ck_matricula_nota"),
        CheckConstraint("frequencia >= 0 AND frequencia <= 100", name="ck_matricula_frequencia"),
        CheckConstraint(
            "situacao IN ('Matriculado', 'Aprovado', 'Reprovado', 'Trancado')",
            name="ck_matricula_situacao"
        ),
    )

    id_matricula    = Column(Integer, primary_key=True, autoincrement=True)
    matricula_aluno = Column(String(15), ForeignKey("aluno.matricula_aluno", ondelete="CASCADE", onupdate="CASCADE"), nullable=False)
    id_turma        = Column(Integer,    ForeignKey("turma.id_turma",        ondelete="CASCADE", onupdate="CASCADE"), nullable=False)
    frequencia      = Column(Numeric(5, 2))
    situacao        = Column(String(20), default="Matriculado")
    nota            = Column(Numeric(4, 2))

    # Relacionamento N-1: muitas matrículas pertencem a um aluno
    aluno = relationship("Aluno", back_populates="matriculas")

    # Relacionamento N-1: muitas matrículas pertencem a uma turma
    turma = relationship("Turma", back_populates="matriculas")

    def __repr__(self):
        return f"<Matricula(id={self.id_matricula}, situacao='{self.situacao}', nota={self.nota})>"
