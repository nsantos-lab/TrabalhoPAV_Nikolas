import tkinter as tk
from tkinter import messagebox
import requests

API_URL = "http://127.0.0.1:5000/trabalhopav/ambientes"

class AcademicSystemApp:
    def __init__(self, root):

        self.root = root
        self.root.title("Todos os Ambientes")
        self.root.geometry("760x850")
        self.root.configure(bg="#f5f6fa")
        self.root.resizable(False, False)

        self.setup_ui()

    def setup_ui(self):

        # ===== TITLE =====
        title = tk.Label(
            self.root,
            text="Tela de Ambiente",
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

        # ===== CLIENTE =====
        lbl_cliente = tk.Label(
            form_frame,
            text="Cliente:",
            font=("Segoe UI", 14, "bold"),
            bg="#f5f6fa",
            fg="#2d3436"
        )
        lbl_cliente.grid(row=1, column=0, sticky="w", pady=10)

        self.entry_cliente = tk.Entry(
            form_frame,
            font=("Segoe UI", 13),
            relief="solid",
            bd=1,
            width=35
        )
        self.entry_cliente.grid(row=1, column=1, padx=20, pady=10, ipady=8)

        # ===== OXIGENIO =====
        lbl_oxigenio = tk.Label(
            form_frame,
            text="Oxigênio:",
            font=("Segoe UI", 14, "bold"),
            bg="#f5f6fa",
            fg="#2d3436"
        )
        lbl_oxigenio.grid(row=2, column=0, sticky="w", pady=10)
        
        self.entry_oxigenio = tk.Entry(
            form_frame,
            font=("Segoe UI", 13),
            relief="solid",
            bd=1,
            width=35
        )
        self.entry_oxigenio.grid(row=2, column=1, padx=20, pady=10, ipady=8)

        # ===== CARBONICO =====
        lbl_carbonico = tk.Label(
            form_frame,
            text="Carbonico:",
            font=("Segoe UI", 14, "bold"),
            bg="#f5f6fa",
            fg="#2d3436"
        )
        lbl_carbonico.grid(row=3, column=0, sticky="w", pady=10)

        self.entry_carbonico = tk.Entry(
            form_frame,
            font=("Segoe UI", 13),
            relief="solid",
            bd=1,
            width=35
        )
        self.entry_carbonico.grid(row=3, column=1, padx=20, pady=10, ipady=8)

                # ===== POLUENTES =====
        lbl_poluentes = tk.Label(
            form_frame,
            text="Poluentes:",
            font=("Segoe UI", 14, "bold"),
            bg="#f5f6fa",
            fg="#2d3436"
        )
        lbl_poluentes.grid(row=4, column=0, sticky="w", pady=10)

        self.entry_poluentes = tk.Entry(
            form_frame,
            font=("Segoe UI", 13),
            relief="solid",
            bd=1,
            width=35
        )
        self.entry_poluentes.grid(row=4, column=1, padx=20, pady=10, ipady=8)

        # ===== UMIDADE =====
        lbl_umidade = tk.Label(
            form_frame,
            text="Umidade:",
            font=("Segoe UI", 14, "bold"),
            bg="#f5f6fa",
            fg="#2d3436"
        )
        lbl_umidade.grid(row=5, column=0, sticky="w", pady=10)

        self.entry_umidade = tk.Entry(
            form_frame,
            font=("Segoe UI", 13),
            relief="solid",
            bd=1,
            width=35
        )
        self.entry_umidade.grid(row=5, column=1, padx=20, pady=10, ipady=8)

        # ===== DENSIDADE =====
        lbl_densidade = tk.Label(
            form_frame,
            text="Densidade:",
            font=("Segoe UI", 14, "bold"),
            bg="#f5f6fa",
            fg="#2d3436"
        )
        lbl_densidade.grid(row=6, column=0, sticky="w", pady=10)

        self.entry_densidade = tk.Entry(
            form_frame,
            font=("Segoe UI", 13),
            relief="solid",
            bd=1,
            width=35
        )
        self.entry_densidade.grid(row=6, column=1, padx=20, pady=10, ipady=8)

                # ===== DADOS_PUBLICOS =====
        lbl_dados_publicos = tk.Label(
            form_frame,
            text="Dados Públicos:",
            font=("Segoe UI", 14, "bold"),
            bg="#f5f6fa",
            fg="#2d3436"
        )
        lbl_dados_publicos.grid(row=7, column=0, sticky="w", pady=10)

        self.entry_dados_publicos = tk.Entry(
            form_frame,
            font=("Segoe UI", 13),
            relief="solid",
            bd=1,
            width=35
        )
        self.entry_dados_publicos.grid(row=7, column=1, padx=20, pady=10, ipady=8)

        # ===== DATA_CADASTRO =====
        lbl_data_cadastro = tk.Label(
            form_frame,
            text="Data de Cadastro:",
            font=("Segoe UI", 14, "bold"),
            bg="#f5f6fa",
            fg="#2d3436"
        )
        lbl_data_cadastro.grid(row=8, column=0, sticky="w", pady=10)

        self.entry_data_cadastro = tk.Entry(
            form_frame,
            font=("Segoe UI", 13),
            relief="solid",
            bd=1,
            width=35
        )
        self.entry_data_cadastro.grid(row=8, column=1, padx=20, pady=10, ipady=8)

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
        self.entry_cliente.delete(0, tk.END)
        self.entry_oxigenio.delete(0, tk.END)
        self.entry_carbonico.delete(0, tk.END)
        self.entry_poluentes.delete(0, tk.END)
        self.entry_umidade.delete(0, tk.END)
        self.entry_densidade.delete(0, tk.END)
        self.entry_dados_publicos.delete(0, tk.END)
        self.entry_data_cadastro.delete(0, tk.END)

    def call_api_get(self):

        ambiente_id = self.entry_id.get()

        if not ambiente_id:
            messagebox.showwarning("Aviso", "Informe o ID do ambiente")
            return

        try:
            response = requests.get(f"{API_URL}/{ambiente_id}")

            if response.status_code == 200:
                data = response.json()

                self.entry_cliente.delete(0, tk.END)
                self.entry_cliente.insert(0, data.get("cliente", ""))

                self.entry_oxigenio.delete(0, tk.END)
                self.entry_oxigenio.insert(0, data.get("oxigenio", ""))

                self.entry_carbonico.delete(0, tk.END)
                self.entry_carbonico.insert(0, data.get("carbonico", ""))

                self.entry_poluentes.delete(0, tk.END)
                self.entry_poluentes.insert(0, data.get("poluentes", ""))

                self.entry_umidade.delete(0, tk.END)
                self.entry_umidade.insert(0, data.get("umidade", ""))

                self.entry_densidade.delete(0, tk.END)
                self.entry_densidade.insert(0, data.get("densidade", ""))

                self.entry_dados_publicos.delete(0, tk.END)
                self.entry_dados_publicos.insert(0, data.get("dados_publicos", ""))

                self.entry_data_cadastro.delete(0, tk.END)
                self.entry_data_cadastro.insert(0, data.get("data_cadastro", ""))

            else:
                messagebox.showerror("Erro", "Ambiente não encontrado")

        except Exception as e:
            messagebox.showerror("Erro", str(e))

    def call_api_post(self):

        try:
            data = {
                "cliente": self.entry_cliente.get(),
                "oxigenio": self.entry_oxigenio.get(),
                "carbonico": self.entry_carbonico.get(),
                "poluentes": self.entry_poluentes.get(),
                "umidade": self.entry_umidade.get(),
                "densidade": self.entry_densidade.get(),
                "dados_publicos": self.entry_dados_publicos.get()
            }

            response = requests.post(API_URL, data=data)

            if response.status_code in [200, 201]:
                messagebox.showinfo("Sucesso", "Ambiente cadastrado com sucesso")
                self.clear_fields()
            else:
                messagebox.showerror("Erro", response.text)

        except Exception as e:
            messagebox.showerror("Erro", str(e))

    def call_api_put(self):

        try:
            ambiente_id = self.entry_id.get()

            data = {
                "cliente": self.entry_cliente.get(),
                "oxigenio": self.entry_oxigenio.get(),
                "carbonico": self.entry_carbonico.get(),
                "poluentes": self.entry_poluentes.get(),
                "umidade": self.entry_umidade.get(),
                "densidade": self.entry_densidade.get(),
                "dados_publicos": self.entry_dados_publicos.get()
            }

            response = requests.put(f"{API_URL}/{ambiente_id}", data=data)

            if response.status_code in [200, 201]:
                messagebox.showinfo("Sucesso", "Ambiente atualizado com sucesso")
                self.clear_fields()
            else:
                messagebox.showerror("Erro", response.text)

        except Exception as e:
            messagebox.showerror("Erro", str(e))

    def call_api_delete(self):

        ambiente_id = self.entry_id.get()

        if not ambiente_id:
            messagebox.showwarning("Aviso", "Informe o ID do ambiente")
            return

        try:
            response = requests.delete(f"{API_URL}/{ambiente_id}")

            if response.status_code == 200:
                messagebox.showinfo("Sucesso", "Ambiente removido com sucesso")
                self.clear_fields()
            else:
                messagebox.showerror("Erro", response.text)

        except Exception as e:
            messagebox.showerror("Erro", str(e))


if __name__ == "__main__":

    root = tk.Tk()

    app = AcademicSystemApp(root)

    root.mainloop()