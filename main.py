import tkinter as tk
from tkinter import messagebox
import pandas as pd
from pandastable import Table, TableModel
import re

def cadastrar():
    usuario = entry_usuario.get()
    senha = entry_senha.get()

    if usuario in usuarios_cadastrados:
        label_status.config(text="Usuário já cadastrado", fg="red")
    else:
        if not usuario or not senha:
            label_status.config(text="Por favor, preencha todos os campos", fg="red")
        else:
            if not verifica_requisitos_senha(senha):
                label_status.config(text="A senha deve conter pelo menos um símbolo (!@$), uma letra maiúscula, uma letra minúscula e não pode estar em branco", fg="red")
            else:
                usuarios_cadastrados.append(usuario)
                senhas[usuario] = senha
                label_status.config(text="Cadastro realizado com sucesso", fg="green")

def verifica_requisitos_senha(senha):
    return re.search(r"[!@$]", senha) and re.search(r"[a-z]", senha) and re.search(r"[A-Z]", senha)

def login():
    usuario = entry_usuario.get()
    senha = entry_senha.get()

    if usuario in usuarios_cadastrados and senhas.get(usuario) == senha:
        label_status.config(text="Login realizado com sucesso", fg="green")
        abrir_janela_dados_empresa()
    else:
        label_status.config(text="Usuário ou senha incorretos", fg="red")

def abrir_janela_dados_empresa():
    global tabela_dados

    janela_dados_empresa = tk.Toplevel(janela)
    janela_dados_empresa.geometry("1000x600")
    janela_dados_empresa.title("Banco de Dados - Empresa de Tecnologia")
    janela_dados_empresa.configure(bg="#3498db")

    frame_planilha = tk.Frame(janela_dados_empresa)
    frame_planilha.pack(pady=10)

    data = {
        'Item': ['Iphone', 'Moto G8 Plus', 'PS5', 'Gtx 1080', 'Xbox-One', 'Tablet', 'Notebok Lenovo', 'MacBook', 'Ipad', 'Teclado'],
        'Vendas do Dia': [10, 15, 8, 20, 12, 17, 9, 14, 7, 16],
        'Valor dos Itens': [8400, 1000, 4550, 1500, 1850, 800, 2950, 3680, 2242, 360],
        'Estoque': [100, 150, 80, 200, 120, 170, 90, 140, 70, 160]
    }

    global df_original
    df_original = pd.DataFrame(data)

    global df
    df = df_original.copy()  # Criando uma cópia dos dados originais

    global planilha
    planilha = Table(frame_planilha, dataframe=df)
    planilha.show()

    # Botões para adicionar, remover e resetar itens
    botao_adicionar_item = tk.Button(janela_dados_empresa, text="Adicionar Item", font=("Arial", 12), command=lambda: adicionar_item(), bg="#4CAF50", fg="white")
    botao_adicionar_item.pack(pady=5)

    botao_remover_item = tk.Button(janela_dados_empresa, text="Remover Item", font=("Arial", 12), command=lambda: remover_item(), bg="#FF5733", fg="white")
    botao_remover_item.pack(pady=5)

    botao_resetar_itens = tk.Button(janela_dados_empresa, text="Resetar Itens", font=("Arial", 12), command=lambda: resetar_itens(df_original), bg="#FFC300", fg="white")
    botao_resetar_itens.pack(pady=5)

def adicionar_item(df):
    global planilha  # Declarando planilha como global para acessar a variável global

    novo_item = {'Produtos': 'Novo Item', 'Vendas do Dia': 0, 'Valor dos Itens': 0, 'Estoque': 0}
    df = df.append(novo_item, ignore_index=True)
    planilha.updateModel(TableModel(df))


def remover_item():
    selected_index = planilha.getSelectedRow()
    if selected_index is not None:
        df.drop(selected_index, inplace=True)
        planilha.updateModel(TableModel(df))

def resetar_itens(df_original):
    df = df_original.copy()  # Resetando os itens para os valores originais
    planilha.updateModel(TableModel(df))

usuarios_cadastrados = []
senhas = {}

janela = tk.Tk()
janela.geometry("900x400")
janela.title("Banco de Dados - Empresa de Tecnologia")
janela.configure(bg="#3498db")

# Adicionando a logo wolf.png ao título do menu do aplicativo
logo = tk.PhotoImage(file="wolf.png")
label_logo = tk.Label(janela, image=logo, bg="#3498db")
label_logo.pack()

texto_boas_vindas = tk.Label(janela, text="Bem-vindo ao Banco de Dados da Empresa de Tecnologia", font=("Helvetica", 24, "bold"), bg="#3498db", fg="white")
texto_boas_vindas.pack()

descricao = "Acesse informações privilegiadas sobre a Empresa de Tecnologia."
descricao_label = tk.Label(janela, text=descricao, font=("Arial", 14), bg="#3498db", fg="white")
descricao_label.pack(pady=10)

frame_entradas = tk.Frame(janela, bg="#3498db")
frame_entradas.pack(pady=10)

label_usuario = tk.Label(frame_entradas, text="Usuário:", font=("Arial", 14), bg="#3498db", fg="white")
label_usuario.grid(row=0, column=0, padx=5)
entry_usuario = tk.Entry(frame_entradas, font=("Arial", 12))
entry_usuario.grid(row=0, column=1, padx=5)

label_senha = tk.Label(frame_entradas, text="Senha:", font=("Arial", 14), bg="#3498db", fg="white")
label_senha.grid(row=1, column=0, padx=5)
entry_senha = tk.Entry(frame_entradas, font=("Arial", 12), show="*")
entry_senha.grid(row=1, column=1, padx=5)

frame_botoes = tk.Frame(janela, bg="#3498db")
frame_botoes.pack(pady=10)

botao_cadastrar = tk.Button(frame_botoes, text="Cadastrar", font=("Arial", 14), command=cadastrar, bg="#4CAF50", fg="white")
botao_cadastrar.grid(row=0, column=0, padx=5)

botao_login = tk.Button(frame_botoes, text="Login", font=("Arial", 14), command=login, bg="#008CBA", fg="white")
botao_login.grid(row=0, column=1, padx=5)

label_status = tk.Label(janela, text="", font=("Arial", 12), bg="#3498db", fg="white")
label_status.pack(pady=10)

janela.mainloop()
