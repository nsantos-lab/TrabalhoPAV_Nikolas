import tkinter as tk
from tkinter import messagebox, ttk
import requests

if __package__:
    from .api_urls import API_URL_AMBIENTE_TEMPO
    from .api_errors import format_api_error
else:
    from api_urls import API_URL_AMBIENTE_TEMPO
    from api_errors import format_api_error


class AmbienteTempoTab:
    def build_ambiente_tempo_tab(self, notebook):
        aba = tk.Frame(notebook, bg="#f5f6fa")
        notebook.add(aba, text="Ambiente Tempo")
        # ===== TITLE AMBIENTE_TEMPO =====
        title = tk.Label(
            aba,
            text="Tela de Tempos de Ambientes",
            font=("Segoe UI", 14, "bold"),
            bg="#f5f6fa",
            fg="#2d3436"
        )
        title.pack(pady=(5, 10))

        # ===== FORM FRAME AMBIENTE_TEMPO =====
        form_frame_ambiente_tempo = tk.Frame(aba, bg="#f5f6fa")
        form_frame_ambiente_tempo.pack(padx=20, fill="x")

        # ===== ID =====
        self.entry_id_ambiente_tempo = self.criar_campo(form_frame_ambiente_tempo, "ID:", 0, 0)

        # ===== AMBIENTE =====
        self.entry_ambiente_ambiente_tempo = self.criar_campo(form_frame_ambiente_tempo, "Ambiente:", 1, 0)

        # ===== OXIGENIO =====
        self.entry_oxigenio_ambiente_tempo = self.criar_campo(form_frame_ambiente_tempo, "Oxigenio:", 2, 0)

        # ===== CARBONICO =====
        self.entry_carbonico_ambiente_tempo = self.criar_campo(form_frame_ambiente_tempo, "Carbonico:", 3, 0)

        # ===== POLUENTES =====
        self.entry_poluentes_ambiente_tempo = self.criar_campo(form_frame_ambiente_tempo, "Poluentes:", 0, 3)

        # ===== UMIDADE =====
        self.entry_umidade_ambiente_tempo = self.criar_campo(form_frame_ambiente_tempo, "Umidade:", 1, 3)

        # ===== TEMPERATURA =====
        self.entry_temperatura_ambiente_tempo = self.criar_campo(form_frame_ambiente_tempo, "Temperatura:", 2, 3)

        # ===== DATA_CADASTRO =====
        self.entry_data_cadastro_ambiente_tempo = self.criar_campo(form_frame_ambiente_tempo, "Data Cadastro:", 3, 3)

        # ===== BUTTON FRAME AMBIENTE_TEMPO=====
        button_frame_ambiente_tempo = tk.Frame(aba, bg="#f5f6fa")
        button_frame_ambiente_tempo.pack(pady=30)

        # ==== DELETE AMBIENTE_TEMPO BUTTON ====
        self.create_button(
            button_frame_ambiente_tempo,
            "Excluir",
            "#d63031",
            self.call_api_delete_ambiente_tempo
        ).grid(row=0, column=0, padx=0)

        # ==== GET AMBIENTE_TEMPO BUTTON ====
        self.create_button(
            button_frame_ambiente_tempo,
            "Editar",
            "#e17055",
            self.call_api_put_ambiente_tempo
        ).grid(row=0, column=1, padx=0)

        # ==== POST AMBIENTE_TEMPO BUTTON ====
        self.create_button(
            button_frame_ambiente_tempo,
            "Cadastrar",
            "#0984e3",
            self.call_api_post_ambiente_tempo
        ).grid(row=0, column=2, padx=0)

        # ==== GET AMBIENTE_TEMPO BUTTON ====
        self.create_button(
            button_frame_ambiente_tempo,
            "Buscar",
            "#6c5ce7",
            self.call_api_get_ambiente_tempo
        ).grid(row=0, column=3, padx=0)

        # ===== CLEAR AMBIENTE_TEMPO BUTTON =====
        self.create_button(
            button_frame_ambiente_tempo,
            "Limpar",
            "#636e72",
            self.clear_fields_ambiente_tempo
        ).grid(row=0, column=4, padx=0)

        # =========================== #
        # ==== AMBIENTE_TEMPO LIST FRAME ===== #
        ambiente_tempo_list_frame = tk.Frame(aba, bg="#f5f6fa")
        ambiente_tempo_list_frame.pack(padx=20, fill="both", expand=True)

        tk.Label(
            ambiente_tempo_list_frame,
            text="Tempo dos Tempos dos Ambientes cadastrados",
            font=("Segoe UI", 10, "bold"),
            bg="#f5f6fa",
            fg="#2d3436"
        ).pack(anchor="w", pady=(0, 5))

        columns = ("id", "ambiente", "oxigenio", "carbonico", "poluentes", "umidade", "temperatura", "cadastro")
        self.ambiente_tempo_list = ttk.Treeview(
            ambiente_tempo_list_frame,
            columns=columns,
            show="headings",
            height=12
        )
        self.ambiente_tempo_list.heading("id", text="ID")
        self.ambiente_tempo_list.heading("ambiente", text="Ambiente")
        self.ambiente_tempo_list.heading("oxigenio", text="Oxigenio")
        self.ambiente_tempo_list.heading("carbonico", text="Carbonico")
        self.ambiente_tempo_list.heading("poluentes", text="Poluente")
        self.ambiente_tempo_list.heading("umidade", text="Umidade")
        self.ambiente_tempo_list.heading("temperatura", text="Temperatura")
        self.ambiente_tempo_list.heading("cadastro", text="Data de Cadastro")


        self.ambiente_tempo_list.column("id", width=50, minwidth=0, stretch=False, anchor="center")
        self.ambiente_tempo_list.column("ambiente", width=50, minwidth=0, stretch=False, anchor="center")
        self.ambiente_tempo_list.column("oxigenio", width=70, minwidth=0, stretch=False, anchor="center")
        self.ambiente_tempo_list.column("carbonico", width=70, minwidth=0, stretch=False, anchor="center")
        self.ambiente_tempo_list.column("poluentes", width=70, minwidth=0, stretch=False, anchor="center")
        self.ambiente_tempo_list.column("umidade", width=70, minwidth=0, stretch=False, anchor="center")
        self.ambiente_tempo_list.column("temperatura", width=70, minwidth=0, stretch=False, anchor="center")
        self.ambiente_tempo_list.column("cadastro", width=0, anchor="center")
        
        ambiente_tempo_scrollbar = tk.Scrollbar(
            ambiente_tempo_list_frame,
            orient="vertical",
            command=self.ambiente_tempo_list.yview
        )
        self.ambiente_tempo_list.configure(yscrollcommand=ambiente_tempo_scrollbar.set)
        self.ambiente_tempo_list.pack(side="left", fill="both", expand=True)
        ambiente_tempo_scrollbar.pack(side="right", fill="y")
        self.ambiente_tempo_list.bind("<<ListboxSelect>>", self.select_banco)

        self.create_button(
            aba,
            "Atualizar lista",
            "#00b894",
            self.load_ambiente_tempo
        ).pack(pady=(8, 15))

        #self.root.after(100, self.load_ambiente_tempo)

    def clear_fields_ambiente_tempo(self):
        self.entry_id_ambiente_tempo.delete(0, tk.END)
        self.entry_ambiente_ambiente_tempo.delete(0, tk.END)
        self.entry_oxigenio_ambiente_tempo.delete(0, tk.END)
        self.entry_carbonico_ambiente_tempo.delete(0, tk.END)
        self.entry_poluentes_ambiente_tempo.delete(0, tk.END)
        self.entry_umidade_ambiente_tempo.delete(0, tk.END)
        self.entry_temperatura_ambiente_tempo.delete(0, tk.END)
        self.entry_data_cadastro_ambiente_tempo.delete(0, tk.END)

    def call_api_get_ambiente_tempo(self):
        ambiente_tempo_id = self.entry_id_ambiente_tempo.get()
        if not ambiente_tempo_id:
                    messagebox.showwarning("Aviso", "Informe o ID do tempo do ambiente")
                    return

        try:          
            response = requests.get(f"{API_URL_AMBIENTE_TEMPO}/{ambiente_tempo_id}")

            if response.status_code == 200:
                ambiente_id = self.get_ambiente_ambiente_tempo(ambiente_tempo_id)
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

                self.entry_ambiente_ambiente_tempo.delete(0, tk.END)
                self.entry_ambiente_ambiente_tempo.insert(0, data.get("ambiente", ""))
                self.entry_oxigenio_ambiente_tempo.delete(0, tk.END)
                self.entry_oxigenio_ambiente_tempo.insert(0, data.get("oxigenio", ""))
                self.entry_carbonico_ambiente_tempo.delete(0, tk.END)
                self.entry_carbonico_ambiente_tempo.insert(0, data.get("carbonico", ""))
                self.entry_poluentes_ambiente_tempo.delete(0, tk.END)
                self.entry_poluentes_ambiente_tempo.insert(0, data.get("poluentes", ""))
                self.entry_umidade_ambiente_tempo.delete(0, tk.END)
                self.entry_umidade_ambiente_tempo.insert(0, data.get("umidade", ""))
                self.entry_temperatura_ambiente_tempo.delete(0, tk.END)
                self.entry_temperatura_ambiente_tempo.insert(0, data.get("temperatura", ""))
                self.entry_data_cadastro_ambiente_tempo.delete(0, tk.END)
                self.entry_data_cadastro_ambiente_tempo.insert(0, data.get("data_cadastro", ""))

            else:
                messagebox.showerror("Erro", format_api_error(response, "buscar tempo do ambiente"))

        except Exception as e:
            messagebox.showerror("Erro", str(e))

    def call_api_post_ambiente_tempo(self):

        ambiente_id = self.entry_ambiente_ambiente_tempo.get()
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
            data = {
                "ambiente": self.entry_ambiente_ambiente_tempo.get(),
                "oxigenio": self.entry_oxigenio_ambiente_tempo.get(),
                "carbonico": self.entry_carbonico_ambiente_tempo.get(),
                "poluentes": self.entry_poluentes_ambiente_tempo.get(),
                "umidade": self.entry_umidade_ambiente_tempo.get(),
                "temperatura": self.entry_temperatura_ambiente_tempo.get()
            }

            response = requests.post(API_URL_AMBIENTE_TEMPO, data=data)

            if response.status_code in [200, 201]:
                messagebox.showinfo("Sucesso", "Ambiente Tempo cadastrado com sucesso")
                self.load_ambiente_tempo()
            else:
                messagebox.showerror("Erro", format_api_error(response, "cadastrar tempo do ambiente"))

        except Exception as e: 
            messagebox.showerror("Erro", str(e))

    def call_api_put_ambiente_tempo(self):
        ambiente_tempo_id = self.entry_id_ambiente_tempo.get()

        if not ambiente_tempo_id:
            messagebox.showwarning("Aviso", "Informe o ID do tempo do ambiente")
            return
        
        ambiente_id = self.get_ambiente_ambiente_tempo(ambiente_tempo_id)
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
                "ambiente": self.entry_ambiente_ambiente_tempo.get(),
                "oxigenio": self.entry_oxigenio_ambiente_tempo.get(),
                "carbonico": self.entry_carbonico_ambiente_tempo.get(),
                "poluentes": self.entry_poluentes_ambiente_tempo.get(),
                "umidade": self.entry_umidade_ambiente_tempo.get(),
                "temperatura": self.entry_temperatura_ambiente_tempo.get(),
            }

            response = requests.put(f"{API_URL_AMBIENTE_TEMPO}/{ambiente_tempo_id}", data=data)

            if response.status_code in [200, 201]:
                messagebox.showinfo("Sucesso", "Ambiente Tempo atualizado com sucesso")
                self.load_ambiente_tempo()
            else:
                messagebox.showerror("Erro", format_api_error(response, "atualizar tempo do ambiente"))

        except Exception as e:
            messagebox.showerror("Erro", str(e))

    def call_api_delete_ambiente_tempo(self):
        ambiente_tempo_id = self.entry_id_ambiente_tempo.get()
        if not ambiente_tempo_id:
            messagebox.showwarning("Aviso", "Informe o ID do tempo do ambiente")
            return

        ambiente_id = self.get_ambiente_ambiente_tempo(ambiente_tempo_id)
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
            response = requests.delete(f"{API_URL_AMBIENTE_TEMPO}/{ambiente_tempo_id}")

            if response.status_code in [200, 204]:
                messagebox.showinfo("Sucesso", "Ambiente Tempo removido com sucesso")
                self.clear_fields_ambiente_tempo()
                self.load_ambiente_tempo()
            else:
                messagebox.showerror("Erro", format_api_error(response, "remover tempo do ambiente"))

        except Exception as e:
            messagebox.showerror("Erro", str(e))

    def load_ambiente_tempo(self):
        try:
            response = requests.get(API_URL_AMBIENTE_TEMPO)
            response.raise_for_status()
            ambiente_tempos = response.json()
            if not isinstance(ambiente_tempos, list):
                raise ValueError("A resposta da API não contém uma lista de tempos de ambientes.")

            self.ambiente_tempo_list.delete(*self.ambiente_tempo_list.get_children())
            for ambiente_tempo in ambiente_tempos:
                ambiente_tempo_id = ambiente_tempo["id"]
                ambiente_id_ambiente = ambiente_tempo.get("ambiente")
                oxigenio = ambiente_tempo.get("oxigenio")
                carbonico = ambiente_tempo.get("carbonico")
                poluentes = ambiente_tempo.get("poluentes")
                umidade = ambiente_tempo.get("umidade")
                temperatura = ambiente_tempo.get("temperatura")
                data_cadastro = ambiente_tempo.get("data_cadastro")

                cliente_id = self.get_cliente_ambiente(ambiente_id_ambiente)
                if not self.cliente_publico(cliente_id) or not self.ambiente_publico(ambiente_id_ambiente):
                    self.ambiente_tempo_list.insert(
                        "",
                        tk.END,
                        values=(ambiente_tempo_id, ambiente_id_ambiente, "Protegido", "Protegido", "Protegido", "Protegido", "Protegido", data_cadastro)
                    )
                else:
                    self.ambiente_tempo_list.insert(
                        "",
                        tk.END,
                        values=(ambiente_tempo_id, ambiente_id_ambiente, oxigenio, carbonico, poluentes, umidade, temperatura, data_cadastro)
                    )
        except (requests.RequestException, ValueError, KeyError) as error:
            messagebox.showerror("Erro", f"Não foi possível carregar os tempos dos ambientes: {error}")

    def select_ambiente_tempo(self, _event):
        selection = self.ambiente_tempo_list.selection()
        if not selection:
            return

        ambiente_tempo_id = self.ambiente_tempo_list.item(selection[0], "values")[0]
        self.entry_id_ambiente_tempo.delete(0, tk.END)
        self.entry_id_ambiente_tempo.insert(0, str(ambiente_tempo_id))
