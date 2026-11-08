import tkinter as tk
from tkinter import messagebox, ttk
import requests

if __package__:
    from .api_urls import API_URL_BANCO
    from .api_errors import format_api_error
else:
    from api_urls import API_URL_BANCO
    from api_errors import format_api_error


class BancosTab:
    def build_bancos_tab(self, notebook):
        aba = tk.Frame(notebook, bg="#f5f6fa")
        notebook.add(aba, text="Bancos")
        # ===== TITLE BANCO =====
        title = tk.Label(
            aba,
            text="Tela de Bancos",
            font=("Segoe UI", 14, "bold"),
            bg="#f5f6fa",
            fg="#2d3436"
        )
        title.pack(pady=(5, 10))

        # ===== FORM FRAME BANCO =====
        form_frame_banco = tk.Frame(aba, bg="#f5f6fa")
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
        button_frame_bancos = tk.Frame(aba, bg="#f5f6fa")
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
        banco_list_frame = tk.Frame(aba, bg="#f5f6fa")
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
            aba,
            "Atualizar lista",
            "#00b894",
            self.load_bancos
        ).pack(pady=(8, 15))

        self.root.after(100, self.load_bancos)

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

        try:
            response = requests.get(f"{API_URL_BANCO}/{id_banco}")

            if response.status_code == 200:
                id_cliente = self.get_cliente_banco(id_banco)
                #messagebox.showinfo("Info", f"ID do cliente: {id_cliente}")
                if not self.cliente_publico(id_cliente):
                    #messagebox.showwarning("Aviso", "Cliente não é público. Não é possível buscar o banco.")
                    if not self.pede_senha(id_banco):
                        #messagebox.showwarning("Aviso", "Senha incorreta. Não é possível buscar o banco.")
                        return

                data = response.json()

                self.entry_cliente_banco.delete(0, tk.END)
                self.entry_cliente_banco.insert(0, data.get("id_cliente", ""))
                self.entry_dinheiro.delete(0, tk.END)
                self.entry_dinheiro.insert(0, data.get("dinheiro", ""))
                self.entry_senha.delete(0, tk.END)
                self.entry_senha.insert(0, data.get("senha", ""))

            else:
                messagebox.showerror("Erro", format_api_error(response, "buscar banco"))

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
                messagebox.showerror("Erro", format_api_error(response, "cadastrar banco"))

        except Exception as e:
            messagebox.showerror("Erro", str(e))

    def call_api_put_banco(self):       
        try:
            response = requests.get(f"{API_URL_BANCO}/{self.entry_id_banco.get()}", timeout=5)

            if response.status_code == 404:
                messagebox.showwarning("Aviso", "Banco nao encontrado")
                return

        except requests.RequestException as error:
            messagebox.showerror("Erro", f"Não foi possível verificar o banco: {error}")
            return

        id_cliente = self.get_cliente_banco(self.entry_id_banco.get())
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
                messagebox.showerror("Erro", format_api_error(response, "atualizar banco"))

        except Exception as e:
            messagebox.showerror("Erro", str(e))

    def call_api_delete_banco(self):
        try:
            response = requests.get(f"{API_URL_BANCO}/{self.entry_id_banco.get()}", timeout=5)

            if response.status_code == 404:
                messagebox.showwarning("Aviso", "Banco nao encontrado")
                return

        except requests.RequestException as error:
            messagebox.showerror("Erro", f"Não foi possível verificar o banco: {error}")
            return

        id_banco = self.entry_id_banco.get()

        if not id_banco:
            messagebox.showwarning("Aviso", "Informe o ID do banco")
            return

        id_cliente = self.get_cliente_banco(id_banco)
        #messagebox.showinfo("Info", "id do cliente sendo pego")

        if not self.cliente_publico(id_cliente):
            #messagebox.showwarning("Aviso", "Cliente não é público. Não é possível remover o banco.")
            if not self.pede_senha(id_banco):
                return

        try:
            response = requests.delete(f"{API_URL_BANCO}/{id_banco}")

            if response.status_code in [200, 204]:
                messagebox.showinfo("Sucesso", "Banco removido com sucesso")
                self.load_bancos()
            else:
                messagebox.showerror("Erro", format_api_error(response, "remover banco"))

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

                if not self.cliente_publico(cliente_id_banco):
                    self.banco_list.insert(
                        "",
                        tk.END,
                        values=(banco_id, cliente_id_banco, "Protegido", "Protegido")
                    )
                else:
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
