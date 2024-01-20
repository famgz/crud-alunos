import tkinter as tk
from tkinter import messagebox
from pathlib import Path
import sys
from utils import json_

source_path = Path(__file__).resolve().parent
sys.path.insert(0, str(source_path.parent))

data_path = Path(source_path, 'data', 'data_alunos.json')


# criar arquivo caso nao exista
if not data_path.exists():
    json_(data_path, {})


# Função para ler o arquivo .json
def ler_arquivo():
    return json_(data_path)


def mostrar(mensagem):
    print(mensagem)
    messagebox.showinfo('Informação', mensagem)


# Salvar alteracoes
def salvar(dados):
    prev = ler_arquivo()
    prev.update(dados)
    return json_(data_path, prev, backup=True, indent='\t')


# Função para excluir um registro no arquivo .json
def excluir_registro(matricula):
    prev = ler_arquivo()
    removido = prev.pop(matricula, None)
    salvar(prev)
    return removido


# Limpar todos os campos
def limpar_campos():
    for entrada in entradas:
        entrada.delete(0, 'end')


def validar_registros(dados):
    def invalidar():
        nonlocal valido
        valido = False

    valido = True
    for key, value in dados.items():
        err_msg = f'Entrada de {key} inválida: {value}'
        if key == 'nome':
            if len(value) < 3:
                invalidar()
                mostrar(err_msg + '\nNome deve ter ao menos 3 caracteres')
                break
        elif key == 'idade':
            if not (value.isdecimal() and int(value) <= 100):
                invalidar()
                mostrar(err_msg + '\nNúmero inválido ou fora do alcance (18-100)')
                break
        elif key == 'sexo':
            if value not in 'fm':
                invalidar()
                mostrar(err_msg + '\nSexo deve ser `f` ou `m`')
                break
        elif key == 'matricula':
            if not value.isdecimal():
                invalidar()
                mostrar(err_msg + '\nMatricula deve conter apenas números')
                break
        elif key.startswith('nota'):
            if not (value.isdecimal() and 0 <= int(value) <= 10):
                invalidar()
                mostrar(err_msg + '\nNúmero inválido ou fora do alcance (0-10)')
                break

    return valido


# Função para inserir um registro no arquivo .json
def inserir_registro():
    dados = {
        'matricula': entrada_matricula.get().strip(),
        'nome': entrada_nome.get().strip(),
        'idade': entrada_idade.get().strip(),
        'sexo': entrada_sexo.get().strip().lower(),
        'nota1': entrada_nota1.get().strip(),
        'nota2': entrada_nota2.get().strip(),
        'nota3': entrada_nota3.get().strip(),
    }

    # Verificar se todos os campos foram preenchidos
    print(dados.values())
    if not all(dados.values()):
        mostrar('Preencha todos os campos!')
        return

    # Validar campos
    if not validar_registros(dados):
        return

    notas = [float(dados['nota1']), float(dados['nota2']), float(dados['nota3'])]
    dados['media'] = sum(notas) / len(notas)

    # converter para entrada chave-valor
    matricula = dados.pop('matricula')
    dados = {matricula: dados}
    salvo = salvar(dados)
    if salvo:
        mostrar('Registros adicionados com sucesso!\n' + str(dados))
    limpar_campos()


# Função para excluir um registro no arquivo .json
def remover_aluno():
    matricula = entrada_matricula.get()
    if not matricula:
        mostrar('Nenhuma matricula encontrada para remover')
        return
    removido = excluir_registro(matricula)
    if removido:
        mostrar('Registro removido com sucesso:\n' + str(removido))
    else:
        mostrar('Matricula não encontrada: ' + matricula)



def buscar_registro():
    dados = ler_arquivo()
    mostrar(dados)
    # idade
    # sexo
    # matricula
    # nota1
    # nota2
    # nota3


# Função para exibir os registros do arquivo .json
def exibir_registros():
    dados = ler_arquivo()
    mostrar(dados)


# Inicializando a interface gráfica
janela = tk.Tk()
janela.title("CRUD Notas")
janela.geometry("640x480")

# Criando os campos de entrada e respectivos labels
label_nome = tk.Label(janela, text='nome')
entrada_nome = tk.Entry(janela)

label_idade = tk.Label(janela, text='idade')
entrada_idade = tk.Entry(janela)

label_sexo = tk.Label(janela, text='sexo')
entrada_sexo = tk.Entry(janela)

label_matricula = tk.Label(janela, text='matricula')
entrada_matricula = tk.Entry(janela)

label_nota1 = tk.Label(janela, text='nota1')
entrada_nota1 = tk.Entry(janela)

label_nota2 = tk.Label(janela, text='nota2')
entrada_nota2 = tk.Entry(janela)

label_nota3 = tk.Label(janela, text='nota3')
entrada_nota3 = tk.Entry(janela)

'''

# Criando os botões
btn_width = 15
btn_padx = 2
botao_criar = tk.Button(janela, text="Inserir", command=inserir_registro, width=btn_width)
botao_ler = tk.Button(janela, text="Ler", command=exibir_registros, width=btn_width)
botao_excluir = tk.Button(janela, text="Excluir", command=remover_aluno, width=btn_width)

# Empacotando variaveis para reutilizacao
labels = [label_nome, label_idade, label_sexo, label_matricula, label_nota1, label_nota2, label_nota3]
entradas = [entrada_nome, entrada_idade, entrada_sexo, entrada_matricula, entrada_nota1, entrada_nota2, entrada_nota3]
botoes = [botao_criar, botao_ler, botao_excluir]

# Adicionando os labels à interface gráfica
for i, entrada in enumerate(labels):
    entrada.grid(row=i, column=0)

# Adicionando os campos de entrada e os botões à interface gráfica
for i, entrada in enumerate(entradas + botoes):
    entrada.grid(row=i, column=1)

# Chamando a função mainloop()
janela.mainloop()
'''


# Styling
font_style = ("Arial", 12)
label_width = 10
entry_width = 20
btn_width = 15
btn_padx = 5

# Creating and styling labels
labels = ["Nome", "Idade", "Sexo", "Matrícula", "Nota 1", "Nota 2", "Nota 3"]
label_widgets = [tk.Label(janela, text=label, font=font_style, width=label_width) for label in labels]

# Creating and styling entry widgets
entry_widgets = [tk.Entry(janela, width=entry_width) for _ in range(len(labels))]

# Creating buttons
btn_criar = tk.Button(janela, text="Inserir", command=inserir_registro, width=btn_width)
btn_ler = tk.Button(janela, text="Ler", command=exibir_registros, width=btn_width)
btn_excluir = tk.Button(janela, text="Excluir", command=remover_aluno, width=btn_width)

# Creating and styling the output box
output_box = tk.Text(janela, height=10, width=60, state=tk.DISABLED, wrap=tk.WORD)

# Centering elements
center_column = 2
for i, (label, entry) in enumerate(zip(label_widgets, entry_widgets)):
    label.grid(row=i, column=center_column - 1, padx=10, pady=5, sticky=tk.E)
    entry.grid(row=i, column=center_column, padx=10, pady=5)

# Centering buttons
btn_criar.grid(row=len(labels), column=center_column - 1, columnspan=2, pady=10)
btn_ler.grid(row=len(labels) + 1, column=center_column - 1, columnspan=2, pady=5)
btn_excluir.grid(row=len(labels) + 2, column=center_column - 1, columnspan=2, pady=5)

# Centering output box
output_box.grid(row=len(labels) + 3, column=center_column - 1, columnspan=2, pady=10)

# Calling the main loop
janela.mainloop()
