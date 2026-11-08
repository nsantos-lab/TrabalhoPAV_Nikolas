import tkinter as tk
from tkinter import messagebox, simpledialog, ttk
import requests

if __package__:
    from .ambiente_tempo_tab import AmbienteTempoTab
    from .ambientes_tab import AmbientesTab
    from .bancos_tab import BancosTab
    from .clientes_tab import ClientesTab
    from .api_urls import API_URL_AMBIENTE, API_URL_AMBIENTE_TEMPO, API_URL_BANCO, API_URL_BANCO_BY_CLIENTE, API_URL_CLIENTE
    from .produtos_tab import build_produtos_tab
else:
    from ambiente_tempo_tab import AmbienteTempoTab
    from ambientes_tab import AmbientesTab
    from bancos_tab import BancosTab
    from clientes_tab import ClientesTab
    from api_urls import API_URL_AMBIENTE, API_URL_AMBIENTE_TEMPO, API_URL_BANCO, API_URL_BANCO_BY_CLIENTE, API_URL_CLIENTE
    from produtos_tab import build_produtos_tab


class AcademicSystemApp(ClientesTab, BancosTab, AmbientesTab, AmbienteTempoTab):
    def __init__(self, root):

        self.root = root
        self.root.title("Trabalho PAV")
        self.root.geometry("780x640")
        self.root.configure(bg="#f5f6fa")
        self.root.resizable(False, False)

        self.setup_ui()

    def criar_campo(self, pai, texto, linha, coluna):
        tk.Label(
        pai,
        text=texto,
        font=("Segoe UI", 10, "bold"),
        bg="#f5f6fa",
        fg="#2d3436"
        ).grid(row=linha, column=coluna, sticky="w")

        campo = tk.Entry(pai, font=("Segoe UI", 10), width=35)
        campo.grid(row=linha, column=coluna + 1, padx=20)
        return campo

    def setup_ui(self):
        notebook = ttk.Notebook(self.root)
        notebook.pack(fill="both", expand=True)

        self.build_clientes_tab(notebook)
        self.build_bancos_tab(notebook)
        self.build_ambientes_tab(notebook)
        build_produtos_tab(notebook)
        self.build_ambiente_tempo_tab(notebook)

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
            height=0,
            bd=0
        )

        return button

    def get_cliente_banco(self, banco_id):
        response = requests.get(f"{API_URL_BANCO}/{banco_id}", timeout=5)
        banco = response.json()
        cliente_id = banco.get("id_cliente")

        if not cliente_id:
            messagebox.showerror("Erro", "Campo 'id_cliente' não encontrado na resposta da API")
            return None

        #messagebox.showinfo("Info", f"Cliente ID: {cliente_id}")
        return cliente_id

    def get_cliente_ambiente(self, ambiente_id):
        response = requests.get(f"{API_URL_AMBIENTE}/{ambiente_id}", timeout=5)
        ambiente = response.json()
        cliente_id = ambiente.get("cliente")

        if not cliente_id:
            #messagebox.showerror("Erro", "Campo 'id_cliente' não encontrado na resposta da API")
            return None

        #messagebox.showinfo("Info", f"Cliente ID: {cliente_id}")
        return cliente_id

    def get_banco_cliente(self, cliente_id):
        response = requests.get(f"{API_URL_BANCO_BY_CLIENTE}/{cliente_id}")
        banco = response.json()
        banco_id = banco.get("id_banco")
        #messagebox.showinfo("aviso", f"Banco ID: {banco_id}")
        return banco_id

    def get_ambiente_ambiente_tempo(self, id_ambiente_tempo):
        response = requests.get(f"{API_URL_AMBIENTE_TEMPO}/{id_ambiente_tempo}",timeout=5)
        ambiente_tempo = response.json()
        ambiente_id = ambiente_tempo.get("ambiente")
        #messagebox.showwarning("Aviso", "Ambiente ID: " + str(ambiente_id))
        return ambiente_id

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

    def ambiente_publico(self, ambiente_id):
        response = requests.get(f"{API_URL_AMBIENTE}/{ambiente_id}",timeout=5)
        ambiente = response.json()

        if "dados_publicos" not in ambiente:
            messagebox.showerror("Erro", "Campo 'dados_publicos' não encontrado na resposta da API")
            return False

        if (ambiente["dados_publicos"] == True):
            #messagebox.showwarning("True", "só")
            return True
        if (ambiente["dados_publicos"] == False):
            #messagebox.showwarning("False", "só")
            return False
        
        messagebox.showerror("Putz", "nao deveria chegar aqui, mas chegou")
        return False

    def pede_senha(self, banco_id):
        response1 = requests.get(f"{API_URL_BANCO}/{banco_id}",timeout=5)
        if response1.status_code != 200:
            messagebox.showerror("Erro", "Falha ao obter banco.")
            return True
        object1 = response1.json()
        senha_correta = object1.get("senha")
        senha_digitada = simpledialog.askstring(
            "Senha",
            "Digite a senha do cliente ",
            show="*",
            parent=self.root)
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
