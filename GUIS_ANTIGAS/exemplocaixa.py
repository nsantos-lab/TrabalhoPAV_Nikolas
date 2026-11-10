import tkinter as tk

def verificar_selecao():
    if var_check.get() == 1:
        print("Opção marcada!")
    else:
        print("Opção desmarcada!")

janela = tk.Tk()
janela.title("Exemplo Checkbutton")
janela.geometry("300x150")

# Variável para armazenar o estado (1 para marcado, 0 para desmarcado)
var_check = tk.IntVar()

# Criando a caixa de seleção
check = tk.Checkbutton(janela, text="Aceito os termos", variable=var_check)
check.pack(pady=20)

# Botão para testar
btn = tk.Button(janela, text="Verificar", command=verificar_selecao)
btn.pack(pady=10)

janela.mainloop()
