import tkinter as tk
from tkinter import messagebox, ttk
import requests

if __package__:
    from .api_urls import API_URL_CLIENTE
    from .api_errors import format_api_error
else:
    from api_urls import API_URL_CLIENTE
    from api_errors import format_api_error


class ClientesTab:
    def build_clientes_tab(self, notebook):
        aba = tk.Frame(notebook, bg="#f5f6fa")
        notebook.add(aba, text="Clientes")
        # ===== TITLE CLIENTE =====
        title = tk.Label(
            aba,
            text="Clientes",
            font=("Segoe UI", 14, "bold"),
            bg="#f5f6fa",
            fg="#2d3436"
        )
        title.pack(pady=(5, 10))

        # ===== FORM FRAME CLIENTE =====
        form_frame_cliente = tk.Frame(aba, bg="#f5f6fa")
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
        button_frame_clientes = tk.Frame(aba, bg="#f5f6fa")
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
        client_list_frame = tk.Frame(aba, bg="#f5f6fa")
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
            aba,
            "Atualizar lista",
            "#00b894",
            self.load_clients
        ).pack(pady=(8, 15))

        self.root.after(100, self.load_clients)

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
            
            if response.status_code == 200:
                if not self.cliente_publico(cliente_id):
                    id_banco = self.get_banco_cliente(cliente_id)
                    if not self.pede_senha(id_banco):
                        return
                    
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
                messagebox.showerror("Erro", format_api_error(response, "buscar cliente"))

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
                messagebox.showerror("Erro", format_api_error(response, "cadastrar cliente"))

        except Exception as e:
            messagebox.showerror("Erro", str(e))

    def call_api_put_cliente(self):
        cliente_id = self.entry_id_cliente.get()
        try:

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
                messagebox.showerror("Erro", format_api_error(response, "atualizar cliente"))

        except Exception as e:
            messagebox.showerror("Erro", str(e))

    def call_api_delete_cliente(self):
        cliente_id = self.entry_id_cliente.get()

        if not cliente_id:
            messagebox.showwarning("Aviso", "Informe o ID do cliente")
            return

        try:
            response = requests.get(f"{API_URL_CLIENTE}/{cliente_id}", timeout=5)

            if response.status_code == 404:
                messagebox.showwarning("Aviso", "Cliente não encontrado")
                return
                

        except requests.RequestException as error:
            messagebox.showerror("Erro", f"Não foi possível verificar o cliente: {error}")
            return

        id_banco = self.get_banco_cliente(cliente_id)
        if not self.cliente_publico(cliente_id):
            if not self.pede_senha(id_banco):
                return

        try:
            response = requests.delete(f"{API_URL_CLIENTE}/{cliente_id}")

            if response.status_code in [200, 204]:
                messagebox.showinfo("Sucesso", "Cliente removido com sucesso")
                self.load_clients()
            else:
                messagebox.showerror("Erro", format_api_error(response, "remover cliente"))

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
