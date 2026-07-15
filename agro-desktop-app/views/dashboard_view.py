import customtkinter as ctk
from views.padron_view import PadronView
from PIL import Image
import os
import math

class DashboardView(ctk.CTkFrame):
    def __init__(self, master, api_client, on_logout):
        super().__init__(master, fg_color="#f3f4f6")
        self.api_client = api_client
        self.on_logout = on_logout
        
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        
        # ==================== SIDEBAR ====================
        self.sidebar_frame = ctk.CTkFrame(self, width=250, corner_radius=0, fg_color="#046c4e")
        self.sidebar_frame.grid(row=0, column=0, sticky="nsew")
        self.sidebar_frame.grid_rowconfigure(9, weight=1)
        
        self.logo_frame = ctk.CTkFrame(self.sidebar_frame, fg_color="transparent")
        self.logo_frame.grid(row=0, column=0, padx=20, pady=(20, 30), sticky="w")
        
        logo_path = os.path.join(os.path.dirname(__file__), "..", "..", "fronted", "public", "placeholder-logo.png")
        if os.path.exists(logo_path):
            img = ctk.CTkImage(light_image=Image.open(logo_path), size=(30, 30))
            self.logo_label = ctk.CTkLabel(self.logo_frame, image=img, text="")
            self.logo_label.pack(side="left")
            
        self.logo_text = ctk.CTkLabel(
            self.logo_frame, text=" AgroTalavera", 
            font=ctk.CTkFont(size=18, weight="bold"), text_color="white"
        )
        self.logo_text.pack(side="left", padx=(5,0))
        
        # Botones Sidebar
        self.btn_dashboard = self._create_sidebar_btn("Dashboard", 1, is_active=True, command=self.show_dashboard)
        self.btn_padron = self._create_sidebar_btn("Padrón de Cultivos", 2, command=self.show_padron)
        self.btn_atributos = self._create_sidebar_btn("Atributos de Control", 3)
        self.btn_evaluacion = self._create_sidebar_btn("Evaluación de Muestras", 4)
        self.btn_comparador = self._create_sidebar_btn("Comparador", 5)
        self.btn_reportes = self._create_sidebar_btn("Reportes", 6)
        self.btn_config = self._create_sidebar_btn("Configuración", 7)
        
        self.logout_btn = ctk.CTkButton(
            self.sidebar_frame, text="Cerrar Sesión", 
            fg_color="transparent", hover_color="#065f46",
            text_color="white", anchor="w", font=ctk.CTkFont(size=14),
            command=self.on_logout
        )
        self.logout_btn.grid(row=9, column=0, padx=20, pady=20, sticky="ew")
        
        # ==================== ÁREA DE CONTENIDO ====================
        self.content_container = ctk.CTkFrame(self, fg_color="transparent")
        self.content_container.grid(row=0, column=1, sticky="nsew")
        self.content_container.grid_rowconfigure(1, weight=1)
        self.content_container.grid_columnconfigure(0, weight=1)
        
        # Header
        self.header_frame = ctk.CTkFrame(self.content_container, height=60, corner_radius=0, fg_color="white", border_width=1, border_color="#e5e7eb")
        self.header_frame.grid(row=0, column=0, sticky="ew")
        self.header_frame.grid_columnconfigure(1, weight=1)
        
        self.header_title = ctk.CTkLabel(
            self.header_frame, text="Dashboard de Control", 
            font=ctk.CTkFont(size=20, weight="bold"), text_color="#111827"
        )
        self.header_title.grid(row=0, column=0, padx=20, pady=15, sticky="w")
        
        self.operator_label = ctk.CTkLabel(
            self.header_frame, text="Operador: Julio Pérez", 
            font=ctk.CTkFont(size=12), text_color="#046c4e"
        )
        self.operator_label.grid(row=0, column=2, padx=20, pady=15, sticky="e")
        
        self.main_view_frame = ctk.CTkFrame(self.content_container, fg_color="transparent")
        self.main_view_frame.grid(row=1, column=0, sticky="nsew", padx=20, pady=20)
        self.main_view_frame.grid_rowconfigure(0, weight=1)
        self.main_view_frame.grid_columnconfigure(0, weight=1)
        
        self.active_view = None
        self.show_dashboard()
        
    def _create_sidebar_btn(self, text, row, is_active=False, command=None):
        color = "#059669" if is_active else "transparent"
        btn = ctk.CTkButton(
            self.sidebar_frame, text=text, 
            fg_color=color, hover_color="#059669",
            text_color="white", anchor="w",
            font=ctk.CTkFont(size=14, weight="bold" if is_active else "normal"),
            command=command
        )
        btn.grid(row=row, column=0, padx=10, pady=5, sticky="ew")
        return btn
        
    def clear_content(self):
        if self.active_view:
            self.active_view.destroy()
            
    def _reset_sidebar(self):
        buttons = [self.btn_dashboard, self.btn_padron, self.btn_atributos, self.btn_evaluacion, self.btn_comparador, self.btn_reportes, self.btn_config]
        for btn in buttons:
            btn.configure(fg_color="transparent", font=ctk.CTkFont(size=14, weight="normal"))
            
    def show_dashboard(self):
        self.clear_content()
        self._reset_sidebar()
        self.btn_dashboard.configure(fg_color="#059669", font=ctk.CTkFont(size=14, weight="bold"))
        self.header_title.configure(text="Dashboard de Control")
        
        self.active_view = ctk.CTkFrame(self.main_view_frame, fg_color="transparent")
        self.active_view.grid(row=0, column=0, sticky="nsew")
        self.active_view.grid_rowconfigure(1, weight=1)
        self.active_view.grid_columnconfigure((0, 1, 2), weight=1)
        
        # Fila 1: Tarjetas
        cards_frame = ctk.CTkFrame(self.active_view, fg_color="transparent")
        cards_frame.grid(row=0, column=0, columnspan=3, sticky="ew", pady=(0, 20))
        cards_frame.grid_columnconfigure((0, 1, 2), weight=1)
        
        self._create_card(cards_frame, "Lotes en Padrón", "4", 0)
        self._create_card(cards_frame, "Muestras Evaluadas", "5", 1)
        self._create_card(cards_frame, "Porcentaje de Aprobación", "60.0%", 2, color="#ea580c")
        
        # Fila 2: Resumen y Actividad (Responsivo por weights)
        resumen_card = ctk.CTkFrame(self.active_view, fg_color="white", corner_radius=10, border_width=1, border_color="#e5e7eb")
        resumen_card.grid(row=1, column=0, columnspan=2, sticky="nsew", padx=(0, 10))
        
        actividad_card = ctk.CTkFrame(self.active_view, fg_color="white", corner_radius=10, border_width=1, border_color="#e5e7eb")
        actividad_card.grid(row=1, column=2, sticky="nsew", padx=(10, 0))
        
        # Llenar Resumen
        ctk.CTkLabel(resumen_card, text="Resumen de Muestras", font=ctk.CTkFont(weight="bold", size=16), text_color="#1f2937").pack(anchor="w", padx=20, pady=20)
        
        # Simulando el gráfico
        chart_frame = ctk.CTkFrame(resumen_card, fg_color="transparent")
        chart_frame.pack(expand=True, fill="both")
        
        canvas = ctk.CTkCanvas(chart_frame, width=200, height=200, bg="white", highlightthickness=0)
        canvas.pack(side="left", padx=(50, 20), expand=True)
        # Dibujar un anillo simple
        canvas.create_arc(10, 10, 190, 190, start=90, extent=216, outline="#16a34a", width=15, style="arc") # 60% verde
        canvas.create_arc(10, 10, 190, 190, start=90+216, extent=144, outline="#ef4444", width=15, style="arc") # rojo
        canvas.create_text(100, 90, text="Aprobadas", font=("Helvetica", 12), fill="#6b7280")
        canvas.create_text(100, 115, text="3", font=("Helvetica", 24, "bold"), fill="#16a34a")
        
        # Leyenda
        legend_frame = ctk.CTkFrame(chart_frame, fg_color="transparent")
        legend_frame.pack(side="left", padx=20, expand=True, anchor="w")
        
        self._add_legend_item(legend_frame, "#16a34a", "Muestras Óptimas: 3")
        self._add_legend_item(legend_frame, "#f97316", "Con Tolerancia: 0")
        self._add_legend_item(legend_frame, "#ef4444", "Con Defectos: 2")
        
        # Llenar Actividad
        ctk.CTkLabel(actividad_card, text="Actividad Reciente", font=ctk.CTkFont(weight="bold", size=16), text_color="#1f2937").pack(anchor="w", padx=20, pady=20)
        self._add_activity_item(actividad_card, "INS-459", "2026-01-23 07:30:00", False)
        self._add_activity_item(actividad_card, "INS-458", "2026-01-22 08:20:00", True)
        self._add_activity_item(actividad_card, "INS-457", "2026-01-20 11:45:00", False)
        self._add_activity_item(actividad_card, "INS-456", "2026-01-18 10:15:00", True)
        
    def _create_card(self, parent, title, value, col, color="#111827"):
        card = ctk.CTkFrame(parent, fg_color="white", corner_radius=10, border_width=1, border_color="#e5e7eb")
        card.grid(row=0, column=col, sticky="ew", padx=10 if col == 1 else (0,10) if col==0 else (10,0))
        ctk.CTkLabel(card, text=title, text_color="#6b7280", font=ctk.CTkFont(size=13)).pack(anchor="w", padx=20, pady=(20,0))
        ctk.CTkLabel(card, text=value, text_color=color, font=ctk.CTkFont(size=32, weight="bold")).pack(anchor="w", padx=20, pady=(5,20))
        
    def _add_legend_item(self, parent, color, text):
        f = ctk.CTkFrame(parent, fg_color="transparent")
        f.pack(anchor="w", pady=5)
        dot = ctk.CTkFrame(f, width=15, height=15, corner_radius=3, fg_color=color)
        dot.pack(side="left")
        ctk.CTkLabel(f, text=text, text_color="#374151").pack(side="left", padx=10)
        
    def _add_activity_item(self, parent, code, date, passed):
        f = ctk.CTkFrame(parent, fg_color="#f9fafb", corner_radius=8, border_width=1, border_color="#e5e7eb")
        f.pack(fill="x", padx=20, pady=5)
        
        left = ctk.CTkFrame(f, fg_color="transparent")
        left.pack(side="left", padx=15, pady=10)
        
        ctk.CTkLabel(left, text=code, font=ctk.CTkFont(weight="bold"), text_color="#1f2937").pack(anchor="w")
        ctk.CTkLabel(left, text=date, font=ctk.CTkFont(size=11), text_color="#9ca3af").pack(anchor="w")
        
        status_color = "#dcfce7" if passed else "#fee2e2"
        text_color = "#16a34a" if passed else "#ef4444"
        symbol = "✓" if passed else "x"
        
        badge = ctk.CTkLabel(f, text=symbol, fg_color=status_color, text_color=text_color, width=25, height=25, corner_radius=5, font=ctk.CTkFont(weight="bold"))
        badge.pack(side="right", padx=15)
        
    def show_padron(self):
        self.clear_content()
        self._reset_sidebar()
        self.btn_padron.configure(fg_color="#059669", font=ctk.CTkFont(size=14, weight="bold"))
        self.header_title.configure(text="Padrón de Cultivos")
        
        self.active_view = PadronView(self.main_view_frame, self.api_client)
        self.active_view.grid(row=0, column=0, sticky="nsew")

    def show_laboratorio(self):
        self.clear_content()
        self._reset_sidebar()
        self.btn_evaluacion.configure(fg_color="#059669", font=ctk.CTkFont(size=14, weight="bold"))
        self.header_title.configure(text="Laboratorio")
        from views.laboratorio_view import LaboratorioView
        self.active_view = LaboratorioView(self.main_view_frame, self.api_client)
        self.active_view.grid(row=0, column=0, sticky="nsew")
