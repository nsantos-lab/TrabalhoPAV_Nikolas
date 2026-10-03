import tkinter as tk
import tkinter as tk
from tkinter import messagebox
import requests


API_URL = "http://localhost:8080/academico/alunos"


class AcademicSystemApp:

    def __init__(self, root):

        self.root = root
        self.root.title("Sistema Acadêmico")
        self.root.geometry("760x480")
        self.root.configure(bg="#f5f6fa")
        self.root.resizable(False, False)

        self.setup_ui()

    def setup_ui(self):

        # ===== TITLE =====
        title = tk.Label(
            self.root,
            text="Tela de Aluno",
            font=("Segoe UI", 28, "bold"),
            bg="#f5f6fa",
            fg="#2d3436"
        )
        title.pack(pady=(25, 20))

        # ===== FORM FRAME =====
        form_frame = tk.Frame(self.root, bg="#f5f6fa")
        form_frame.pack(padx=40, fill="x")

        # ===== ID =====
        lbl_id = tk.Label(
            form_frame,
            text="ID:",
            font=("Segoe UI", 14, "bold"),
            bg="#f5f6fa",
            fg="#2d3436"
        )
        lbl_id.grid(row=0, column=0, sticky="w", pady=10)

        self.entry_id = tk.Entry(
            form_frame,
            font=("Segoe UI", 13),
            relief="solid",
            bd=1,
            width=35
        )
        self.entry_id.grid(row=0, column=1, padx=20, pady=10, ipady=8)

        # ===== NOME =====
        lbl_nome = tk.Label(
            form_frame,
            text="Nome:",
            font=("Segoe UI", 14, "bold"),
            bg="#f5f6fa",
            fg="#2d3436"
        )
        lbl_nome.grid(row=1, column=0, sticky="w", pady=10)

        self.entry_nome = tk.Entry(
            form_frame,
            font=("Segoe UI", 13),
            relief="solid",
            bd=1,
            width=35
        )
        self.entry_nome.grid(row=1, column=1, padx=20, pady=10, ipady=8)

        # ===== MATRICULA =====
        lbl_matricula = tk.Label(
            form_frame,
            text="Matrícula:",
            font=("Segoe UI", 14, "bold"),
            bg="#f5f6fa",
            fg="#2d3436"
        )
        lbl_matricula.grid(row=2, column=0, sticky="w", pady=10)
        
        self.entry_matricula = tk.Entry(
            form_frame,
            font=("Segoe UI", 13),
            relief="solid",
            bd=1,
            width=35
        )
        self.entry_matricula.grid(row=2, column=1, padx=20, pady=10, ipady=8)

        # ===== BUTTON FRAME =====
        button_frame = tk.Frame(self.root, bg="#f5f6fa")
        button_frame.pack(pady=30)

        self.create_button(
            button_frame,
            "Excluir",
            "#d63031",
            self.call_api_delete
        ).grid(row=0, column=0, padx=8)

        self.create_button(
            button_frame,
            "Editar",
            "#e17055",
            self.call_api_put
        ).grid(row=0, column=1, padx=8)

        self.create_button(
            button_frame,
            "Cadastrar",
            "#0984e3",
            self.call_api_post
        ).grid(row=0, column=2, padx=8)

        self.create_button(
            button_frame,
            "Buscar",
            "#6c5ce7",
            self.call_api_get
        ).grid(row=0, column=3, padx=8)

        # ===== CLEAR BUTTON =====
        clear_frame = tk.Frame(self.root, bg="#f5f6fa")
        clear_frame.pack()

        self.create_button(
            clear_frame,
            "Limpar",
            "#636e72",
            self.clear_fields
        ).pack()

    def create_button(self, parent, text, color, command):

        button = tk.Button(
            parent,
            text=text,
            command=command,
            font=("Segoe UI", 12, "bold"),
            bg=color,
            fg="white",
            activebackground=color,
            activeforeground="white",
            relief="flat",
            cursor="hand2",
            width=12,
            height=2,
            bd=0
        )

        return button

    def clear_fields(self):

        self.entry_id.delete(0, tk.END)
        self.entry_nome.delete(0, tk.END)
        self.entry_matricula.delete(0, tk.END)

    def call_api_get(self):

        aluno_id = self.entry_id.get()

        if not aluno_id:
            messagebox.showwarning("Aviso", "Informe o ID do aluno")
            return

        try:
            response = requests.get(f"{API_URL}/{aluno_id}")

            if response.status_code == 200:
                data = response.json()

                self.entry_nome.delete(0, tk.END)
                self.entry_nome.insert(0, data.get("nome", ""))

                self.entry_matricula.delete(0, tk.END)
                self.entry_matricula.insert(0, data.get("matricula", ""))

            else:
                messagebox.showerror("Erro", "Aluno não encontrado")

        except Exception as e:
            messagebox.showerror("Erro", str(e))

    def call_api_post(self):

        try:
            data = {
                "id": int(self.entry_id.get()),
                "nome": self.entry_nome.get(),
                "matricula": self.entry_matricula.get(),
            }

            response = requests.post(API_URL, data=data)

            if response.status_code in [200, 201]:
                messagebox.showinfo("Sucesso", "Aluno cadastrado com sucesso")
                self.clear_fields()
            else:
                messagebox.showerror("Erro", response.text)

        except Exception as e:
            messagebox.showerror("Erro", str(e))

    def call_api_put(self):

        try:
            aluno_id = self.entry_id.get()

            data = {
                "nome": self.entry_nome.get(),
                "matricula": self.entry_matricula.get(),
            }

            response = requests.put(f"{API_URL}/{aluno_id}", data=data)

            if response.status_code in [200, 201]:
                messagebox.showinfo("Sucesso", "Aluno atualizado com sucesso")
                self.clear_fields()
            else:
                messagebox.showerror("Erro", response.text)

        except Exception as e:
            messagebox.showerror("Erro", str(e))

    def call_api_delete(self):

        aluno_id = self.entry_id.get()

        if not aluno_id:
            messagebox.showwarning("Aviso", "Informe o ID do aluno")
            return

        try:
            response = requests.delete(f"{API_URL}/{aluno_id}")

            if response.status_code == 200:
                messagebox.showinfo("Sucesso", "Aluno removido com sucesso")
                self.clear_fields()
            else:
                messagebox.showerror("Erro", response.text)

        except Exception as e:
            messagebox.showerror("Erro", str(e))


if __name__ == "__main__":

    root = tk.Tk()

    app = AcademicSystemApp(root)

    root.mainloop()