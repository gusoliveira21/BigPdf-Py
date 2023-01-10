import tkinter as tk
from tkinter import filedialog, messagebox


class JanelaSenhas(tk.Toplevel):
    def __init__(self, master):
        super().__init__(master)
        self.geometry("300x200")
        self.title("Senhas")

        self.toolbar = tk.Frame(self)
        self.toolbar.pack(side="top", fill="x")

        botao_adicionar = tk.Button(self.toolbar, text="Adicionar", command=self.adicionar_senhas)
        botao_adicionar.pack(side="left")

        botao_excluir = tk.Button(self.toolbar, text="Excluir", command=self.excluir_senhas)
        botao_excluir.pack(side="left")

        self.lista_senhas = tk.Listbox(self, width=200, height=200, selectmode="single")
        self.lista_senhas.pack()

        self.listar_senhas()

    def listar_senhas(self):
        self.limpa_lista_da_tela()
        with open("senhas.txt", "r") as arquivo:
            for senha in arquivo:
                self.lista_senhas.insert(tk.END, senha.strip())

    def limpa_lista_da_tela(self):
        self.lista_senhas.delete(0, tk.END)

    def adicionar_senhas(self):
        senhas_string = tk.simpledialog.askstring("Senhas", "Digite as senhas, separadas por vírgula:")
        senhas = senhas_string.split(',')
        if senhas:
            with open("senhas.txt", "a") as arquivo:
                for senha in senhas:
                    arquivo.write(senha.strip() + "\n")
            self.listar_senhas()
        else:
            messagebox.showerror("Erro", "Nenhuma senha inserida")

    def excluir_senhas(self):
        index = self.lista_senhas.curselection()

        if index:
            self.lista_senhas.delete(index)

            with open("senhas.txt", "w") as arquivo:
                senhas = self.lista_senhas.get(0, tk.END)
                for senha in senhas:
                    arquivo.write(senha + "\n")
        else:
            messagebox.showerror("Erro", "Nenhuma senha selecionada para excluir")