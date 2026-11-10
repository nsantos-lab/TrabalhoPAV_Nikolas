import tkinter as tk
from tkinter import messagebox, ttk
from datetime import datetime
import requests
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.dates as mdates
from matplotlib.figure import Figure
from matplotlib.ticker import FormatStrFormatter


if __package__:
    from .api_urls import API_URL_AMBIENTE_TEMPO
    from .api_errors import format_api_error
else:
    from api_urls import API_URL_AMBIENTE_TEMPO
    from api_errors import format_api_error


class AmbienteTempoGraphTab:
    def build_ambiente_tempo_graph_tab(self, notebook):
        aba = tk.Frame(notebook, bg="#f5f6fa")
        notebook.add(aba, text="Ambiente Tempo (Gráfico)")
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

        # ===== AMBIENTE =====
        self.entry_ambiente_ambiente_tempo = self.criar_campo(form_frame_ambiente_tempo, "Ambiente:", 0, 0)

        # ==== SENHA ====
        self.entry_senha_ambiente_tempo = self.criar_campo(form_frame_ambiente_tempo, "Senha:", 0, 3)

        # ===== BUTTON FRAME AMBIENTE_TEMPO=====
        button_frame_ambiente_tempo = tk.Frame(aba, bg="#f5f6fa")
        button_frame_ambiente_tempo.pack(pady=30)

        # ===== CLEAR AMBIENTE_TEMPO BUTTON =====
        self.create_button(
            button_frame_ambiente_tempo,
            "Limpar",
            "#636e72",
            self.clear_graph_fields_ambiente_tempo
        ).grid(row=0, column=4, padx=0)

        # =========================== #
        # ==== AMBIENTE_TEMPO GRAPH FRAME ====
        graph_options_frame = tk.Frame(aba, bg="#f5f6fa")
        graph_options_frame.pack(padx=20, fill="x")
        tk.Label(
            graph_options_frame,
            text="Medição:",
            font=("Segoe UI", 10, "bold"),
            bg="#f5f6fa",
            fg="#2d3436"
        ).pack(side="left")
        self.graph_metric = ttk.Combobox(
            graph_options_frame,
            state="readonly",
            values=("Oxigênio", "Carbonico", "Poluentes", "Umidade", "Temperatura")
        )
        self.graph_metric.current(4)
        self.graph_metric.pack(side="left", padx=(8, 0))
        self.graph_metric.bind("<<ComboboxSelected>>", self.plot_ambiente_tempo)

        graph_frame = tk.Frame(aba, bg="#f5f6fa")
        self.create_button(
            aba,
            "Atualizar gráfico",
            "#00b894",
            self.load_ambiente_tempo_graph
        ).pack(pady=(8, 15))
        graph_frame.pack(padx=20, fill="both", expand=True)
        self.graph_figure = Figure(figsize=(7, 4))
        self.graph_axes = self.graph_figure.add_subplot(111)
        self.graph_canvas = FigureCanvasTkAgg(self.graph_figure, master=graph_frame)
        self.graph_canvas.get_tk_widget().pack(fill="both", expand=True)
        self.ambiente_tempos_publicos = []
        self.plot_ambiente_tempo()

        

        #self.root.after(100, self.load_ambiente_tempo_graph)

    def clear_graph_fields_ambiente_tempo(self):
        self.entry_ambiente_ambiente_tempo.delete(0, tk.END)
        self.entry_oxigenio_ambiente_tempo.delete(0, tk.END)
        self.entry_carbonico_ambiente_tempo.delete(0, tk.END)
        self.entry_poluentes_ambiente_tempo.delete(0, tk.END)
        self.entry_umidade_ambiente_tempo.delete(0, tk.END)
        self.entry_temperatura_ambiente_tempo.delete(0, tk.END)

    def load_ambiente_tempo_graph(self):
        try:
            id_ambiente_text = self.entry_ambiente_ambiente_tempo.get().strip()
            if not id_ambiente_text:
                raise ValueError("Informe o ID do ambiente.")

            id_ambiente_real = int(id_ambiente_text)
            id_cliente = self.get_cliente_ambiente(id_ambiente_real)
            id_banco = self.get_banco_cliente(id_cliente)
            if id_cliente is None:
                raise ValueError("Não foi possível encontrar o cliente do ambiente.")
            if not id_banco is None:
                if not self.cliente_publico(id_cliente) or not self.ambiente_publico(id_ambiente_real):
                    senha_digitada = self.entry_senha_ambiente_tempo.get()
                    if not self.dar_senha(id_banco, senha_digitada):
                        return

            response = requests.get(API_URL_AMBIENTE_TEMPO, timeout=5)
            response.raise_for_status()
            ambiente_tempos = response.json()
            if not isinstance(ambiente_tempos, list):
                raise ValueError("A resposta da API não contém uma lista de tempos de ambientes.")

            measurements = []
            for ambiente_tempo in ambiente_tempos:
                if int(ambiente_tempo.get("ambiente", -1)) != id_ambiente_real:
                    continue

                data_cadastro = ambiente_tempo.get("data_cadastro")
                if not data_cadastro:
                    raise ValueError("Uma medição não possui data de cadastro.")
                if isinstance(data_cadastro, str):
                    data_cadastro = datetime.fromisoformat(data_cadastro.replace("Z", "+00:00"))

                measurements.append((data_cadastro, ambiente_tempo))

            self.ambiente_tempos_publicos = sorted(
                measurements,
                key=lambda measurement: measurement[0]
            )
            self.plot_ambiente_tempo()
        except (requests.RequestException, ValueError, KeyError) as error:
            messagebox.showerror("Erro", f"Não foi possível carregar os tempos dos ambientes: {error}")


    def plot_ambiente_tempo(self, _event=None):
        metric_names = {
            "Oxigênio": "oxigenio",
            "Carbonico": "carbonico",
            "Poluentes": "poluentes",
            "Umidade": "umidade",
            "Temperatura": "temperatura"
        }
        metric = self.graph_metric.get()
        metric_key = metric_names[metric]

        self.graph_axes.clear()
        if self.ambiente_tempos_publicos:
            dates = [measurement[0] for measurement in self.ambiente_tempos_publicos]
            values = [
                float(measurement[1][metric_key])
                for measurement in self.ambiente_tempos_publicos
            ]
            self.graph_axes.plot(dates, values, marker="o", markersize=3, color="#0984e3")
            self.graph_axes.xaxis.set_major_formatter(mdates.DateFormatter("%d/%m %H:%M"))
            self.graph_axes.tick_params(axis="x", labelrotation=30)
            self.graph_axes.set_ylabel(metric)
            self.graph_axes.grid(True, linestyle=":", alpha=0.6)
            self.graph_axes.set_title(f"{metric} ao longo do tempo")
            self.graph_axes.yaxis.set_major_formatter(FormatStrFormatter("%.1f"))
            if min(values) == max(values):
                padding = max(abs(values[0]) * 0.1, 0.1)
                self.graph_axes.set_ylim(values[0] - padding, values[0] + padding)
                self.graph_axes.set_yticks([values[0]])
        else:
            self.graph_axes.text(
                0.5,
                0.5,
                "Nenhuma medição encontrada para este ambiente",
                ha="center",
                va="center",
                transform=self.graph_axes.transAxes
            )

        self.graph_figure.tight_layout()
        self.graph_canvas.draw()