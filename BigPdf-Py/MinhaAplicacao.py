import logging

from PyPDF2 import PdfReader, PdfWriter
import os
import tkinter as tk
from tkinter import filedialog, messagebox, Listbox
from JanelaSenhas import JanelaSenhas
from tkinter.ttk import Treeview
import logging

class MinhaAplicacao(tk.Tk):
    def __init__(self):
        super().__init__()
        self.geometry("800x600")
        self.title("BigPdf")

        self.toolbar = tk.Frame(self)
        self.toolbar.pack(side="top", fill="x")

        botao_selecionar = tk.Button(self.toolbar, text="Selecionar arquivos", command=self.selecionar_arquivos)
        botao_selecionar.pack(side="left")

        botao_remover = tk.Button(self.toolbar, text="Remover arquivos", command=self.remover_arquivos)
        botao_remover.pack(side="left")

        botao_exibir_senhas = tk.Button(self.toolbar, text="Gerenciar senhas", command=self.exibir_senhas)
        botao_exibir_senhas.pack(side="left")

        botao_desbloquear = tk.Button(self.toolbar, text="Desbloquear um PDF", command=self.desbloquear_pdf)
        botao_desbloquear.pack(side="left")

        self.lista_arquivos = Treeview(self, columns=('Nome', 'Descriptado'))
        self.lista_arquivos.heading('#0', text='Nome')
        self.lista_arquivos.heading('#1', text='Descriptado')
        self.lista_arquivos.column('#0', width=400)
        self.lista_arquivos.column('#1', width=400)
        self.lista_arquivos.pack()

        self.mainloop()

    def esta_encrypted(self, pdf_selecionado):
        pdf_file = self.lista_arquivos.item(pdf_selecionado)['text']
        with open(pdf_file, 'rb') as file:
            pdf = PdfReader(file)
            return pdf.is_encrypted

    def decrypt(self, pdf_file, password):
        rota_arquivo = self.lista_arquivos.item(pdf_file)['text']
        if os.path.isfile(rota_arquivo):
            try:
                with open(rota_arquivo, 'rb') as file:
                    pdf = PdfReader(file)
                    if pdf.decrypt(password):
                        messagebox.showerror("Sucesso", "SUCESSO")
                        file.close()
                        return True
                messagebox.showerror("Sucesso", "SUCESSO")
                file.close()
                return True
            except Exception as e:
                logging.exception(e)
        else:
            messagebox.showerror("Erro", "Arquivo não encontrado")

    def desbloquear_pdf(self):
        selecionado = self.lista_arquivos.selection()
        with open("senhas.txt", 'r') as password_file:
            passwords = password_file.read().splitlines()
        for arquivo_selecionado in selecionado:
            valor = False
            if self.esta_encrypted(arquivo_selecionado):
                for password in passwords:
                    if self.decrypt(arquivo_selecionado, password):
                        valor = True
                        self.lista_arquivos.item(arquivo_selecionado, values="verde")
                        break
            else:
                self.lista_arquivos.item(arquivo_selecionado, values="verde")
            if valor:
                print("escrevendo pdf")
                self.escrever_pdf_decifrado(self.lista_arquivos.item(arquivo_selecionado)['text'], 'decrypted.pdf')


    def escrever_pdf_decifrado(pdf_file, output_file):
        with open(pdf_file, 'rb') as file:
            pdf = PdfReader(file)
            pdf_writer = PdfWriter()
            for page in pdf.pages:
                pdf_writer.add_page(page)
            pdf_writer.write(output_file)
        os.replace(output_file, pdf_file)

    def exibir_senhas(self):
        JanelaSenhas(self)

    def selecionar_arquivos(self):
        arquivos = tk.filedialog.askopenfilenames(filetypes=[("Arquivos PDF", "*.pdf")])
        for arquivo in arquivos:
            self.lista_arquivos.insert('', 'end', text=arquivo, values=("status"))

    def remover_arquivos(self):
        selecionado = self.lista_arquivos.selection()
        for arquivo in selecionado:
            self.lista_arquivos.delete(arquivo)


if __name__ == "__main__":
    app = MinhaAplicacao()
