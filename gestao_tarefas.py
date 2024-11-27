import sqlite3
import ttkbootstrap as ttk
from ttkbootstrap.constants import *

def conectar():
    return sqlite3.connect('gestao_tarefas.db')

def criar_tabela():
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS Tarefas (
        id_tarefa INTEGER PRIMARY KEY AUTOINCREMENT,
        titulo TEXT NOT NULL,
        descricao TEXT NOT NULL,
        data_criacao DATETIME DEFAULT CURRENT_TIMESTAMP,
        data_prazo DATETIME NOT NULL,
        status TEXT CHECK(status IN ('pendente', 'concluida')) DEFAULT 'pendente',
        prioridade TEXT CHECK(prioridade IN ('Alta', 'Média', 'Baixa')) DEFAULT 'Média'
    );
    """)
    conn.commit()
    conn.close()

def adicionar_tarefa(titulo, descricao, data_prazo, prioridade):
    if not titulo or not descricao or not data_prazo:
        ttk.dialogs.MessageDialog(
            title="Erro",
            message="Todos os campos são obrigatórios!",
            buttons=["OK"],
            icon="error"
        ).show()
        return
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("""
    INSERT INTO Tarefas (titulo, descricao, data_prazo, prioridade)
    VALUES (?, ?, ?, ?)
    """, (titulo, descricao, data_prazo, prioridade))
    conn.commit()
    conn.close()
    ttk.dialogs.MessageDialog(
        title="Sucesso",
        message="Tarefa adicionada com sucesso!",
        buttons=["OK"],
        icon="info"
    ).show()

def listar_tarefas():
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Tarefas")
    tarefas = cursor.fetchall()
    conn.close()
    tarefas_texto = ""
    for t in tarefas:
        tarefas_texto += (
            f"ID: {t[0]}\n"
            f"Título: {t[1]}\n"
            f"Descrição: {t[2]}\n"
            f"Prazo: {t[4]}\n"
            f"Status: {t[5]}\n"
            f"Prioridade: {t[6]}\n"
            "---------------------------\n"
        )
    return tarefas_texto

def atualizar_status(id_tarefa, status):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("""
    UPDATE Tarefas
    SET status = ?
    WHERE id_tarefa = ?
    """, (status, id_tarefa))
    conn.commit()
    conn.close()
    ttk.dialogs.MessageDialog(
        title="Sucesso",
        message="Status atualizado com sucesso!",
        buttons=["OK"],
        icon="info"
    ).show()

def excluir_tarefa(id_tarefa):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("""
    DELETE FROM Tarefas
    WHERE id_tarefa = ?
    """, (id_tarefa,))
    conn.commit()
    conn.close()
    ttk.dialogs.MessageDialog(
        title="Sucesso",
        message="Tarefa excluída com sucesso!",
        buttons=["OK"],
        icon="info"
    ).show()

def adicionar_tarefa_gui():
    titulo = entry_titulo.get()
    descricao = descricao_text.get("1.0", "end").strip()
    data_prazo = entry_prazo.get()
    prioridade = combo_prioridade.get()
    adicionar_tarefa(titulo, descricao, data_prazo, prioridade)
    atualizar_lista_tarefas()

def atualizar_status_gui():
    try:
        id_tarefa = int(entry_id_tarefa.get())
        status = combo_status.get()
        if status:
            atualizar_status(id_tarefa, status)
            atualizar_lista_tarefas()
        else:
            ttk.dialogs.MessageDialog(
                title="Erro",
                message="Escolha um status válido!",
                buttons=["OK"],
                icon="error"
            ).show()
    except ValueError:
        ttk.dialogs.MessageDialog(
            title="Erro",
            message="Digite um ID válido!",
            buttons=["OK"],
            icon="error"
        ).show()

def excluir_tarefa_gui():
    try:
        id_tarefa = int(entry_id_tarefa.get())
        excluir_tarefa(id_tarefa)
        atualizar_lista_tarefas()
    except ValueError:
        ttk.dialogs.MessageDialog(
            title="Erro",
            message="Digite um ID válido!",
            buttons=["OK"],
            icon="error"
        ).show()

def atualizar_lista_tarefas():
    lista_tarefas.delete("1.0", "end")
    tarefas_texto = listar_tarefas()
    lista_tarefas.insert("end", tarefas_texto)

app = ttk.Window(themename="solar")
app.title("Sistema de Gestão de Tarefas")
app.geometry("700x600")

ttk.Label(app, text="Título:").grid(row=0, column=0, padx=10, pady=5)
entry_titulo = ttk.Entry(app, width=40)
entry_titulo.grid(row=0, column=1, padx=10, pady=5)

ttk.Label(app, text="Descrição:").grid(row=1, column=0, padx=10, pady=5)
descricao_text = ttk.Text(app, width=40, height=4)
descricao_text.grid(row=1, column=1, padx=10, pady=5)

ttk.Label(app, text="Prazo (YYYY-MM-DD):").grid(row=2, column=0, padx=10, pady=5)
entry_prazo = ttk.Entry(app, width=40)
entry_prazo.grid(row=2, column=1, padx=10, pady=5)

ttk.Label(app, text="Prioridade:").grid(row=3, column=0, padx=10, pady=5)
combo_prioridade = ttk.Combobox(app, values=["Alta", "Média", "Baixa"], width=37, state="readonly")
combo_prioridade.set("Média")
combo_prioridade.grid(row=3, column=1, padx=10, pady=5)

ttk.Button(app, text="Adicionar Tarefa", bootstyle=SUCCESS, command=adicionar_tarefa_gui).grid(row=4, column=0, columnspan=2, pady=10)

lista_tarefas = ttk.Text(app, width=80, height=20)
lista_tarefas.grid(row=5, column=0, columnspan=2, padx=10, pady=10)

ttk.Label(app, text="ID Tarefa:").grid(row=6, column=0, padx=10, pady=5)
entry_id_tarefa = ttk.Entry(app, width=40)
entry_id_tarefa.grid(row=6, column=1, padx=10, pady=5)

ttk.Label(app, text="Novo Status:").grid(row=7, column=0, padx=10, pady=5)
combo_status = ttk.Combobox(app, values=["pendente", "concluida"], width=37, state="readonly")
combo_status.set("pendente")
combo_status.grid(row=7, column=1, padx=10, pady=5)

ttk.Button(app, text="Atualizar Status", bootstyle=INFO, command=atualizar_status_gui).grid(row=8, column=0, pady=10)
ttk.Button(app, text="Excluir Tarefa", bootstyle=DANGER, command=excluir_tarefa_gui).grid(row=8, column=1, pady=10)

criar_tabela()
atualizar_lista_tarefas()
app.mainloop()
