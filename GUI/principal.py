import tkinter as tk
from tkinter import messagebox, simpledialog, ttk
import requests

API_URL_CLIENTE = "http://127.0.0.1:5000/trabalhopav/clientes"
API_URL_BANCO = "http://127.0.0.1:5000/trabalhopav/bancos"
API_URL_BANCO_BY_CLIENTE = "http://127.0.0.1:5000/trabalhopav/bancos/cliente"
API_URL_AMBIENTE = "http://127.0.0.1:5000/trabalhopav/ambientes"

class AcademicSystemApp:
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

        # ==== ABAS =====
        notebook = ttk.Notebook(self.root)
        notebook.pack(fill="both", expand=True)

        aba_clientes = tk.Frame(notebook, bg="#f5f6fa")
        aba_bancos = tk.Frame(notebook, bg="#f5f6fa")
        aba_ambientes = tk.Frame(notebook, bg="#f5f6fa")
        aba_produtos = tk.Frame(notebook, bg="#f5f6fa")
        aba_ambiente_tempo = tk.Frame(notebook, bg="#f5f6fa")

        notebook.add(aba_clientes, text="Clientes")
        notebook.add(aba_bancos, text="Bancos")
        notebook.add(aba_ambientes, text="Ambientes")
        notebook.add(aba_produtos, text="Produtos")
        notebook.add(aba_ambiente_tempo, text="Ambiente Tempo")

        # ======== CLIENTE ========
        # ===== TITLE CLIENTE =====
        title = tk.Label(
            aba_clientes,
            text="Clientes",
            font=("Segoe UI", 14, "bold"),
            bg="#f5f6fa",
            fg="#2d3436"
        )
        title.pack(pady=(5, 10))

        # ===== FORM FRAME CLIENTE =====
        form_frame_cliente = tk.Frame(aba_clientes, bg="#f5f6fa")
        form_frame_cliente.pack(padx=20, fill="x")

        # ===== ID =====
        self.entry_id_cliente = self.criar_campo(form_frame_cliente, "ID:", 0, 0)

        # ===== NOME =====
        self.entry_nome = self.criar_campo(form_frame_cliente, "Nome:", 1, 0)

        # ===== CPF =====
        self.entry_cpf = self.criar_campo(form_frame_cliente, "CPF:", 2, 0)

        # ===== EMAIL =====
        self.entry_email = self.criar_campo(form_frame_cliente, "Email:", 3, 0)

        # ===== TELEFONE =====
        self.entry_telefone = self.criar_campo(form_frame_cliente, "Telefone:", 0, 3)
        
        # ===== DADOS_PUBLICOS =====
        self.entry_dados_publicos_cliente = self.criar_campo(form_frame_cliente, "Dados Públicos:", 1, 3)

        # ===== DATA_NASCIMENTO =====
        self.entry_data_nascimento = self.criar_campo(form_frame_cliente, "Nascimento:", 2, 3)

        # ===== DATA_CADASTRO =====
        self.entry_data_cadastro_cliente = self.criar_campo(form_frame_cliente, "Data de Cadastro:", 3, 3)

        # ===== BUTTON FRAME CLIENTES=====
        button_frame_clientes = tk.Frame(aba_clientes, bg="#f5f6fa")
        button_frame_clientes.pack(pady=30)

        # ==== DELETE CLIENTES BUTTON ====
        self.create_button(
            button_frame_clientes,
            "Excluir",
            "#d63031",
            self.call_api_delete_cliente
        ).grid(row=0, column=0, padx=0)

        # ==== PUT CLIENTES BUTTON ====
        self.create_button(
            button_frame_clientes,
            "Editar",
            "#e17055",
            self.call_api_put_cliente
        ).grid(row=0, column=1, padx=0)

        # ==== POST CLIENTES BUTTON ====
        self.create_button(
            button_frame_clientes,
            "Cadastrar",
            "#0984e3",
            self.call_api_post_cliente
        ).grid(row=0, column=2, padx=0)

        # ==== GET CLIENTES BUTTON ====
        self.create_button(
            button_frame_clientes,
            "Buscar",
            "#6c5ce7",
            self.call_api_get_cliente
        ).grid(row=0, column=3, padx=0)

        # ===== CLEAR CLIENTES BUTTON =====
        self.create_button(
            button_frame_clientes,
            "Limpar",
            "#636e72",
            self.clear_fields_cliente
        ).grid(row=0, column=4, padx=0)

        # ==== CLIENT LIST FRAME =====
        client_list_frame = tk.Frame(aba_clientes, bg="#f5f6fa")
        client_list_frame.pack(padx=20, fill="both", expand=True)

        tk.Label(
            client_list_frame,
            text="Clientes cadastrados",
            font=("Segoe UI", 10, "bold"),
            bg="#f5f6fa",
            fg="#2d3436"
        ).pack(anchor="w", pady=(0, 5))

        columns = ("id", "nome", "cpf", "email", "telefone", "dados_publicos", "nascimento", "data_cadastro")
        self.client_list = ttk.Treeview(
            client_list_frame,
            columns=columns,
            show="headings",
            height=12
        )
        self.client_list.heading("id", text="ID")
        self.client_list.heading("nome", text="Nome")
        self.client_list.heading("cpf", text="CPF")
        self.client_list.heading("email", text="Email")
        self.client_list.heading("telefone", text="Telefone")
        self.client_list.heading("dados_publicos", text="Públicos")
        self.client_list.heading("nascimento", text="Nascimento")
        self.client_list.heading("data_cadastro", text="Data de Cadastro")

        self.client_list.column("id", width=50, minwidth=0, stretch=False, anchor="center")
        self.client_list.column("nome", width=90, minwidth=0, stretch=False, anchor="center")
        self.client_list.column("cpf", width=75, minwidth=0, stretch=False, anchor="center")
        self.client_list.column("email", width=100)
        self.client_list.column("telefone", width=75, minwidth=0, stretch=False, anchor="center")
        self.client_list.column("dados_publicos", width=0, anchor="center")
        self.client_list.column("nascimento", width=75, minwidth=0, stretch=False, anchor="center")
        self.client_list.column("data_cadastro", width=50)
        client_scrollbar = tk.Scrollbar(
            client_list_frame,
            orient="vertical",
            command=self.client_list.yview
        )
        self.client_list.configure(yscrollcommand=client_scrollbar.set)
        self.client_list.pack(side="left", fill="both", expand=True)
        client_scrollbar.pack(side="right", fill="y")
        self.client_list.bind("<<ListboxSelect>>", self.select_client)

        self.create_button(
            aba_clientes,
            "Atualizar lista",
            "#00b894",
            self.load_clients
        ).pack(pady=(8, 15))

        self.root.after(100, self.load_clients)

        # ======== BANCO ========
        # ===== TITLE BANCO =====
        title = tk.Label(
            aba_bancos,
            text="Tela de Bancos",
            font=("Segoe UI", 14, "bold"),
            bg="#f5f6fa",
            fg="#2d3436"
        )
        title.pack(pady=(5, 10))

        # ===== FORM FRAME BANCO =====
        form_frame_banco = tk.Frame(aba_bancos, bg="#f5f6fa")
        form_frame_banco.pack(padx=20, fill="x")

        # ===== ID =====
        self.entry_id_banco = self.criar_campo(form_frame_banco, "ID:", 0, 0)

        # ===== CLIENTE =====
        self.entry_cliente_banco = self.criar_campo(form_frame_banco, "Cliente:", 1, 0)

        # ===== DINHEIRO =====
        self.entry_dinheiro = self.criar_campo(form_frame_banco, "Dinheiro:", 2, 0)

        # ===== SENHA =====
        self.entry_senha = self.criar_campo(form_frame_banco, "Senha:", 3, 0)

        # ===== BUTTON FRAME BANCOS=====
        button_frame_bancos = tk.Frame(aba_bancos, bg="#f5f6fa")
        button_frame_bancos.pack(pady=30)

        # ==== DELETE BANCOS BUTTON ====
        self.create_button(
            button_frame_bancos,
            "Excluir",
            "#d63031",
            self.call_api_delete_banco
        ).grid(row=0, column=0, padx=0)

        # ==== GET BANCOS BUTTON ====
        self.create_button(
            button_frame_bancos,
            "Editar",
            "#e17055",
            self.call_api_put_banco
        ).grid(row=0, column=1, padx=0)

        # ==== POST BANCOS BUTTON ====
        self.create_button(
            button_frame_bancos,
            "Cadastrar",
            "#0984e3",
            self.call_api_post_banco
        ).grid(row=0, column=2, padx=0)

        # ==== GET BANCOS BUTTON ====
        self.create_button(
            button_frame_bancos,
            "Buscar",
            "#6c5ce7",
            self.call_api_get_banco
        ).grid(row=0, column=3, padx=0)

        # ===== CLEAR BANCOS BUTTON =====
        self.create_button(
            button_frame_bancos,
            "Limpar",
            "#636e72",
            self.clear_fields_banco
        ).grid(row=0, column=4, padx=0)

        # =========================== #
        # ==== BANCO LIST FRAME ===== #
        banco_list_frame = tk.Frame(aba_bancos, bg="#f5f6fa")
        banco_list_frame.pack(padx=20, fill="both", expand=True)

        tk.Label(
            banco_list_frame,
            text="Bancos cadastrados",
            font=("Segoe UI", 10, "bold"),
            bg="#f5f6fa",
            fg="#2d3436"
        ).pack(anchor="w", pady=(0, 5))

        columns = ("id", "cliente", "dinheiro", "senha")
        self.banco_list = ttk.Treeview(
            banco_list_frame,
            columns=columns,
            show="headings",
            height=12
        )
        self.banco_list.heading("id", text="ID")
        self.banco_list.heading("cliente", text="Cliente")
        self.banco_list.heading("dinheiro", text="Dinheiro")
        self.banco_list.heading("senha", text="Senha")


        self.banco_list.column("id", width=5, anchor="center")
        self.banco_list.column("cliente", width=5, anchor="center")
        self.banco_list.column("dinheiro", width=35)
        self.banco_list.column("senha", width=20)
        
        banco_scrollbar = tk.Scrollbar(
            banco_list_frame,
            orient="vertical",
            command=self.banco_list.yview
        )
        self.banco_list.configure(yscrollcommand=banco_scrollbar.set)
        self.banco_list.pack(side="left", fill="both", expand=True)
        banco_scrollbar.pack(side="right", fill="y")
        self.banco_list.bind("<<ListboxSelect>>", self.select_banco)

        self.create_button(
            aba_bancos,
            "Atualizar lista",
            "#00b894",
            self.load_bancos
        ).pack(pady=(8, 15))

        self.root.after(100, self.load_bancos)

        # ======== AMBIENTE ========
        # ===== TITLE AMBIENTE =====
        title = tk.Label(
            aba_ambientes,
            text="Tela de Ambientes",
            font=("Segoe UI", 14, "bold"),
            bg="#f5f6fa",
            fg="#2d3436"
        )
        title.pack(pady=(5, 10))

        # ===== FORM FRAME AMBIENTE =====
        form_frame_ambiente = tk.Frame(aba_ambientes, bg="#f5f6fa")
        form_frame_ambiente.pack(padx=20, fill="x")

        # ===== ID =====
        self.entry_id_ambiente = self.criar_campo(form_frame_ambiente, "ID:", 0, 0)

        # ===== CLIENTE =====
        self.entry_cliente_ambiente = self.criar_campo(form_frame_ambiente, "Cliente:", 1, 0)

        # ===== OXIGENIO =====
        self.entry_oxigenio_ambiente = self.criar_campo(form_frame_ambiente, "Oxigenio:", 2, 0)

        # ===== CARBONICO =====
        self.entry_carbonico_ambiente = self.criar_campo(form_frame_ambiente, "Carbonico:", 3, 0)

        # ===== POLUENTES =====
        self.entry_poluentes_ambiente = self.criar_campo(form_frame_ambiente, "Poluentes:", 4, 0)

        # ===== UMIDADE =====
        self.entry_umidade_ambiente = self.criar_campo(form_frame_ambiente, "Umidade:", 0, 3)

        # ===== DENSIDADE =====
        self.entry_densidade_ambiente = self.criar_campo(form_frame_ambiente, "Densidade:", 1, 3)

        # ===== DADOS_PUBLICOS =====
        self.entry_dados_publicos_ambiente = self.criar_campo(form_frame_ambiente, "Dados Publicos:", 2, 3)

        # ===== DATA_CADASTRO =====
        self.entry_data_cadastro_ambiente = self.criar_campo(form_frame_ambiente, "Data Cadastro:", 3, 3)

        # ===== BUTTON FRAME AMBIENTES=====
        button_frame_ambientes = tk.Frame(aba_ambientes, bg="#f5f6fa")
        button_frame_ambientes.pack(pady=30)

        # ==== DELETE AMBIENTES BUTTON ====
        self.create_button(
            button_frame_ambientes,
            "Excluir",
            "#d63031",
            self.call_api_delete_ambiente
        ).grid(row=0, column=0, padx=0)

        # ==== GET AMBIENTES BUTTON ====
        self.create_button(
            button_frame_ambientes,
            "Editar",
            "#e17055",
            self.call_api_put_ambiente
        ).grid(row=0, column=1, padx=0)

        # ==== POST AMBIENTES BUTTON ====
        self.create_button(
            button_frame_ambientes,
            "Cadastrar",
            "#0984e3",
            self.call_api_post_ambiente
        ).grid(row=0, column=2, padx=0)

        # ==== GET AMBIENTES BUTTON ====
        self.create_button(
            button_frame_ambientes,
            "Buscar",
            "#6c5ce7",
            self.call_api_get_ambiente
        ).grid(row=0, column=3, padx=0)

        # ===== CLEAR AMBIENTES BUTTON =====
        self.create_button(
            button_frame_ambientes,
            "Limpar",
            "#636e72",
            self.clear_fields_ambiente
        ).grid(row=0, column=4, padx=0)

        # =========================== #
        # ==== AMBIENTE LIST FRAME ===== #
        ambiente_list_frame = tk.Frame(aba_ambientes, bg="#f5f6fa")
        ambiente_list_frame.pack(padx=20, fill="both", expand=True)

        tk.Label(
            ambiente_list_frame,
            text="Ambientes cadastrados",
            font=("Segoe UI", 10, "bold"),
            bg="#f5f6fa",
            fg="#2d3436"
        ).pack(anchor="w", pady=(0, 5))

        columns = ("id", "cliente", "oxigenio", "carbonico", "poluentes", "umidade", "densidade", "publicos", "cadastro")
        self.ambiente_list = ttk.Treeview(
            ambiente_list_frame,
            columns=columns,
            show="headings",
            height=12
        )
        self.ambiente_list.heading("id", text="ID")
        self.ambiente_list.heading("cliente", text="Cliente")
        self.ambiente_list.heading("oxigenio", text="Oxigenio")
        self.ambiente_list.heading("carbonico", text="Carbonico")
        self.ambiente_list.heading("poluentes", text="Poluente")
        self.ambiente_list.heading("umidade", text="Umidade")
        self.ambiente_list.heading("densidade", text="Densidade")
        self.ambiente_list.heading("publicos", text="Publico")
        self.ambiente_list.heading("cadastro", text="Data de Cadastro")


        self.ambiente_list.column("id", width=50, minwidth=0, stretch=False, anchor="center")
        self.ambiente_list.column("cliente", width=50, minwidth=0, stretch=False, anchor="center")
        self.ambiente_list.column("oxigenio", width=70, minwidth=0, stretch=False, anchor="center")
        self.ambiente_list.column("carbonico", width=70, minwidth=0, stretch=False, anchor="center")
        self.ambiente_list.column("poluentes", width=70, minwidth=0, stretch=False, anchor="center")
        self.ambiente_list.column("umidade", width=70, minwidth=0, stretch=False, anchor="center")
        self.ambiente_list.column("densidade", width=70, minwidth=0, stretch=False, anchor="center")
        self.ambiente_list.column("publicos", width=60, minwidth=0, stretch=False, anchor="center")
        self.ambiente_list.column("cadastro", width=0, anchor="center")
        
        ambiente_scrollbar = tk.Scrollbar(
            ambiente_list_frame,
            orient="vertical",
            command=self.ambiente_list.yview
        )
        self.ambiente_list.configure(yscrollcommand=ambiente_scrollbar.set)
        self.ambiente_list.pack(side="left", fill="both", expand=True)
        ambiente_scrollbar.pack(side="right", fill="y")
        self.ambiente_list.bind("<<ListboxSelect>>", self.select_banco)

        self.create_button(
            aba_ambientes,
            "Atualizar lista",
            "#00b894",
            self.load_ambientes
        ).pack(pady=(8, 15))

        self.root.after(100, self.load_ambientes)




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

    

    # ==== DEF_CLIENTES ==== #

    def clear_fields_cliente(self):
        self.entry_id_cliente.delete(0, tk.END)
        self.entry_nome.delete(0, tk.END)
        self.entry_cpf.delete(0, tk.END)
        self.entry_email.delete(0, tk.END)
        self.entry_telefone.delete(0, tk.END)
        self.entry_dados_publicos_cliente.delete(0, tk.END)
        self.entry_data_nascimento.delete(0, tk.END)
        self.entry_data_cadastro_cliente.delete(0, tk.END)

    def call_api_get_cliente(self):
        cliente_id = self.entry_id_cliente.get()

        if not cliente_id:
            messagebox.showwarning("Aviso", "Informe o ID do cliente")
            return
        
        try:
            response = requests.get(f"{API_URL_CLIENTE}/{cliente_id}")
            object = response.json()
            dados_publicos1 = object.get("dados_publicos")
            if dados_publicos1 is False:
                if not self.pede_senha_id_cliente(cliente_id):
                    return
            if response.status_code == 200:
                data = response.json()

                self.entry_nome.delete(0, tk.END)
                self.entry_nome.insert(0, data.get("nome", ""))
                self.entry_cpf.delete(0, tk.END)
                self.entry_cpf.insert(0, data.get("cpf", ""))
                self.entry_email.delete(0, tk.END)
                self.entry_email.insert(0, data.get("email", ""))
                self.entry_telefone.delete(0, tk.END)
                self.entry_telefone.insert(0, data.get("telefone", ""))
                self.entry_dados_publicos_cliente.delete(0, tk.END)
                self.entry_dados_publicos_cliente.insert(0, data.get("dados_publicos", ""))
                self.entry_data_nascimento.delete(0, tk.END)
                self.entry_data_nascimento.insert(0, data.get("data_nascimento", ""))
                self.entry_data_cadastro_cliente.delete(0, tk.END)
                self.entry_data_cadastro_cliente.insert(0, data.get("data_cadastro", ""))

            else:
                messagebox.showerror("Erro", "Cliente não encontrado")

        except Exception as e:
            messagebox.showerror("Erro", str(e))

    def call_api_post_cliente(self):
        try:
            data = {
                "nome": self.entry_nome.get(),
                "cpf": self.entry_cpf.get(),
                "email": self.entry_email.get(),
                "telefone": self.entry_telefone.get(),
                "dados_publicos": self.entry_dados_publicos_cliente.get(),
                "data_nascimento": self.entry_data_nascimento.get()
            }

            response = requests.post(API_URL_CLIENTE, data=data)

            if response.status_code in [200, 201]:
                messagebox.showinfo("Sucesso", "Cliente cadastrado com sucesso")
                self.load_clients()
            else:
                messagebox.showerror("Erro", response.text)

        except Exception as e:
            messagebox.showerror("Erro", str(e))

    def call_api_put_cliente(self):
        try:
            cliente_id = self.entry_id_cliente.get()

            response = requests.get(f"{API_URL_CLIENTE}/{cliente_id}")
            object = response.json()
            dados_publicos1 = object.get("dados_publicos")
            if dados_publicos1 is False:
                if not self.pede_senha_id_cliente(cliente_id):
                    return

            data = {
                "nome": self.entry_nome.get(),
                "cpf": self.entry_cpf.get(),
                "email": self.entry_email.get(),
                "telefone": self.entry_telefone.get(),
                "dados_publicos": self.entry_dados_publicos_cliente.get(),
                "data_nascimento": self.entry_data_nascimento.get()
            }

            response = requests.put(f"{API_URL_CLIENTE}/{cliente_id}", data=data)

            if response.status_code in [200, 201]:
                messagebox.showinfo("Sucesso", "Cliente atualizado com sucesso")
                self.load_clients()
            else:
                messagebox.showerror("Erro", response.text)

        except Exception as e:
            messagebox.showerror("Erro", str(e))

    def call_api_delete_cliente(self):
        cliente_id = self.entry_id_cliente.get()

        if not cliente_id:
            messagebox.showwarning("Aviso", "Informe o ID do cliente")
            return

        response = requests.get(f"{API_URL_CLIENTE}/{cliente_id}")
        object = response.json()
        dados_publicos1 = object.get("dados_publicos")
        if dados_publicos1 is False:
            if not self.pede_senha_id_cliente(cliente_id):
                return

        try:
            response = requests.delete(f"{API_URL_CLIENTE}/{cliente_id}")

            if response.status_code == 200:
                messagebox.showinfo("Sucesso", "Cliente removido com sucesso")
                self.load_clients()
            else:
                messagebox.showerror("Erro", response.text)

        except Exception as e:
            messagebox.showerror("Erro", str(e))

    def load_clients(self):
        try:
            response = requests.get(API_URL_CLIENTE)
            response.raise_for_status()
            clients = response.json()
            if not isinstance(clients, list):
                raise ValueError("A resposta da API não contém uma lista de clientes.")

            self.client_list.delete(*self.client_list.get_children())
            for client in clients:
                client_id = client["id"]
                name = client.get("nome")
                cpf = client.get("cpf")
                email = client.get("email")
                telefone = client.get("telefone")
                dados_publicos = client.get("dados_publicos")
                nascimento = client.get("data_nascimento")
                data_cadastro = client.get("data_cadastro")

                self.client_list.insert(
                    "",
                    tk.END,
                    values=(client_id, name, cpf, email, telefone, dados_publicos, nascimento, data_cadastro)
                )
        except (requests.RequestException, ValueError, KeyError) as error:
            messagebox.showerror("Erro", f"Não foi possível carregar os clientes: {error}")

    def select_client(self, _event):
        selection = self.client_list.selection()
        if not selection:
            return

        client_id = self.client_list.item(selection[0], "values")[0]
        self.entry_id.delete(0, tk.END)
        self.entry_id.insert(0, str(client_id))

    # ==== DEF_BANCOS ==== #

    def clear_fields_banco(self):
        self.entry_id_banco.delete(0, tk.END)
        self.entry_cliente_banco.delete(0, tk.END)
        self.entry_dinheiro.delete(0, tk.END)
        self.entry_senha.delete(0, tk.END)

    def call_api_get_banco(self):   
        id_banco = self.entry_id_banco.get()

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

                self.entry_cliente_banco.delete(0, tk.END)
                self.entry_cliente_banco.insert(0, data.get("id_cliente", ""))
                self.entry_dinheiro.delete(0, tk.END)
                self.entry_dinheiro.insert(0, data.get("dinheiro", ""))
                self.entry_senha.delete(0, tk.END)
                self.entry_senha.insert(0, data.get("senha", ""))

            else:
                messagebox.showerror("Erro", "Banco não encontrado")

        except Exception as e:
            messagebox.showerror("Erro", str(e))

    def call_api_post_banco(self):

        try:
            data = {
                "id_cliente": self.entry_cliente_banco.get(),
                "dinheiro": self.entry_dinheiro.get(),
                "senha": self.entry_senha.get()
            }

            response = requests.post(API_URL_BANCO, data=data)

            if response.status_code in [200, 201]:
                messagebox.showinfo("Sucesso", "Banco cadastrado com sucesso")
                self.load_bancos()
            else:
                messagebox.showerror("Erro", response.text)

        except Exception as e:
            messagebox.showerror("Erro", str(e))

    def call_api_put_banco(self):
        id_cliente = self.get_cliente(self.entry_id_banco.get())
        
        if not self.cliente_publico(id_cliente):
            #messagebox.showwarning("Aviso", "Cliente não é público. Não é possível buscar o banco.")
            if not self.pede_senha(self.entry_id_banco.get()):
                messagebox.showwarning("Aviso", "Senha incorreta. Não é possível buscar o banco.")
                return

        try:
            id_banco = self.entry_id_banco.get()

            data = {
                "id_cliente": self.entry_cliente_banco.get(),
                "dinheiro": self.entry_dinheiro.get(),
                "senha": self.entry_senha.get()
            }

            response = requests.put(f"{API_URL_BANCO}/{id_banco}", data=data)

            if response.status_code in [200, 201]:
                messagebox.showinfo("Sucesso", "Banco atualizado com sucesso")
                self.load_bancos()
            else:
                messagebox.showerror("Erro", response.text)

        except Exception as e:
            messagebox.showerror("Erro", str(e))

    def call_api_delete_banco(self):

        id_banco = self.entry_id_banco.get()

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
                self.load_bancos()
            else:
                messagebox.showerror("Erro", response.text)

        except Exception as e:
            messagebox.showerror("Erro", str(e))

    def load_bancos(self):
        try:
            response = requests.get(API_URL_BANCO)
            response.raise_for_status()
            bancos = response.json()
            if not isinstance(bancos, list):
                raise ValueError("A resposta da API não contém uma lista de bancos.")

            self.banco_list.delete(*self.banco_list.get_children())
            for banco in bancos:
                banco_id = banco["id_banco"]
                cliente_id_banco = banco.get("id_cliente")
                dinheiro = banco.get("dinheiro")
                senha = banco.get("senha")

                self.banco_list.insert(
                    "",
                    tk.END,
                    values=(banco_id, cliente_id_banco, dinheiro, senha)
                )
        except (requests.RequestException, ValueError, KeyError) as error:
            messagebox.showerror("Erro", f"Não foi possível carregar os bancos: {error}")

    def select_banco(self, _event):
        selection = self.banco_list.selection()
        if not selection:
            return

        banco_id = self.banco_list.item(selection[0], "values")[0]
        self.entry_id.delete(0, tk.END)
        self.entry_id.insert(0, str(banco_id))
    
    # ==== DEF_AMBIENTES ==== #

    def clear_fields_ambiente(self):
        self.entry_id_ambiente.delete(0, tk.END)
        self.entry_cliente_ambiente.delete(0, tk.END)
        self.entry_oxigenio_ambiente.delete(0, tk.END)
        self.entry_carbonico_ambiente.delete(0, tk.END)
        self.entry_poluentes_ambiente.delete(0, tk.END)
        self.entry_umidade_ambiente.delete(0, tk.END)
        self.entry_densidade_ambiente.delete(0, tk.END)
        self.entry_dados_publicos_ambiente.delete(0, tk.END)
        self.entry_data_cadastro_ambiente.delete(0, tk.END)

    def call_api_get_ambiente(self):
        ambiente_id = self.entry_id_ambiente.get()
        if not ambiente_id:
            messagebox.showwarning("Aviso", "Informe o ID do ambiente")
            return

        try:
            response = requests.get(f"{API_URL_AMBIENTE}/{ambiente_id}")

            if response.status_code == 200:
                data = response.json()
                self.entry_cliente_ambiente.delete(0, tk.END)
                self.entry_cliente_ambiente.insert(0, data.get("cliente", ""))
                self.entry_oxigenio_ambiente.delete(0, tk.END)
                self.entry_oxigenio_ambiente.insert(0, data.get("oxigenio", ""))
                self.entry_carbonico_ambiente.delete(0, tk.END)
                self.entry_carbonico_ambiente.insert(0, data.get("carbonico", ""))
                self.entry_poluentes_ambiente.delete(0, tk.END)
                self.entry_poluentes_ambiente.insert(0, data.get("poluentes", ""))
                self.entry_umidade_ambiente.delete(0, tk.END)
                self.entry_umidade_ambiente.insert(0, data.get("umidade", ""))
                self.entry_densidade_ambiente.delete(0, tk.END)
                self.entry_densidade_ambiente.insert(0, data.get("densidade", ""))
                self.entry_dados_publicos_ambiente.delete(0, tk.END)
                self.entry_dados_publicos_ambiente.insert(0, data.get("dados_publicos", ""))
                self.entry_data_cadastro_ambiente.delete(0, tk.END)
                self.entry_data_cadastro_ambiente.insert(0, data.get("data_cadastro", ""))

            else:
                messagebox.showerror("Erro", "Ambiente não encontrado")

        except Exception as e:
            messagebox.showerror("Erro", str(e))

    def call_api_post_ambiente(self):
        try:
            data = {
                "cliente": self.entry_cliente_ambiente.get(),
                "oxigenio": self.entry_oxigenio_ambiente.get(),
                "carbonico": self.entry_carbonico_ambiente.get(),
                "poluentes": self.entry_poluentes_ambiente.get(),
                "umidade": self.entry_umidade_ambiente.get(),
                "densidade": self.entry_densidade_ambiente.get(),
                "dados_publicos": self.entry_dados_publicos_ambiente.get()
            }
            response = requests.post(API_URL_AMBIENTE, data=data)
            if response.status_code in [200, 201]:
                messagebox.showinfo("Sucesso", "Ambiente cadastrado com sucesso")
                
                self.clear_fields()
            else:
                messagebox.showerror("Erro", response.text)
        except Exception as e:
            messagebox.showerror("Erro", str(e))

    def call_api_put_ambiente(self):
        try:
            ambiente_id = self.entry_id.get()

            data = {
                "cliente": self.entry_cliente_ambiente.get(),
                "oxigenio": self.entry_oxigenio_ambiente.get(),
                "carbonico": self.entry_carbonico_ambiente.get(),
                "poluentes": self.entry_poluentes_ambiente.get(),
                "umidade": self.entry_umidade_ambiente.get(),
                "densidade": self.entry_densidade_ambiente.get(),
                "dados_publicos": self.entry_dados_publicos_ambiente.get()
            }

            response = requests.put(f"{API_URL_AMBIENTE}/{ambiente_id}", data=data)
            if response.status_code in [200, 201]:
                messagebox.showinfo("Sucesso", "Ambiente atualizado com sucesso")
                self.clear_fields()
            else:
                messagebox.showerror("Erro", response.text)
        except Exception as e:
            messagebox.showerror("Erro", str(e))

    def call_api_delete_ambiente(self):
        ambiente_id = self.entry_id_ambiente.get()
        if not ambiente_id:
            messagebox.showwarning("Aviso", "Informe o ID do ambiente")
            return
        try:
            if not self.ambiente_publico(ambiente_id):
                messagebox.showwarning("Aviso", "Os dados desse ambiente são privados, logo vc nao pode deletar.")
                return
            response = requests.delete(f"{API_URL_AMBIENTE}/{ambiente_id}")
            if response.status_code == 200:
                messagebox.showinfo("Sucesso", "Ambiente removido com sucesso")
                self.clear_fields()
            else:
                messagebox.showerror("Erro", response.text)
        except Exception as e:
            messagebox.showerror("Erro", str(e))

    def load_ambientes(self):
        try:
            response = requests.get(API_URL_AMBIENTE)
            response.raise_for_status()
            ambientes = response.json()
            if not isinstance(ambientes, list):
                raise ValueError("A resposta da API não contém uma lista de bancos.")

            self.ambiente_list.delete(*self.ambiente_list.get_children())
            for ambiente in ambientes:
                ambiente_id = ambiente["id"]
                cliente_id_ambiente = ambiente.get("cliente")
                oxigenio = ambiente.get("oxigenio")
                carbonico = ambiente.get("carbonico")
                poluentes = ambiente.get("poluentes")
                umidade = ambiente.get("umidade")
                densidade = ambiente.get("densidade")
                dados_publicos = ambiente.get("dados_publicos")
                data_cadastro = ambiente.get("data_cadastro")

                self.ambiente_list.insert(
                    "",
                    tk.END,
                    values=(ambiente_id, cliente_id_ambiente, oxigenio, carbonico, poluentes, umidade, densidade, dados_publicos, data_cadastro)
                )
        except (requests.RequestException, ValueError, KeyError) as error:
            messagebox.showerror("Erro", f"Não foi possível carregar os ambientes: {error}")
    
    def select_ambiente(self, _event):
        selection = self.ambiente_list.selection()
        if not selection:
            return

        ambiente_id = self.ambiente_list.item(selection[0], "values")[0]
        self.entry_id_ambiente.delete(0, tk.END)
        self.entry_id_ambiente.insert(0, str(ambiente_id))
    
    
    # ======================================== #
    # ======================================== #
    # ======================================== #
    # ======================================== #

    def pede_senha_id_cliente(self, cliente_id):
        
        response1 = requests.get(f"{API_URL_BANCO_BY_CLIENTE}/{cliente_id}")
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

    def get_cliente(self, banco_id):
        response = requests.get(f"{API_URL_BANCO}/{banco_id}", timeout=5)
        banco = response.json()
        cliente_id = banco.get("id_cliente")

        if not cliente_id:
            messagebox.showerror("Erro", "Campo 'id_cliente' não encontrado na resposta da API")
            return None

        #messagebox.showinfo("Info", f"Cliente ID: {cliente_id}")
        return cliente_id

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

    
#==================COMECANDO BANCOS==================================#
#==================COMECANDO BANCOS==================================#

    


if __name__ == "__main__":

    root = tk.Tk()

    app = AcademicSystemApp(root)

    root.mainloop()