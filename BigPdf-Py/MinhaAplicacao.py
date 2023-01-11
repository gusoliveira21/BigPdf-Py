from PyPDF2 import PdfReader, PdfWriter
import os
import tkinter as tk
from tkinter import filedialog, messagebox
from JanelaSenhas import JanelaSenhas


class MinhaAplicacao(tk.Tk):
    def __init__(self):
        super().__init__()
        self.geometry("800x600")
        self.title("Minha Aplicação")

        self.toolbar = tk.Frame(self)
        self.toolbar.pack(side="top", fill="x")

        botao_selecionar = tk.Button(self.toolbar, text="Selecionar arquivos", command=self.selecionar_arquivos)
        botao_selecionar.pack(side="left")

        botao_remover = tk.Button(self.toolbar, text="Remover arquivos", command=self.remover_arquivos)
        botao_remover.pack(side="left")

        botao_exibir_senhas = tk.Button(self.toolbar, text="Gerenciar senhas", command=self.exibir_senhas)
        botao_exibir_senhas.pack(side="left")

        botao_desbloquear = tk.Button(self.toolbar, text="Desbloquear PDFs", command=self.desbloquear_pdfs)
        botao_desbloquear.pack(side="left")

        self.lista_arquivos = tk.Listbox(self, width=400, height=400)
        self.lista_arquivos.pack()

        self.mainloop()

    def desbloquear_pdfs(self):
        pdf_files = self.lista_arquivos.get(0, tk.END)

        for pdf_file in pdf_files:
            with open(pdf_file, 'rb') as file:
                pdf = PdfReader(file)

                if pdf.is_encrypted:
                    password = tk.simpledialog.askstring("Senha",
                                                         "Digite a senha para o arquivo {}:".format(pdf_file),
                                                         show='*')
                    pdf.decrypt(password)

                with open('decrypted.pdf', 'wb') as output:
                    pdf_writer = PdfWriter()

                    for page in pdf.pages:
                        pdf_writer.add_page(page)

                    pdf_writer.write(output)

            os.replace('decrypted.pdf', pdf_file)

    def exibir_senhas(self):
        janela_senhas = JanelaSenhas(self)

    def selecionar_arquivos(self):
        arquivos = tk.filedialog.askopenfilenames(filetypes=[("Arquivos PDF", "*.pdf")])

        for arquivo in arquivos:
            if arquivo not in self.lista_arquivos.get(0, tk.END):
                self.lista_arquivos.insert(tk.END, arquivo)
            else:
                messagebox.showerror("Erro", "O arquivo {} já existe na lista".format(arquivo))

    def remover_arquivos(self):
        index = self.lista_arquivos.curselection()

        if index:
            self.lista_arquivos.delete(index)
        else:
            messagebox.showerror("Erro", "Nenhum arquivo selecionado para remover")


if __name__ == "__main__":
    app = MinhaAplicacao()
