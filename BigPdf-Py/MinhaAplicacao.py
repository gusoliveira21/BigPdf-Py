import logging

from PyPDF2 import PdfReader, PdfWriter
import os
import tkinter as tk
from tkinter import filedialog, messagebox, Listbox
from JanelaSenhas import JanelaSenhas
from tkinter.ttk import Treeview
import logging

class MinhaAplicacao(tk.Tk):
    list_pdf = []

    def __init__(self):
        super().__init__()
        self.geometry("800x800")
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
        self.lista_arquivos.column('#0', width=598)
        self.lista_arquivos.column('#1', width=200)
        self.lista_arquivos.pack()

        self.mainloop()

    def method_is_encrypted(self, pdf_file):
        with open(pdf_file, 'rb') as file:
            pdf = PdfReader(file)
            return pdf.is_encrypted

    def esta_encrypted(self, pdf_selecionado):
        pdf_file = self.lista_arquivos.item(pdf_selecionado)['text']
        return self.method_is_encrypted(pdf_file)

    def decrypt(self, pdf_file, password):
        rota_arquivo = self.lista_arquivos.item(pdf_file)['text']
        if os.path.isfile(rota_arquivo):
            try:
                with open(rota_arquivo, 'rb') as file:
                    pdf = PdfReader(file)
                    if pdf.decrypt(password):
                        self.escrever_pdf_decifrado(pdf, rota_arquivo)
                        file.close()
                        return True
                file.close()
                return True
            except Exception as e:
                logging.exception(e)
        else:
            messagebox.showerror("Erro", "Arquivo não encontrado")

    def escrever_pdf_decifrado(self, pdf_file, output_name_file):
        pdf_writer = PdfWriter()
        for page in pdf_file.pages:
            pdf_writer.add_page(page)
        pdf_writer.write(output_name_file)
        os.replace(output_name_file, pdf_file)

    def desbloquear_pdf(self):
        selecionado = self.lista_arquivos.selection()
        with open("senhas.txt", 'r') as password_file:
            passwords = password_file.read().splitlines()
        for arquivo_selecionado in selecionado:
            if self.esta_encrypted(arquivo_selecionado):
                for password in passwords:
                    if self.decrypt(arquivo_selecionado, password):
                        self.lista_arquivos.item(arquivo_selecionado, values="VERDE")
                        break
            else:
                self.lista_arquivos.item(arquivo_selecionado, values="VERDE")

    def exibir_senhas(self):
        JanelaSenhas(self)

    def method_setup_colum_decrypt(self, router):
        if self.method_is_encrypted(router):
            return "VERMELHO"
        else:
            return "VERDE"

    def selecionar_arquivos(self):
        arquivos = tk.filedialog.askopenfilenames(filetypes=[("Arquivos PDF", "*.pdf")])
        for arquivo in arquivos:
            if arquivo not in self.list_pdf:
                self.list_pdf.append(arquivo)
                self.lista_arquivos.insert('', 'end', text=arquivo, values=(self.method_setup_colum_decrypt(arquivo)))
            else:
                messagebox.showerror("Erro", "O arquivo {} já existe na lista".format(arquivo))

    def remover_arquivos(self):
        selecionado = self.lista_arquivos.selection()
        for arquivo in selecionado:
            self.list_pdf.remove(self.lista_arquivos.item(arquivo)['text'])
            self.lista_arquivos.delete(arquivo)


if __name__ == "__main__":
    app = MinhaAplicacao()
