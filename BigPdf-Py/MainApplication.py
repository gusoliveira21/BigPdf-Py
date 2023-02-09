import logging
import os
import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter.ttk import Treeview

import PyPDF2
from PyPDF2 import PdfReader, PdfWriter

from WindowPassword import PasswordWindow


def write_unlocked_pdf(pdf_file, output_name_file):
    pdf_writer = PdfWriter()
    for page in pdf_file.pages:
        pdf_writer.add_page(page)
    pdf_writer.write(output_name_file)


def method_pdf_is_locked(pdf_file):
    with open(pdf_file, 'rb') as file:
        pdf = PdfReader(file)
        return pdf.is_encrypted


def set_file_color(router):
    if method_pdf_is_locked(router):
        return "red"
    else:
        return "green"


class MainApplication(tk.Tk):
    list_pdf = []

    def __init__(self):
        super().__init__()
        width = "600"
        height = "250"
        self.geometry(width + "x" + height)
        self.title("BigPdf")

        self.toolbar = tk.Frame(self)
        self.toolbar.pack(side="top", fill="x")

        button_select_files = tk.Button(self.toolbar, text="Selecionar arquivos", command=self.select_files)
        button_select_files.pack(side="left")

        button_remove_files = tk.Button(self.toolbar, text="Remover arquivos", command=self.remove_files)
        button_remove_files.pack(side="left")

        button_display_passwords = tk.Button(self.toolbar, text="Gerenciar senhas", command=self.display_passwords)
        button_display_passwords.pack(side="left")

        button_unlock_pdf = tk.Button(self.toolbar, text="Desbloquear um PDF", command=self.unlock_pdf)
        button_unlock_pdf.pack(side="left")

        button_merge_pdf = tk.Button(self.toolbar, text="Unir PDFs", command=self.merge_pdfs)
        button_merge_pdf.pack(side="left")

        #button_remove_pages_pdf = tk.Button(self.toolbar, text="Apaga páginas", command=self.remove_pages_pdfs)
        #button_remove_pages_pdf.pack(side="left")

        self.list_files = Treeview(self, columns=('Nome',))
        self.list_files.heading('#0', text='Nome')
        self.list_files.column('#0', width=width)
        self.list_files.pack()

        self.mainloop()

    def remove_pages_pdfs(self):
        return 0

    def merge_pdfs(self):
        pdf_files = []
        pdf_readers = []
        selected_files = self.list_files.selection()
        for file in selected_files:
            if not self.is_lock(file):
                router_file = self.list_files.item(file)['text']
                if os.path.isfile(router_file):
                    try:
                        pdf_files.append(open(router_file, 'rb'))
                        pdf_readers.append(PyPDF2.PdfReader(router_file))
                        merged_pdf = PyPDF2.PdfWriter()
                        for pdf_reader in pdf_readers:
                            for page in range(len(pdf_reader.pages)):
                                merged_pdf.add_page(pdf_reader.pages[page])
                        self.remove_selection(file)
                    except Exception as e:
                        logging.exception(e)
                else:
                    print("Não é um arquivo")
            else:
                print("mensagem avisando que arquivo esta com senha")
        save_file = filedialog.asksaveasfile(mode='wb', defaultextension=".pdf")
        merged_pdf.write(save_file)
        for pdf_file in pdf_files:
            pdf_file.close()
        save_file.close()


    def is_lock(self, pdf_selected):
        pdf_file = self.list_files.item(pdf_selected)['text']
        return method_pdf_is_locked(pdf_file)

    def decrypt(self, pdf_file, password):
        router_file = self.list_files.item(pdf_file)['text']
        if os.path.isfile(router_file):
            try:
                with open(router_file, 'rb') as file:
                    pdf = PdfReader(file)
                    if pdf.decrypt(password):
                        write_unlocked_pdf(pdf, router_file)
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

    def unlock_pdf(self):
        files_selected = self.list_files.selection()
        with open("senhas.txt", 'r') as password_file:
            passwords = password_file.read().splitlines()
        for file in files_selected:
            if self.is_lock(file):
                for password in passwords:
                    if self.decrypt(file, password):
                        self.list_files.item(file, tags="green")
                        self.apply_pdf_color("green")
                        self.remove_selection(file)
                        break
                    else:
                        self.remove_selection(file)
                        print("unlock_pdf: Provavelmente não tem senha para esse pdf")
                else:
                    print("unlock_pdf: Realmente nao tem senha pra ele")
                    self.remove_selection(file)
            else:
                self.remove_selection(file)

    def display_passwords(self):
        PasswordWindow(self)

    def remove_selection(self, file):
        self.list_files.selection_remove(file)

    def apply_pdf_color(self, color_selected):
        if color_selected == "green":
            self.list_files.tag_configure("green", background="#00FF00")
        else:
            self.list_files.tag_configure("red", background="#ff5863")

    def select_files(self):
        selected_files = tk.filedialog.askopenfilenames(filetypes=[("Arquivos PDF", "*.pdf")])
        for file in selected_files:
            if file not in self.list_pdf:
                self.list_pdf.append(file)
                tag_color = set_file_color(file)
                self.list_files.insert('', 'end', text=file, tags=tag_color)
                self.apply_pdf_color(tag_color)
            else:
                messagebox.showerror("Erro", "O file {} já existe na lista".format(file))

    def remove_files(self):
        selected_files = self.list_files.selection()
        for file in selected_files:
            self.list_pdf.remove(self.list_files.item(file)['text'])
            self.list_files.delete(file)


if __name__ == "__main__":
    app = MainApplication()
