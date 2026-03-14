"""
consultas.py
------------
Consultas avançadas via ORM SQLAlchemy, equivalentes a JOINs SQL.
Demonstra: relacionamentos, filtros, ordenação e agregações.
"""

from sqlalchemy.orm import Session, joinedload
from sqlalchemy import func
from models import Aluno, Matricula, Turma, Curso, PreRequisito


# ===========================================================
# CONSULTA 1 — JOIN entre Matrícula, Aluno, Turma e Curso
# Equivalente a: SELECT aluno, curso, semestre, nota FROM matricula
#                JOIN aluno ... JOIN turma ... JOIN curso ...
# ===========================================================
def consulta_alunos_matriculados(session: Session):
    """
    Lista todos os alunos matriculados com informações
    do curso e da turma. Usa joinedload para carregar
    os relacionamentos em uma única consulta eficiente.
    """
    print("\n  [CONSULTA 1] Alunos matriculados com curso e turma:")
    print(f"  {'Nome do Aluno':<20} {'Curso':<40} {'Semestre':<10} {'Nota':<6} {'Situação'}")
    print("  " + "-" * 90)

    matriculas = (
        session.query(Matricula)
        .options(
            joinedload(Matricula.aluno),
            joinedload(Matricula.turma).joinedload(Turma.curso)
        )
        .all()
    )

    for m in matriculas:
        nome_aluno  = m.aluno.nome if m.aluno else "—"
        nome_curso  = m.turma.curso.nome if m.turma and m.turma.curso else "—"
        semestre    = m.turma.semestre if m.turma else "—"
        nota        = m.nota if m.nota is not None else "—"
        situacao    = m.situacao or "—"
        print(f"  {nome_aluno:<20} {nome_curso:<40} {semestre:<10} {str(nota):<6} {situacao}")

    return matriculas


# ===========================================================
# CONSULTA 2 — JOIN com filtro por atributo de tabela relacionada
# Equivalente a: SELECT aluno.nome, matricula.nota
#                FROM matricula JOIN aluno ...
#                WHERE matricula.situacao = 'Aprovado' AND nota >= 7
# ===========================================================
def consulta_alunos_aprovados(session: Session):
    """
    Lista apenas os alunos aprovados com nota >= 7,
    filtrando por atributo da tabela relacionada.
    """
    print("\n  [CONSULTA 2] Alunos aprovados (nota >= 7):")
    print(f"  {'Nome do Aluno':<25} {'Nota'}")
    print("  " + "-" * 35)

    resultados = (
        session.query(Aluno.nome, Matricula.nota)
        .join(Matricula, Aluno.matricula_aluno == Matricula.matricula_aluno)
        .filter(Matricula.situacao == "Aprovado", Matricula.nota >= 7)
        .order_by(Matricula.nota.desc())
        .all()
    )

    for nome, nota in resultados:
        print(f"  {nome:<25} {nota}")

    return resultados


# ===========================================================
# CONSULTA 3 — Agregação por relacionamento (COUNT + GROUP BY)
# Equivalente a: SELECT curso.nome, COUNT(matricula)
#                FROM curso JOIN turma ... JOIN matricula ...
#                GROUP BY curso.nome
# ===========================================================
def consulta_total_alunos_por_curso(session: Session):
    """
    Conta quantos alunos estão matriculados em cada curso,
    usando agregação via ORM (equivalente a COUNT + GROUP BY + JOIN).
    """
    print("\n  [CONSULTA 3] Total de alunos por curso:")
    print(f"  {'Curso':<40} {'Total Alunos'}")
    print("  " + "-" * 55)

    resultados = (
        session.query(Curso.nome, func.count(Matricula.id_matricula).label("total"))
        .join(Turma, Curso.codigo_curso == Turma.codigo_curso)
        .join(Matricula, Turma.id_turma == Matricula.id_turma)
        .group_by(Curso.nome)
        .order_by(func.count(Matricula.id_matricula).desc())
        .all()
    )

    for nome_curso, total in resultados:
        print(f"  {nome_curso:<40} {total}")

    return resultados


# ===========================================================
# CONSULTA 4 — Todos os alunos + matrículas (LEFT JOIN)
# Inclui alunos que ainda não possuem matrícula.
# ===========================================================
def consulta_todos_alunos_com_matricula(session: Session):
    """
    Lista todos os alunos, incluindo os que não têm matrícula.
    Usa outerjoin para equivaler ao LEFT JOIN do SQL.
    """
    print("\n  [CONSULTA 4] Todos os alunos (incluindo sem matrícula):")
    print(f"  {'Nome do Aluno':<25} {'ID Matrícula'}")
    print("  " + "-" * 40)

    resultados = (
        session.query(Aluno.nome, Matricula.id_matricula)
        .outerjoin(Matricula, Aluno.matricula_aluno == Matricula.matricula_aluno)
        .order_by(Aluno.nome)
        .all()
    )

    for nome, id_mat in resultados:
        protocolo = str(id_mat) if id_mat else "Sem matrícula"
        print(f"  {nome:<25} {protocolo}")

    return resultados


# ===========================================================
# CONSULTA 5 — Auto-referência: pré-requisitos dos cursos
# Equivalente a: SELECT c.nome, cr.nome FROM pre_requisito
#                JOIN curso c ... JOIN curso cr ...
# ===========================================================
def consulta_pre_requisitos(session: Session):
    """
    Exibe os pré-requisitos de cada curso usando
    auto-referência na tabela Curso via ORM.
    """
    print("\n  [CONSULTA 5] Pré-requisitos por curso:")
    print(f"  {'Curso Principal':<35} {'Pré-Requisito'}")
    print("  " + "-" * 65)

    CursoReq = Curso.__table__.alias("curso_req")

    pre_reqs = (
        session.query(PreRequisito)
        .options(
            joinedload(PreRequisito.curso),
            joinedload(PreRequisito.curso_requisito)
        )
        .all()
    )

    for pr in pre_reqs:
        nome_principal = pr.curso.nome if pr.curso else pr.codigo_curso
        nome_requisito = pr.curso_requisito.nome if pr.curso_requisito else pr.codigo_curso_requisito
        print(f"  {nome_principal:<35} {nome_requisito}")

    return pre_reqs
