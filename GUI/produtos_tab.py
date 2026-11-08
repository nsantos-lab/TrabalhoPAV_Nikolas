import tkinter as tk


def build_produtos_tab(notebook):
    aba_produtos = tk.Frame(notebook, bg="#f5f6fa")
    notebook.add(aba_produtos, text="Produtos")
