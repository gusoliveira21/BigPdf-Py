import tkinter as tk
from tkinter import filedialog, messagebox


class PasswordWindow(tk.Toplevel):

    def __init__(self, master):
        super().__init__(master)
        self.geometry("300x200")
        self.title("Senhas")

        self.toolbar = tk.Frame(self)
        self.toolbar.pack(side="top", fill="x")

        button_add_password = tk.Button(self.toolbar, text="Adicionar", command=self.add_password)
        button_add_password.pack(side="left")

        button_remove_password = tk.Button(self.toolbar, text="Excluir", command=self.remove_password)
        button_remove_password.pack(side="left")

        self.show_psswd = tk.Listbox(self, width=200, height=200, selectmode="single")
        self.show_psswd.pack()

        self.show_passwords()

    def show_passwords(self):
        self.clean_list_window()
        with open("senhas.txt", "r") as file:
            for password in file:
                self.show_psswd.insert(tk.END, password.strip())

    def clean_list_window(self):
        self.show_psswd.delete(0, tk.END)

    def add_password(self):
        psswd_string = tk.simpledialog.askstring("Senhas", "Digite as senhas, separadas por vírgula:")
        psswd = psswd_string.split(',')
        if psswd:
            with open("senhas.txt", "a") as file:
                for password in psswd:
                    file.write(password.strip() + "\n")
            self.show_passwords()
        else:
            messagebox.showerror("Erro", "Nenhuma senha inserida")

    def remove_password(self):
        index = self.show_psswd.curselection()

        if index:
            self.show_psswd.delete(index)

            with open("senhas.txt", "w") as file:
                senhas = self.show_psswd.get(0, tk.END)
                for senha in senhas:
                    file.write(senha + "\n")
        else:
            messagebox.showerror("Erro", "Nenhuma senha selecionada para excluir")
