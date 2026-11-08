import tkinter as tk
from tkinter import messagebox, ttk
import requests

if __package__:
    from .api_urls import API_URL_PRODUTO
    from .api_errors import format_api_error
else:
    from api_urls import API_URL_PRODUTO
    from api_errors import format_api_error


class ProdutosTab:
    def build_produtos_tab(self, notebook):
        aba = tk.Frame(notebook, bg="#f5f6fa")
        notebook.add(aba, text="Produtos")
        # ===== TITLE PRODUTO =====
        title = tk.Label(
            aba,
            text="Tela de Produtos",
            font=("Segoe UI", 14, "bold"),
            bg="#f5f6fa",
            fg="#2d3436"
        )
        title.pack(pady=(5, 10))

        # ===== FORM FRAME PRODUTO =====
        form_frame_produto = tk.Frame(aba, bg="#f5f6fa")
        form_frame_produto.pack(padx=20, fill="x")

        # ===== ID =====
        self.entry_id_produto = self.criar_campo(form_frame_produto, "ID:", 0, 0)

        # ===== AMBIENTE =====
        self.entry_ambiente_produto = self.criar_campo(form_frame_produto, "Ambiente:", 1, 0)

        # ===== TIPO =====
        self.entry_tipo = self.criar_campo(form_frame_produto, "Tipo:", 2, 0)

         # ===== PRECO =====
        self.entry_preco = self.criar_campo(form_frame_produto, "Precço:", 0, 3)

        # ===== POTENCIA =====
        self.entry_potencia = self.criar_campo(form_frame_produto, "Potencia:", 1, 3)

        # ===== BUTTON FRAME PRODUTOS =====
        button_frame_produtos = tk.Frame(aba, bg="#f5f6fa")
        button_frame_produtos.pack(pady=30)

        # ==== DELETE PRODUTOS BUTTON ====
        self.create_button(
            button_frame_produtos,
            "Excluir",
            "#d63031",
            self.call_api_delete_produto
        ).grid(row=0, column=0, padx=0)

        # ==== GET PRODUTOS BUTTON ====
        self.create_button(
            button_frame_produtos,
            "Editar",
            "#e17055",
            self.call_api_put_produto
        ).grid(row=0, column=1, padx=0)

        # ==== POST PRODUTOS BUTTON ====
        self.create_button(
            button_frame_produtos,
            "Cadastrar",
            "#0984e3",
            self.call_api_post_produto
        ).grid(row=0, column=2, padx=0)

        # ==== GET PRODUTOS BUTTON ====
        self.create_button(
            button_frame_produtos,
            "Buscar",
            "#6c5ce7",
            self.call_api_get_produto
        ).grid(row=0, column=3, padx=0)

        # ===== CLEAR PRODUTOS BUTTON =====
        self.create_button(
            button_frame_produtos,
            "Limpar",
            "#636e72",
            self.clear_fields_produto
        ).grid(row=0, column=4, padx=0)

        # =========================== #
        # ==== PRODUTO LIST FRAME ===== #
        produto_list_frame = tk.Frame(aba, bg="#f5f6fa")
        produto_list_frame.pack(padx=20, fill="both", expand=True)

        tk.Label(
            produto_list_frame,
            text="Produtos cadastrados",
            font=("Segoe UI", 10, "bold"),
            bg="#f5f6fa",
            fg="#2d3436"
        ).pack(anchor="w", pady=(0, 5))

        columns = ("id", "ambiente", "tipo", "preco", "potencia")
        self.produto_list = ttk.Treeview(
            produto_list_frame,
            columns=columns,
            show="headings",
            height=12
        )
        self.produto_list.heading("id", text="ID")
        self.produto_list.heading("ambiente", text="Ambiente")
        self.produto_list.heading("tipo", text="Tipo")
        self.produto_list.heading("preco", text="Preço")
        self.produto_list.heading("potencia", text="Potencia")


        self.produto_list.column("id", width=5, anchor="center")
        self.produto_list.column("ambiente", width=5, anchor="center")
        self.produto_list.column("tipo", width=35)
        self.produto_list.column("preco", width=20)
        self.produto_list.column("potencia", width=20)
        
        produto_scrollbar = tk.Scrollbar(
            produto_list_frame,
            orient="vertical",
            command=self.produto_list.yview
        )
        self.produto_list.configure(yscrollcommand=produto_scrollbar.set)
        self.produto_list.pack(side="left", fill="both", expand=True)
        produto_scrollbar.pack(side="right", fill="y")
        self.produto_list.bind("<<ListboxSelect>>", self.select_produto)

        self.create_button(
            aba,
            "Atualizar lista",
            "#00b894",
            self.load_produtos
        ).pack(pady=(8, 15))

        self.root.after(100, self.load_produtos)

    def clear_fields_produto(self):
        self.entry_id_produto.delete(0, tk.END)
        self.entry_ambiente_produto.delete(0, tk.END)
        self.entry_tipo.delete(0, tk.END)
        self.entry_preco.delete(0, tk.END)
        self.entry_potencia.delete(0, tk.END)

    def call_api_get_produto(self):   
        produto_id = self.entry_id_produto.get()

        if not produto_id:
            messagebox.showwarning("Aviso", "Informe o ID do produto")
            return

        try:
            
            response = requests.get(f"{API_URL_PRODUTO}/{produto_id}")

            if response.status_code == 200:
                ambiente_id = self.get_ambiente_produto(produto_id)
                id_cliente = self.get_cliente_ambiente(ambiente_id)
                id_banco = self.get_banco_cliente(id_cliente)
                precisa_senha=0

                if not self.ambiente_publico(ambiente_id):
                    precisa_senha+=1
                if not self.cliente_publico(id_cliente):
                    precisa_senha+=1

                if not precisa_senha == 0:
                    if not self.pede_senha(id_banco):
                        return

                data = response.json()

                self.entry_ambiente_produto.delete(0, tk.END)
                self.entry_ambiente_produto.insert(0, data.get("id_ambiente", ""))
                self.entry_tipo.delete(0, tk.END)
                self.entry_tipo.insert(0, data.get("tipo", ""))
                self.entry_preco.delete(0, tk.END)
                self.entry_preco.insert(0, data.get("preco", ""))
                self.entry_potencia.delete(0, tk.END)
                self.entry_potencia.insert(0, data.get("potencia", ""))

            else:
                messagebox.showerror("Erro", format_api_error(response, "buscar banco"))

        except Exception as e:
            messagebox.showerror("Erro", str(e))

    def call_api_post_produto(self):

        try:
            ambiente_id = self.entry_ambiente.get()
            id_cliente = self.get_cliente_ambiente(ambiente_id)
            id_banco = self.get_banco_cliente(id_cliente)
            precisa_senha=0

            if not self.ambiente_publico(ambiente_id):
                precisa_senha+=1
            if not self.cliente_publico(id_cliente):
                precisa_senha+=1

            if not precisa_senha == 0:
                if not self.pede_senha(id_banco):
                    return

            if not self.validar_pagamento(id_banco, float(self.entry_preco.get())):
                return

            data = {
                "id_ambiente": self.entry_ambiente_produto.get(),
                "tipo": self.entry_tipo.get(),
                "preco": self.entry_preco.get(),
                "potencia": self.entry_potencia.get()
            }

            response = requests.post(API_URL_PRODUTO, data=data)

            if response.status_code in [200, 201]:
                messagebox.showinfo("Sucesso", "Produto cadastrado com sucesso")
                self.load_produtos()
            else:
                messagebox.showerror("Erro", format_api_error(response, "cadastrar produto"))

        except Exception as e:
            messagebox.showerror("Erro", str(e))

    def call_api_put_produto(self):       
        try:
            response = requests.get(f"{API_URL_PRODUTO}/{self.entry_id_produto.get()}", timeout=5)

            if response.status_code == 404:
                messagebox.showwarning("Aviso", "Produto nao encontrado")
                return

        except requests.RequestException as error:
            messagebox.showerror("Erro", f"Não foi possível verificar o produto: {error}")
            return

        produto_id = self.entry_id_produto.get()
        ambiente_id = self.get_ambiente_produto(produto_id)
        id_cliente = self.get_cliente_ambiente(ambiente_id)
        id_banco = self.get_banco_cliente(id_cliente)
        precisa_senha=0

        if not self.ambiente_publico(ambiente_id):
            precisa_senha+=1
        if not self.cliente_publico(id_cliente):
            precisa_senha+=1

        if not precisa_senha == 0:
            if not self.pede_senha(id_banco):
                return

        try:
            id_produto = self.entry_id_produto.get()
            if not self.produto_permite_operacao(id_produto):
                messagebox.showwarning("Aviso", "Os dados desse produto pertencem a um ambiente privado, " \
                                        "logo vc nao pode atualizar.")
                
                if not self.pedir_validar_senha(id_produto):
                    return
            

            data = {
                "id_ambiente": self.entry_ambiente.get(),
                "tipo": self.entry_tipo.get(),
                "preco": self.entry_preco.get(),
                "potencia": self.entry_potencia.get()
            }

            response = requests.put(f"{API_URL_PRODUTO}/{id_produto}", data=data)

            if response.status_code in [200, 201]:
                messagebox.showinfo("Sucesso", "Produto atualizado com sucesso")
                self.load_produtos()
            else:
                messagebox.showerror("Erro", format_api_error(response, "atualizar produto"))

        except Exception as e:
            messagebox.showerror("Erro", str(e))

    def call_api_delete_produto(self):
        try:
            response = requests.get(f"{API_URL_PRODUTO}/{self.entry_id_produto.get()}", timeout=5)

            if response.status_code == 404:
                messagebox.showwarning("Aviso", "Produto nao encontrado")
                return

        except requests.RequestException as error:
            messagebox.showerror("Erro", f"Não foi possível verificar o produto: {error}")
            return

        id_produto = self.entry_id_produto.get()

        if not id_produto:
            messagebox.showwarning("Aviso", "Informe o ID do produto")
            return

        ambiente_id = self.get_ambiente_produto(id_produto)
        id_cliente = self.get_cliente_ambiente(ambiente_id)
        id_banco = self.get_banco_cliente(id_cliente)
        precisa_senha=0

        if not self.ambiente_publico(ambiente_id):
            precisa_senha+=1
        if not self.cliente_publico(id_cliente):
            precisa_senha+=1

        if not precisa_senha == 0:
            if not self.pede_senha(id_banco):
                return

        try:
            response = requests.delete(f"{API_URL_PRODUTO}/{id_produto}")

            if response.status_code in [200, 204]:
                messagebox.showinfo("Sucesso", "Produto removido com sucesso")
                self.load_produtos()
            else:
                messagebox.showerror("Erro", format_api_error(response, "remover produto"))

        except Exception as e:
            messagebox.showerror("Erro", str(e))

    def load_produtos(self):
        try:
            response = requests.get(API_URL_PRODUTO)
            response.raise_for_status()
            produtos = response.json()
            if not isinstance(produtos, list):
                raise ValueError("A resposta da API não contém uma lista de produtos.")

            self.produto_list.delete(*self.produto_list.get_children())
            for produto in produtos:
                produto_id = produto["id"]
                ambiente_id_produto = produto.get("id_ambiente")
                tipo = produto.get("tipo")
                preco = produto.get("preco")
                potencia = produto.get("potencia")

                self.produto_list.insert(
                    "",
                    tk.END,
                    values=(produto_id, ambiente_id_produto, tipo, preco, potencia)
                )
        except (requests.RequestException, ValueError, KeyError) as error:
            messagebox.showerror("Erro", f"Não foi possível carregar os produtos: {error}")

    def select_produto(self, _event):
        selection = self.produto_list.selection()
        if not selection:
            return

        produto_id = self.produto_list.item(selection[0], "values")[0]
        self.entry_id.delete(0, tk.END)
        self.entry_id.insert(0, str(produto_id))
