"""
crud.py
-------
Operações CRUD (Create, Read, Update, Delete) via ORM SQLAlchemy.
Nenhuma query SQL manual é utilizada nestas funções.
"""

from sqlalchemy.orm import Session
from models import Curso, Aluno, Turma, PreRequisito, Matricula


# ===========================================================
# CREATE — Inserção de registros
# ===========================================================

def inserir_curso(session: Session, codigo: str, nome: str, carga_horaria: int, ementa: str = None):
    """Insere um novo curso no banco de dados."""
    curso = Curso(
        codigo_curso=codigo,
        nome=nome,
        carga_horaria=carga_horaria,
        ementa=ementa
    )
    session.add(curso)
    session.commit()
    session.refresh(curso)
    print(f"  [INSERT] Curso inserido: {curso}")
    return curso


def inserir_aluno(session: Session, matricula: str, nome: str, email: str):
    """Insere um novo aluno no banco de dados."""
    aluno = Aluno(matricula_aluno=matricula, nome=nome, email=email)
    session.add(aluno)
    session.commit()
    session.refresh(aluno)
    print(f"  [INSERT] Aluno inserido: {aluno}")
    return aluno


def inserir_turma(session: Session, codigo_curso: str, semestre: str, vagas: int,
                  horarios: str = None, status: str = "Planejada", local: str = None):
    """Insere uma nova turma vinculada a um curso."""
    turma = Turma(
        codigo_curso=codigo_curso,
        semestre=semestre,
        vagas_maximas=vagas,
        horarios=horarios,
        status_turma=status,
        local=local
    )
    session.add(turma)
    session.commit()
    session.refresh(turma)
    print(f"  [INSERT] Turma inserida: {turma}")
    return turma


def inserir_matricula(session: Session, matricula_aluno: str, id_turma: int,
                      nota: float = None, frequencia: float = None, situacao: str = "Matriculado"):
    """Insere uma matrícula de um aluno em uma turma."""
    matricula = Matricula(
        matricula_aluno=matricula_aluno,
        id_turma=id_turma,
        nota=nota,
        frequencia=frequencia,
        situacao=situacao
    )
    session.add(matricula)
    session.commit()
    session.refresh(matricula)
    print(f"  [INSERT] Matrícula inserida: {matricula}")
    return matricula


def inserir_pre_requisito(session: Session, codigo_curso: str, codigo_requisito: str):
    """Define um pré-requisito entre dois cursos."""
    pre_req = PreRequisito(
        codigo_curso=codigo_curso,
        codigo_curso_requisito=codigo_requisito
    )
    session.add(pre_req)
    session.commit()
    print(f"  [INSERT] Pré-requisito: '{codigo_requisito}' é requisito de '{codigo_curso}'")
    return pre_req


# ===========================================================
# READ — Listagem de registros
# ===========================================================

def listar_cursos(session: Session):
    """Lista todos os cursos ordenados pelo nome."""
    cursos = session.query(Curso).order_by(Curso.nome).all()
    print(f"\n  [READ] Total de cursos: {len(cursos)}")
    for c in cursos:
        print(f"    → {c.codigo_curso} | {c.nome} | {c.carga_horaria}h")
    return cursos


def listar_alunos(session: Session, limite: int = 10, offset: int = 0):
    """Lista alunos com paginação simples (limite + offset)."""
    alunos = session.query(Aluno).order_by(Aluno.nome).limit(limite).offset(offset).all()
    print(f"\n  [READ] Alunos (página offset={offset}, limite={limite}):")
    for a in alunos:
        print(f"    → {a.matricula_aluno} | {a.nome} | {a.email}")
    return alunos


def listar_turmas_ativas(session: Session):
    """Lista apenas turmas com status 'Ativa'."""
    turmas = session.query(Turma).filter(Turma.status_turma == "Ativa").order_by(Turma.semestre).all()
    print(f"\n  [READ] Turmas ativas: {len(turmas)}")
    for t in turmas:
        print(f"    → Turma {t.id_turma} | Curso: {t.codigo_curso} | {t.semestre} | {t.local}")
    return turmas


# ===========================================================
# UPDATE — Atualização de registros
# ===========================================================

def atualizar_status_turma(session: Session, id_turma: int, novo_status: str):
    """Atualiza o status de uma turma (ex.: Ativa → Encerrada)."""
    turma = session.query(Turma).filter(Turma.id_turma == id_turma).first()
    if turma:
        status_anterior = turma.status_turma
        turma.status_turma = novo_status
        session.commit()
        print(f"  [UPDATE] Turma {id_turma}: '{status_anterior}' → '{novo_status}'")
    else:
        print(f"  [UPDATE] Turma {id_turma} não encontrada.")
    return turma


def atualizar_nota_matricula(session: Session, id_matricula: int, nova_nota: float, nova_situacao: str):
    """Atualiza nota e situação de uma matrícula existente."""
    matricula = session.query(Matricula).filter(Matricula.id_matricula == id_matricula).first()
    if matricula:
        matricula.nota = nova_nota
        matricula.situacao = nova_situacao
        session.commit()
        print(f"  [UPDATE] Matrícula {id_matricula}: nota={nova_nota}, situacao='{nova_situacao}'")
    else:
        print(f"  [UPDATE] Matrícula {id_matricula} não encontrada.")
    return matricula


# ===========================================================
# DELETE — Remoção de registros
# ===========================================================

def remover_aluno(session: Session, matricula_aluno: str):
    """
    Remove um aluno pelo número de matrícula.
    As matrículas vinculadas são removidas automaticamente
    pelo CASCADE definido no modelo.
    """
    aluno = session.query(Aluno).filter(Aluno.matricula_aluno == matricula_aluno).first()
    if aluno:
        session.delete(aluno)
        session.commit()
        print(f"  [DELETE] Aluno '{aluno.nome}' removido (e suas matrículas por CASCADE).")
    else:
        print(f"  [DELETE] Aluno '{matricula_aluno}' não encontrado.")


def remover_matricula(session: Session, id_matricula: int):
    """Remove uma matrícula específica pelo ID."""
    matricula = session.query(Matricula).filter(Matricula.id_matricula == id_matricula).first()
    if matricula:
        session.delete(matricula)
        session.commit()
        print(f"  [DELETE] Matrícula ID {id_matricula} removida.")
    else:
        print(f"  [DELETE] Matrícula ID {id_matricula} não encontrada.")
