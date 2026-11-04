import tkinter as tk
from tkinter import messagebox, simpledialog
import requests

API_URL_PRODUTO = "http://127.0.0.1:5000/trabalhopav/produtos"
API_URL_AMBIENTE = "http://127.0.0.1:5000/trabalhopav/ambientes"
API_URL_CLIENTE = "http://127.0.0.1:5000/trabalhopav/clientes"
API_URL_BANCO = "http://127.0.0.1:5000/trabalhopav/bancos"
API_URL_BANCO_BY_CLIENTE = "http://127.0.0.1:5000/trabalhopav/bancos/cliente"

class AcademicSystemApp:
    def __init__(self, root):

        self.root = root
        self.root.title("Todos os Produtos")
        self.root.geometry("760x760")
        self.root.configure(bg="#f5f6fa")
        self.root.resizable(False, False)

        self.setup_ui()

    def setup_ui(self):

        # ===== TITLE =====
        title = tk.Label(
            self.root,
            text="Tela de Produtos",
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

        # ===== AMBIENTE =====
        lbl_ambiente = tk.Label(
            form_frame,
            text="Ambiente:",
            font=("Segoe UI", 14, "bold"),
            bg="#f5f6fa",
            fg="#2d3436"
        )
        lbl_ambiente.grid(row=1, column=0, sticky="w", pady=10)

        self.entry_ambiente = tk.Entry(
            form_frame,
            font=("Segoe UI", 13),
            relief="solid",
            bd=1,
            width=35
        )
        self.entry_ambiente.grid(row=1, column=1, padx=20, pady=10, ipady=8)

        # ===== TIPO =====
        lbl_tipo = tk.Label(
            form_frame,
            text="Tipo:",
            font=("Segoe UI", 14, "bold"),
            bg="#f5f6fa",
            fg="#2d3436"
        )
        lbl_tipo.grid(row=2, column=0, sticky="w", pady=10)
        
        self.entry_tipo = tk.Entry(
            form_frame,
            font=("Segoe UI", 13),
            relief="solid",
            bd=1,
            width=35
        )
        self.entry_tipo.grid(row=2, column=1, padx=20, pady=10, ipady=8)

        # ===== PRECO =====
        lbl_preco = tk.Label(
            form_frame,
            text="Preço:",
            font=("Segoe UI", 14, "bold"),
            bg="#f5f6fa",
            fg="#2d3436"
        )
        lbl_preco.grid(row=3, column=0, sticky="w", pady=10)

        self.entry_preco = tk.Entry(
            form_frame,
            font=("Segoe UI", 13),
            relief="solid",
            bd=1,
            width=35
        )
        self.entry_preco.grid(row=3, column=1, padx=20, pady=10, ipady=8)

                # ===== POTENCIA =====
        lbl_potencia = tk.Label(
            form_frame,
            text="Potência:",
            font=("Segoe UI", 14, "bold"),
            bg="#f5f6fa",
            fg="#2d3436"
        )
        lbl_potencia.grid(row=4, column=0, sticky="w", pady=10)

        self.entry_potencia = tk.Entry(
            form_frame,
            font=("Segoe UI", 13),
            relief="solid",
            bd=1,
            width=35
        )
        self.entry_potencia.grid(row=4, column=1, padx=20, pady=10, ipady=8)

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
        self.entry_ambiente.delete(0, tk.END)
        self.entry_tipo.delete(0, tk.END)
        self.entry_preco.delete(0, tk.END)
        self.entry_potencia.delete(0, tk.END)

    def call_api_get(self):

        produto_id = self.entry_id.get()

        if not produto_id:
            messagebox.showwarning("Aviso", "Informe o ID do produto")
            return

        try:
            if not self.produto_permite_operacao(produto_id):
                messagebox.showwarning("Aviso", "Os dados desse produto pertencem a um ambiente privado, " \
                                        "logo vc nao pode buscar.")
                
                if not self.pedir_validar_senha(produto_id):
                    return
            
            response = requests.get(f"{API_URL_PRODUTO}/{produto_id}")

            if response.status_code == 200:
                data = response.json()

                self.entry_ambiente.delete(0, tk.END)
                self.entry_ambiente.insert(0, data.get("id_ambiente", ""))

                self.entry_tipo.delete(0, tk.END)
                self.entry_tipo.insert(0, data.get("tipo", ""))

                self.entry_preco.delete(0, tk.END)
                self.entry_preco.insert(0, data.get("preco", ""))

                self.entry_potencia.delete(0, tk.END)
                self.entry_potencia.insert(0, data.get("potencia", ""))

            else:
                messagebox.showerror("Erro", "Produto não encontrado")

        except Exception as e:
            messagebox.showerror("Erro", str(e))

    def call_api_post(self):

        try:
            ambiente_id = self.entry_ambiente.get()
            if not self.ambiente_permite_operacao(ambiente_id):
                messagebox.showwarning("Aviso", "Os dados desse produto pertencem a um ambiente privado, " \
                "logo vc nao pode cadastrar.")

                if not self.ambiente_pedir_validar_senha(ambiente_id):
                    return
            
            data = {
                "id_ambiente": self.entry_ambiente.get(),
                "tipo": self.entry_tipo.get(),
                "preco": self.entry_preco.get(),
                "potencia": self.entry_potencia.get()
            }

            response = requests.post(API_URL_PRODUTO, data=data)

            if response.status_code in [200, 201]:
                messagebox.showinfo("Sucesso", "Produto cadastrado com sucesso")
                self.clear_fields()
            else:
                messagebox.showerror("Erro", response.text)

        except Exception as e:
            messagebox.showerror("Erro", str(e))

    def call_api_put(self):

        try:
            produto_id = self.entry_id.get()
            if not self.produto_permite_operacao(produto_id):
                messagebox.showwarning("Aviso", "Os dados desse produto pertencem a um ambiente privado, " \
                                        "logo vc nao pode atualizar.")
                
                if not self.pedir_validar_senha(produto_id):
                    return

            data = {
                "id_ambiente": self.entry_ambiente.get(),
                "tipo": self.entry_tipo.get(),
                "preco": self.entry_preco.get(),
                "potencia": self.entry_potencia.get()
            }

            response = requests.put(f"{API_URL_PRODUTO}/{produto_id}", data=data)

            if response.status_code in [200, 201]:
                messagebox.showinfo("Sucesso", "Produto atualizado com sucesso")
                self.clear_fields()
            else:
                messagebox.showerror("Erro", response.text)

        except Exception as e:
            messagebox.showerror("Erro", str(e))

    def call_api_delete(self):

        produto_id = self.entry_id.get()

        if not produto_id:
            messagebox.showwarning("Aviso", "Informe o ID do produto")
            return

        try:
            if not self.produto_permite_operacao(produto_id):
                messagebox.showwarning("Aviso", "Os dados desse produto pertencem a um ambiente privado, logo vc nao pode deletar.")
                return
            
            response = requests.delete(f"{API_URL_PRODUTO}/{produto_id}")

            if response.status_code == 200:
                messagebox.showinfo("Sucesso", "Produto removido com sucesso")
                self.clear_fields()
            else:
                messagebox.showerror("Erro", response.text)

        except Exception as e:
            messagebox.showerror("Erro", str(e))

    def produto_permite_operacao(self, produto_id):
    
        response = requests.get(f"{API_URL_PRODUTO}/{produto_id}",timeout=5)

        produto1 = response.json()

        ambiente_id = produto1.get("id_ambiente")
        #messagebox.showwarning("Aviso", "Ambiente ID: " + str(ambiente_id))

        response1 = requests.get(f"{API_URL_AMBIENTE}/{ambiente_id}",timeout=5)
        
        ambiente = response1.json()

        if (ambiente["dados_publicos"] == True):
            #messagebox.showwarning("True", "só")
            return True
        if (ambiente["dados_publicos"] == False):
            #messagebox.showwarning("False", "só")
            return False
        
        messagebox.showerror("Putz", "nao deveria chegar aqui, mas chegou")
        return False

    def ambiente_permite_operacao(self, ambiente_id):
           
            response = requests.get(f"{API_URL_AMBIENTE}/{ambiente_id}",timeout=5)
            ambiente = response.json()
    
            if (ambiente["dados_publicos"] == True):
                #messagebox.showwarning("True", "só")
                return True
            if (ambiente["dados_publicos"] == False):
                #messagebox.showwarning("False", "só")
                return False
            
            messagebox.showerror("Putz", "nao deveria chegar aqui, mas chegou")
            return False

    def pedir_validar_senha(self, produto_id):
        #messagebox.showinfo("Aviso", "entrando em pedir_validar_senha") 
        senha = simpledialog.askstring(
        "Senha", 
        "Digite a senha do cliente ", 
        show="*",
        parent=self.root)

        #messagebox.showinfo("Aviso", "saiu do simpledialog.askstring")

        if senha is None:
            return False

        #messagebox.showinfo("Aviso", "entrando no request de produto pra saber o ambiente")

        response0 = requests.get(f"{API_URL_PRODUTO}/{produto_id}",timeout=5)
        object0 = response0.json()
        ambiente_id0 = object0.get("id_ambiente")

        #messagebox.showinfo("Aviso", "entrando no request de ambiente pra saber o cliente")

        response1 = requests.get(f"{API_URL_AMBIENTE}/{ambiente_id0}",timeout=5)
        object1 = response1.json()
        cliente_id1 = object1.get("cliente")

        #messagebox.showinfo("Aviso", "entrando no request de cliente pra saber a senha")

        response2 = requests.get(f"{API_URL_CLIENTE}/{cliente_id1}",timeout=5)
        object2 = response2.json()
        senha_correta2 = object2.get("senha")

        #messagebox.showinfo("Aviso", "verificando a senha")

        if senha == senha_correta2:
            messagebox.showinfo("Sucesso", "Senha correta. Acesso permitido.")
            return True

        messagebox.showwarning("Aviso", "Senha incorreta. Acesso negado.")
        return False

    def ambiente_pedir_validar_senha(self, ambiente_id):
            #messagebox.showinfo("Aviso", "entrando em pedir_validar_senha") 
            senha = simpledialog.askstring(
            "Senha", 
            "Digite a senha do cliente ", 
            show="*",
            parent=self.root)
    
            #messagebox.showinfo("Aviso", "saiu do simpledialog.askstring")
    
            if senha is None:
                return False
    
            #messagebox.showinfo("Aviso", "entrando no request de produto pra saber o ambiente")

            #messagebox.showinfo("Aviso", "entrando no request de ambiente pra saber o cliente")
    
            response1 = requests.get(f"{API_URL_AMBIENTE}/{ambiente_id}",timeout=5)
            object1 = response1.json()
            cliente_id1 = object1.get("cliente")
    
            #messagebox.showinfo("Aviso", "entrando no request de cliente pra saber a senha")
    
            response2 = requests.get(f"{API_URL_CLIENTE}/{cliente_id1}",timeout=5)
            object2 = response2.json()
            senha_correta2 = object2.get("senha")
    
            #messagebox.showinfo("Aviso", "verificando a senha")
    
            if senha == senha_correta2:
                messagebox.showinfo("Sucesso", "Senha correta. Acesso permitido.")
                return True
    
            messagebox.showwarning("Aviso", "Senha incorreta. Acesso negado.")
            return False
        

if __name__ == "__main__":

    root = tk.Tk()

    app = AcademicSystemApp(root)

    root.mainloop()