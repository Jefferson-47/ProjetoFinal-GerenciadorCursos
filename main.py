"""
main.py
-------
Ponto de entrada do projeto Gerenciador de Cursos e Alunos.
Executa todas as operações CRUD e consultas via ORM SQLAlchemy,
conectando-se ao banco PostgreSQL configurado no arquivo .env
"""

from database import get_session
from crud import (
    inserir_curso, inserir_aluno, inserir_turma,
    inserir_matricula, inserir_pre_requisito,
    listar_cursos, listar_alunos, listar_turmas_ativas,
    atualizar_status_turma, atualizar_nota_matricula,
    remover_matricula
)
from consultas import (
    consulta_alunos_matriculados,
    consulta_alunos_aprovados,
    consulta_total_alunos_por_curso,
    consulta_todos_alunos_com_matricula,
    consulta_pre_requisitos
)


def secao(titulo: str):
    print(f"\n{'=' * 60}")
    print(f"  {titulo}")
    print(f"{'=' * 60}")


def main():
    session = get_session()

    try:
        # -------------------------------------------------------
        # PARTE 1 — INSERT (CREATE)
        # Inserção de cursos, alunos, turmas e matrículas via ORM
        # -------------------------------------------------------
        secao("PARTE 1 — INSERÇÃO DE DADOS (CREATE)")

        # Inserindo 3 cursos
        inserir_curso(session, "ADS", "Análise e Desenvolvimento de Sistemas", 2400,
                      "Curso focado em desenvolvimento de software")
        inserir_curso(session, "BD",  "Banco de Dados", 1800,
                      "Modelagem e administração de dados")
        inserir_curso(session, "ENG", "Engenharia de Software", 3000,
                      "Projetos e processos de software")

        # Inserindo 4 alunos
        inserir_aluno(session, "2023001", "Ana Silva",   "ana@email.com")
        inserir_aluno(session, "2023002", "Bruno Costa", "bruno@email.com")
        inserir_aluno(session, "2023003", "Carla Souza", "carla@email.com")
        inserir_aluno(session, "2023004", "Diego Lima",  "diego@email.com")  # sem matrícula

        # Inserindo turmas
        t1 = inserir_turma(session, "ADS", "2024.1", 30, "Seg/Qua 19h", "Ativa",     "Sala 101")
        t2 = inserir_turma(session, "BD",  "2024.1", 25, "Ter/Qui 18h", "Ativa",     "Sala 202")
        t3 = inserir_turma(session, "ENG", "2024.1", 20, "Sex 14h",     "Planejada", "Sala 303")

        # Inserindo pré-requisitos
        inserir_pre_requisito(session, "ENG", "ADS")
        inserir_pre_requisito(session, "BD",  "ADS")
        inserir_pre_requisito(session, "ENG", "BD")

        # Inserindo matrículas com notas
        m1 = inserir_matricula(session, "2023001", t1.id_turma, nota=8.5, frequencia=85.5, situacao="Aprovado")
        m2 = inserir_matricula(session, "2023002", t2.id_turma, nota=7.2, frequencia=78.0, situacao="Aprovado")
        m3 = inserir_matricula(session, "2023003", t1.id_turma, nota=5.0, frequencia=60.0, situacao="Reprovado")

        # -------------------------------------------------------
        # PARTE 2 — READ (Listagem com ordenação e paginação)
        # -------------------------------------------------------
        secao("PARTE 2 — LISTAGEM DE DADOS (READ)")

        listar_cursos(session)
        listar_alunos(session, limite=10, offset=0)
        listar_turmas_ativas(session)

        # -------------------------------------------------------
        # PARTE 3 — UPDATE (Atualização de registros)
        # -------------------------------------------------------
        secao("PARTE 3 — ATUALIZAÇÃO DE DADOS (UPDATE)")

        # Encerra a turma 3 (de Planejada → Encerrada)
        atualizar_status_turma(session, t3.id_turma, "Encerrada")

        # Atualiza nota da matrícula 3 (Carla: reprovada → aprovada)
        atualizar_nota_matricula(session, m3.id_matricula, nova_nota=7.5, nova_situacao="Aprovado")

        # -------------------------------------------------------
        # PARTE 4 — DELETE (Remoção respeitando integridade)
        # -------------------------------------------------------
        secao("PARTE 4 — REMOÇÃO DE DADOS (DELETE)")

        # Insere uma matrícula extra apenas para demonstrar o DELETE
        m_temp = inserir_matricula(session, "2023002", t1.id_turma, nota=6.0, frequencia=55.0, situacao="Reprovado")
        remover_matricula(session, m_temp.id_matricula)

        # -------------------------------------------------------
        # PARTE 5 — CONSULTAS COM RELACIONAMENTO (JOIN via ORM)
        # -------------------------------------------------------
        secao("PARTE 5 — CONSULTAS COM RELACIONAMENTO")

        consulta_alunos_matriculados(session)
        consulta_alunos_aprovados(session)
        consulta_total_alunos_por_curso(session)
        consulta_todos_alunos_com_matricula(session)
        consulta_pre_requisitos(session)

        print("\n" + "=" * 60)
        print("  Todas as operações concluídas com sucesso!")
        print("=" * 60)

    except Exception as e:
        session.rollback()
        print(f"\n[ERRO] {e}")
        raise

    finally:
        session.close()


if __name__ == "__main__":
    main()
