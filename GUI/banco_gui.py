import tkinter as tk
from tkinter import messagebox, simpledialog
import requests

API_URL_BANCO = "http://127.0.0.1:5000/trabalhopav/bancos"
API_URL_CLIENTE = "http://127.0.0.1:5000/trabalhopav/clientes"

class AcademicSystemApp:
    def __init__(self, root):

        self.root = root
        self.root.title("Todos os Bancos")
        self.root.geometry("760x850")
        self.root.configure(bg="#f5f6fa")
        self.root.resizable(False, False)

        self.setup_ui()

    def setup_ui(self):

        # ===== TITLE =====
        title = tk.Label(
            self.root,
            text="Tela de Bancos",
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

        # ===== DINHEIRO =====
        lbl_dinheiro = tk.Label(
            form_frame,
            text="Dinheiro:",
            font=("Segoe UI", 14, "bold"),
            bg="#f5f6fa",
            fg="#2d3436"
        )
        lbl_dinheiro.grid(row=2, column=0, sticky="w", pady=10)
        
        self.entry_dinheiro = tk.Entry(
            form_frame,
            font=("Segoe UI", 13),
            relief="solid",
            bd=1,
            width=35
        )
        self.entry_dinheiro.grid(row=2, column=1, padx=20, pady=10, ipady=8)

        # ===== SENHA =====
        lbl_senha = tk.Label(
            form_frame,
            text="Senha:",
            font=("Segoe UI", 14, "bold"),
            bg="#f5f6fa",
            fg="#2d3436"
        )
        lbl_senha.grid(row=3, column=0, sticky="w", pady=10)

        self.entry_senha = tk.Entry(
            form_frame,
            font=("Segoe UI", 13),
            relief="solid",
            bd=1,
            width=35
        )
        self.entry_senha.grid(row=3, column=1, padx=20, pady=10, ipady=8)

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
        self.entry_dinheiro.delete(0, tk.END)
        self.entry_senha.delete(0, tk.END)

    def call_api_get(self):

        id_banco = self.entry_id.get()

        if not id_banco:
            messagebox.showwarning("Aviso", "Informe o ID do banco")
            return

        id_cliente = self.get_cliente(id_banco)
        #messagebox.showinfo("Info", f"ID do cliente: {id_cliente}")

        if not self.cliente_publico(id_cliente):
            #messagebox.showwarning("Aviso", "Cliente não é público. Não é possível buscar o banco.")
            if not self.pede_senha(id_banco):
                #messagebox.showwarning("Aviso", "Senha incorreta. Não é possível buscar o banco.")
                return

        try:
            response = requests.get(f"{API_URL_BANCO}/{id_banco}")

            if response.status_code == 200:
                data = response.json()

                self.entry_cliente.delete(0, tk.END)
                self.entry_cliente.insert(0, data.get("id_cliente", ""))

                self.entry_dinheiro.delete(0, tk.END)
                self.entry_dinheiro.insert(0, data.get("dinheiro", ""))

                self.entry_senha.delete(0, tk.END)
                self.entry_senha.insert(0, data.get("senha", ""))

            else:
                messagebox.showerror("Erro", "Banco não encontrado")

        except Exception as e:
            messagebox.showerror("Erro", str(e))

    def call_api_post(self):

        try:
            data = {
                "id_cliente": self.entry_cliente.get(),
                "dinheiro": self.entry_dinheiro.get(),
                "senha": self.entry_senha.get()
            }

            response = requests.post(API_URL_BANCO, data=data)

            if response.status_code in [200, 201]:
                messagebox.showinfo("Sucesso", "Banco cadastrado com sucesso")
                self.clear_fields()
            else:
                messagebox.showerror("Erro", response.text)

        except Exception as e:
            messagebox.showerror("Erro", str(e))

    def call_api_put(self):
        id_cliente = self.get_cliente(self.entry_id.get())
        
        if not self.cliente_publico(id_cliente):
            messagebox.showwarning("Aviso", "Cliente não é público. Não é possível buscar o banco.")
            if not self.pede_senha(self.entry_id.get()):
                messagebox.showwarning("Aviso", "Senha incorreta. Não é possível buscar o banco.")
                return

        try:
            id_banco = self.entry_id.get()

            data = {
                "id_cliente": self.entry_cliente.get(),
                "dinheiro": self.entry_dinheiro.get(),
                "senha": self.entry_senha.get()
            }

            response = requests.put(f"{API_URL_BANCO}/{id_banco}", data=data)

            if response.status_code in [200, 201]:
                messagebox.showinfo("Sucesso", "Banco atualizado com sucesso")
                self.clear_fields()
            else:
                messagebox.showerror("Erro", response.text)

        except Exception as e:
            messagebox.showerror("Erro", str(e))

    def call_api_delete(self):

        id_banco = self.entry_id.get()

        if not id_banco:
            messagebox.showwarning("Aviso", "Informe o ID do banco")
            return

        id_cliente = self.get_cliente(id_banco)
        #messagebox.showinfo("Info", "id do cliente sendo pego")

        if not self.cliente_publico(id_cliente):
            #messagebox.showwarning("Aviso", "Cliente não é público. Não é possível remover o banco.")
            if not self.pede_senha(id_banco):
                return

        try:
            response = requests.delete(f"{API_URL_BANCO}/{id_banco}")

            if response.status_code == 200:
                messagebox.showinfo("Sucesso", "Banco removido com sucesso")
                self.clear_fields()
            else:
                messagebox.showerror("Erro", response.text)

        except Exception as e:
            messagebox.showerror("Erro", str(e))

    def cliente_publico(self, cliente_id):
        response = requests.get(f"{API_URL_CLIENTE}/{cliente_id}", timeout=5)
        cliente = response.json()

        if "dados_publicos" not in cliente:
            messagebox.showerror("Erro", "Campo 'dados_publicos' não encontrado na resposta da API")
            return False

        if (cliente["dados_publicos"] == True):
            #messagebox.showwarning("True", "só")
            return True
        if (cliente["dados_publicos"] == False):
            #messagebox.showwarning("False", "só")
            return False
        
        messagebox.showerror("Putz", "nao deveria chegar aqui, mas chegou")
        return False

    def get_cliente(self, banco_id):
        response = requests.get(f"{API_URL_BANCO}/{banco_id}", timeout=5)
        banco = response.json()
        cliente_id = banco.get("id_cliente")

        if not cliente_id:
            messagebox.showerror("Erro", "Campo 'id_cliente' não encontrado na resposta da API")
            return None

        #messagebox.showinfo("Info", f"Cliente ID: {cliente_id}")
        return cliente_id
    
    def pede_senha(self, banco_id):
            senha_digitada = simpledialog.askstring(
                "Senha", 
                "Digite a senha do cliente ", 
                show="*",
                parent=self.root)
            response1 = requests.get(f"{API_URL_BANCO}/{banco_id}",timeout=5)
            if response1.status_code != 200:
                messagebox.showerror("Erro", "Falha ao obter banco.")
                return False
            object1 = response1.json()
            senha_correta = object1.get("senha")
            if senha_digitada == senha_correta:
                messagebox.showinfo("Sucesso", "Senha correta. Acesso permitido.")
                return True
            else:
                messagebox.showerror("Erro", "Senha incorreta. Acesso negado.")
                return False

if __name__ == "__main__":

    root = tk.Tk()

    app = AcademicSystemApp(root)

    root.mainloop()