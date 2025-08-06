# DayTask

## Sobre o Projeto
Uma aplicação web de lista de tarefas com autenticação, estilizada com TailwindCSS e inspirada em post-its fofinhos. Cada usuário pode adicionar, editar e excluir suas próprias tarefas, com sistema de login e logout seguro.

## Problema
O ToDo Post-It resolve esse problema oferecendo:
- Uma interface leve, acessível e divertida (estilo post-it);
- Cadastro e login de usuários;
- Visualização personalizada: cada usuário vê apenas suas tarefas;
- Organização por prioridade (baixa, média, alta);
- Edição e exclusão intuitiva das tarefas;
- Logout com apenas um clique.

Tudo isso com uma estrutura clara e responsiva, desenvolvida com Django e TailwindCSS.

## Solução
Gerenciar tarefas diárias pode ser difícil sem uma ferramenta simples e acessível. Muitas soluções existentes são complicadas ou sem personalidade, o que desmotiva o uso contínuo.

![Banner do TODOLIST](https://github.com/user-attachments/assets/bfa92ddb-4c7b-481f-9478-d575709d7c33)

![Banner do TODOLIST](https://github.com/user-attachments/assets/70fbfe25-f3b6-48d9-98c5-46b2ceb80cda)

---

## Tecnologias

- Python 3.12
- Django 5
- Tailwind CSS
- HTML + Jinja
- SQLite (banco local para testes)

---

## Como rodar o projeto localmente

```bash
# Clone o repositório
git clone https://github.com/seuusuario/todo-postit.git
cd todo-postit

# Crie o ambiente virtual
python -m venv venv
source venv/bin/activate  # ou venv\Scripts\activate no Windows

# Instale as dependências
pip install -r requirements.txt

# Migre o banco
python manage.py migrate

# Crie um superusuário
python manage.py createsuperuser

# Rode o servidor
python manage.py runserver
```

| ![Jamyle Elen][img2] |
|:--------------------:|
| **Jamyle Elen**      |
| **Programador** |

[img2]: https://github.com/user-attachments/assets/4b3637cc-e1a0-45e4-af1b-6b37f3626ecb
