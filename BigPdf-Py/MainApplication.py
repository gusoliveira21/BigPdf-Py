import PyPDF2
from PyPDF2 import PdfReader, PdfWriter
import os
import tkinter as tk
from tkinter import filedialog, messagebox, Listbox
from JanelaSenhas import JanelaSenhas
from tkinter.ttk import Treeview
import logging


def escrever_pdf_decifrado(pdf_file, output_name_file):
    pdf_writer = PdfWriter()
    for page in pdf_file.pages:
        pdf_writer.add_page(page)
    pdf_writer.write(output_name_file)


def method_is_encrypted(pdf_file):
    with open(pdf_file, 'rb') as file:
        pdf = PdfReader(file)
        return pdf.is_encrypted


class MainApplication(tk.Tk):
    list_pdf = []

    def __init__(self):
        super().__init__()
        width = "600"
        height = "400"
        self.geometry(width + "x" + height)
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

        botao_unir_pdf = tk.Button(self.toolbar, text="Unir PDFs", command=self.unir_pdf)
        botao_unir_pdf.pack(side="left")

        self.lista_arquivos = Treeview(self, columns=('Nome',))
        self.lista_arquivos.heading('#0', text='Nome')
        self.lista_arquivos.column('#0', width=width)
        self.lista_arquivos.pack()

        self.mainloop()

    def unir_pdf(self):
        pdf_files = []
        pdf_readers = []
        pdfs_selecionados = self.lista_arquivos.selection()
        for pdf in pdfs_selecionados:
            if not self.esta_encrypted(pdf):
                rota_arquivo = self.lista_arquivos.item(pdf)['text']
                if os.path.isfile(rota_arquivo):
                    try:
                        pdf_files.append(open(rota_arquivo, 'rb'))
                        pdf_readers.append(PyPDF2.PdfReader(rota_arquivo))
                        merged_pdf = PyPDF2.PdfWriter()
                        for pdf_reader in pdf_readers:
                            for page in range(len(pdf_reader.pages)):
                                merged_pdf.add_page(pdf_reader.pages[page])
                    except Exception as e:
                        logging.exception(e)
                else:
                    print("Não é um arquivo")
            else:
                print("mensagem avisando que arquivo esta com senha")
        save_file = filedialog.asksaveasfile(mode ='wb', defaultextension=".pdf")
        merged_pdf.write(save_file)
        for pdf_file in pdf_files:
            pdf_file.close()
        save_file.close()

    def esta_encrypted(self, pdf_selecionado):
        pdf_file = self.lista_arquivos.item(pdf_selecionado)['text']
        return method_is_encrypted(pdf_file)

    def decrypt(self, pdf_file, password):
        rota_arquivo = self.lista_arquivos.item(pdf_file)['text']
        if os.path.isfile(rota_arquivo):
            try:
                with open(rota_arquivo, 'rb') as file:
                    pdf = PdfReader(file)
                    if pdf.decrypt(password):
                        escrever_pdf_decifrado(pdf, rota_arquivo)
                        file.close()
                        return True
                    else:
                        file.close()
                        return False
                file.close()
                return True
            except Exception as e:
                logging.exception(e)
        else:
            messagebox.showerror("Erro", "decrypt: Arquivo não encontrado")

    def desbloquear_pdf(self):
        selecionado = self.lista_arquivos.selection()
        with open("senhas.txt", 'r') as password_file:
            passwords = password_file.read().splitlines()
        for arquivo_selecionado in selecionado:
            if self.esta_encrypted(arquivo_selecionado):
                for password in passwords:
                    if self.decrypt(arquivo_selecionado, password):
                        self.lista_arquivos.item(arquivo_selecionado, tags="green")
                        self.aplicar_cor_pdf("green")
                        self.remove_selecao(arquivo_selecionado)
                        break
                    else:
                        self.remove_selecao(arquivo_selecionado)
                        print("desbloquear_pdf: Provavelmente não tem senha para esse pdf")
                else:
                    print("desbloquear_pdf: Realmente nao tem senha pra ele")
                    self.remove_selecao(arquivo_selecionado)
            else:
                self.remove_selecao(arquivo_selecionado)

    def exibir_senhas(self):
        JanelaSenhas(self)

    def remove_selecao(self, arquivo):
        self.lista_arquivos.selection_remove(arquivo)

    def definir_cor_arquivo(self, router):
        if method_is_encrypted(router):
            return "red"
        else:
            return "green"

    def aplicar_cor_pdf(self, cor_definida):
        if cor_definida == "green":
            self.lista_arquivos.tag_configure("green", background="#00FF00")
        else:
            self.lista_arquivos.tag_configure("red", background="#ff5863")

    def selecionar_arquivos(self):
        arquivos = tk.filedialog.askopenfilenames(filetypes=[("Arquivos PDF", "*.pdf")])
        for arquivo in arquivos:
            if arquivo not in self.list_pdf:
                self.list_pdf.append(arquivo)
                tag_cor = self.definir_cor_arquivo(arquivo)
                self.lista_arquivos.insert('', 'end', text=arquivo, tags=tag_cor)
                self.aplicar_cor_pdf(tag_cor)
            else:
                messagebox.showerror("Erro", "O arquivo {} já existe na lista".format(arquivo))

    def remover_arquivos(self):
        selecionado = self.lista_arquivos.selection()
        for arquivo in selecionado:
            self.list_pdf.remove(self.lista_arquivos.item(arquivo)['text'])
            self.lista_arquivos.delete(arquivo)

    def salvar_pdf(self):
        root = tk.Tk()
        root.withdraw()

        file_path = filedialog.asksaveasfilename(defaultextension=".pdf")

        with open(file_path, "wb") as output_file:
            # código para mesclar os arquivos PDF aqui
            output_file.write(merged_pdf_bytes)
if __name__ == "__main__":
    app = MainApplication()
