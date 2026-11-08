import tkinter as tk
from tkinter import messagebox, ttk
import requests

if __package__:
    from .api_urls import API_URL_CLIENTE, API_URL_AMBIENTE
    from .api_errors import format_api_error
else:
    from api_urls import API_URL_CLIENTE, API_URL_AMBIENTE
    from api_errors import format_api_error


class AmbientesTab:
    def build_ambientes_tab(self, notebook):
        aba = tk.Frame(notebook, bg="#f5f6fa")
        notebook.add(aba, text="Ambientes")
        # ===== TITLE AMBIENTE =====
        title = tk.Label(
            aba,
            text="Tela de Ambientes",
            font=("Segoe UI", 14, "bold"),
            bg="#f5f6fa",
            fg="#2d3436"
        )
        title.pack(pady=(5, 10))

        # ===== FORM FRAME AMBIENTE =====
        form_frame_ambiente = tk.Frame(aba, bg="#f5f6fa")
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
        button_frame_ambientes = tk.Frame(aba, bg="#f5f6fa")
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
        ambiente_list_frame = tk.Frame(aba, bg="#f5f6fa")
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
            aba,
            "Atualizar lista",
            "#00b894",
            self.load_ambientes
        ).pack(pady=(8, 15))

        self.root.after(100, self.load_ambientes)

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
                messagebox.showerror("Erro", format_api_error(response, "buscar ambiente"))

        except Exception as e:
            messagebox.showerror("Erro", str(e))

    def call_api_post_ambiente(self):
        id_cliente = self.entry_cliente_ambiente.get()
        if (id_cliente is None or id_cliente == ""):
            messagebox.showwarning("Aviso", "Sem id do cliente")
            return

        try:
            response = requests.get(f"{API_URL_CLIENTE}/{id_cliente}", timeout=5)

            if response.status_code == 404:
                messagebox.showwarning("Aviso", "Cliente não encontrado")
                return
                

        except requests.RequestException as error:
            messagebox.showerror("Erro", f"Não foi possível verificar o cliente: {error}")
            return
        
        if not self.cliente_publico(id_cliente):
            messagebox.showinfo("aviso", "cliente nao é publico")
            id_banco = self.get_banco_cliente(id_cliente)
            if not self.pede_senha(id_banco):
                return
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
                
                self.load_ambientes()
            else:
                messagebox.showerror("Erro", format_api_error(response, "cadastrar ambiente"))
        except Exception as e:
            messagebox.showerror("Erro", str(e))

    def call_api_put_ambiente(self):
        ambiente_id = self.entry_id_ambiente.get()
        if not ambiente_id:
            messagebox.showwarning("Aviso", "Informe o ID do ambiente")
            return

        try:
            response = requests.get(f"{API_URL_AMBIENTE}/{ambiente_id}", timeout=5)

            if response.status_code == 404:
                messagebox.showwarning("Aviso", "Ambiente nao encontrado")
                return
            if response.status_code != 200:
                messagebox.showerror("Erro", format_api_error(response, "verificar ambiente"))
                return

        except requests.RequestException as error:
            messagebox.showerror("Erro", f"Não foi possível verificar o ambiente: {error}")
            return
        
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
                self.load_ambientes()
            else:
                messagebox.showerror("Erro", format_api_error(response, "atualizar ambiente"))
        except Exception as e:
            messagebox.showerror("Erro", str(e))

    def call_api_delete_ambiente(self):
        try:
            response = requests.get(f"{API_URL_AMBIENTE}/{self.entry_id_ambiente}", timeout=5)

            if response.status_code == 404:
                messagebox.showwarning("Aviso", "Ambiente nao encontrado")
                return

        except requests.RequestException as error:
            messagebox.showerror("Erro", f"Não foi possível verificar o ambiente: {error}")
            return
        ambiente_id = self.entry_id_ambiente.get()
        if not ambiente_id:
            messagebox.showwarning("Aviso", "Informe o ID do ambiente")
            return

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

            response = requests.delete(f"{API_URL_AMBIENTE}/{ambiente_id}")
            if response.status_code in [200, 204]:
                messagebox.showinfo("Sucesso", "Ambiente removido com sucesso")
                self.clear_fields_ambiente()
                self.load_ambientes()
            else:
                messagebox.showerror("Erro", format_api_error(response, "remover ambiente"))
        except Exception as e:
            messagebox.showerror("Erro", str(e))

    def load_ambientes(self):
        try:
            response = requests.get(API_URL_AMBIENTE)
            response.raise_for_status()
            ambientes = response.json()
            if not isinstance(ambientes, list):
                raise ValueError("A resposta da API não contém uma lista de ambientes.")

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

                if not self.cliente_publico(cliente_id_ambiente) or dados_publicos == 0:
                    self.ambiente_list.insert(
                        "",
                        tk.END,
                        values=(ambiente_id, cliente_id_ambiente, "Protegido", "Protegido", "Protegido", "Protegido", "Protegido", dados_publicos, "Protegido")
                    )
                else:
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
