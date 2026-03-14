# Gerenciador de Cursos e Alunos — Etapa 7 (ORM)

**Instituição:** Universidade Federal do Cariri  
**Curso:** Análise e Desenvolvimento de Sistemas  
**Disciplina:** Projeto de Banco de Dados  
**ORM utilizado:** SQLAlchemy 2.0 (Python)  
**Banco de Dados:** PostgreSQL

---

## Estrutura do Projeto

```
gerenciador_cursos/
├── .env.example       # Modelo de variáveis de ambiente
├── requirements.txt   # Dependências Python
├── database.py        # Configuração da conexão com o PostgreSQL
├── models.py          # Mapeamento ORM (classes ↔ tabelas)
├── crud.py            # Operações CRUD via ORM
├── consultas.py       # Consultas com relacionamentos (JOIN via ORM)
└── main.py            # Ponto de entrada — executa tudo
```

---

## Pré-requisitos

- Python 3.10 ou superior
- PostgreSQL instalado e em execução
- Banco de dados criado com o schema das etapas anteriores

---

## Como configurar

### 1. Instalar dependências

```bash
pip install -r requirements.txt
```

### 2. Configurar variáveis de ambiente

Copie o arquivo de exemplo e preencha com suas credenciais:

```bash
cp .env.example .env
```

Edite o arquivo `.env`:

```
DB_HOST=localhost
DB_PORT=5432
DB_NAME=gerenciador_cursos
DB_USER=postgres
DB_PASSWORD=sua_senha_aqui
```

### 3. Preparar o banco

Certifique-se de que o banco já foi criado com o script DDL das etapas anteriores.  
O banco deve estar **vazio** antes de rodar o projeto pela primeira vez (o `main.py` irá inserir os dados de teste).

---

## Como executar

```bash
python main.py
```

---

## O que o projeto faz

### Mapeamento ORM (`models.py`)
Cada tabela do banco vira uma classe Python com seus relacionamentos:

| Classe         | Tabela          | Relacionamentos                        |
|----------------|-----------------|----------------------------------------|
| `Curso`        | `curso`         | 1-N com Turma, 1-N com PreRequisito    |
| `Aluno`        | `aluno`         | 1-N com Matricula                      |
| `Turma`        | `turma`         | N-1 com Curso, 1-N com Matricula       |
| `PreRequisito` | `pre_requisito` | N-1 com Curso (duplo)                  |
| `Matricula`    | `matricula`     | N-1 com Aluno, N-1 com Turma           |

### CRUD (`crud.py`)
- **CREATE:** insere cursos, alunos, turmas, matrículas e pré-requisitos
- **READ:** lista com ordenação e paginação (limit/offset)
- **UPDATE:** atualiza status de turma e nota/situação de matrícula
- **DELETE:** remove matrícula e aluno (com CASCADE automático)

### Consultas com JOIN (`consultas.py`)
1. Alunos matriculados com nome do curso e semestre (JOIN 4 tabelas)
2. Alunos aprovados com nota ≥ 7 (filtro em tabela relacionada)
3. Total de alunos por curso (COUNT + GROUP BY via ORM)
4. Todos os alunos incluindo sem matrícula (LEFT JOIN / outerjoin)
5. Pré-requisitos dos cursos (auto-referência via ORM)

---

## Exemplo de saída

```
============================================================
  PARTE 1 — INSERÇÃO DE DADOS (CREATE)
============================================================
  [INSERT] Curso inserido: <Curso(codigo='ADS', nome='Análise e Desenvolvimento de Sistemas')>
  [INSERT] Aluno inserido: <Aluno(matricula='2023001', nome='Ana Silva')>
  ...

============================================================
  PARTE 5 — CONSULTAS COM RELACIONAMENTO
============================================================
  [CONSULTA 1] Alunos matriculados com curso e turma:
  Nome do Aluno        Curso                                    Semestre   Nota   Situação
  ------------------------------------------------------------------------------------------
  Ana Silva            Análise e Desenvolvimento de Sistemas    2024.1     8.5    Aprovado
  Bruno Costa          Banco de Dados                           2024.1     7.2    Aprovado
  Carla Souza          Análise e Desenvolvimento de Sistemas    2024.1     7.5    Aprovado
```

---

## Observações

- Nenhuma query SQL manual foi utilizada no CRUD e consultas principais.
- Os relacionamentos são carregados via `joinedload` para eficiência.
- O arquivo `.env` **não deve ser versionado** (adicione ao `.gitignore`).
