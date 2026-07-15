import customtkinter as ctk

class LaboratorioView(ctk.CTkFrame):
    def __init__(self, master, api_client):
        super().__init__(master, fg_color="transparent")
        self.api_client = api_client
        
        # Título principal
        self.title_label = ctk.CTkLabel(
            self, text="Registro de Atributos de Control (Laboratorio)", 
            font=ctk.CTkFont(size=22, weight="bold"), text_color="#111827"
        )
        self.title_label.pack(anchor="w", padx=20, pady=(0, 5))
        
        self.subtitle = ctk.CTkLabel(
            self, text="Ingrese los parámetros físicos y químicos de la muestra", 
            font=ctk.CTkFont(size=12), text_color="#6b7280"
        )
        self.subtitle.pack(anchor="w", padx=20, pady=(0, 20))
        
        # Tarjeta del Formulario (blanca)
        self.form_card = ctk.CTkFrame(self, fg_color="white", corner_radius=10, border_width=1, border_color="#e5e7eb", width=600)
        self.form_card.pack(fill="both", expand=True, padx=20, pady=(0, 20))
        self.form_card.grid_columnconfigure((0, 1), weight=1)
        
        # Selección de Lote
        ctk.CTkLabel(self.form_card, text="Selección de Lote", font=ctk.CTkFont(weight="bold", size=13), text_color="#374151").grid(row=0, column=0, columnspan=2, sticky="w", padx=20, pady=(20, 5))
        
        self.lote_combo = ctk.CTkComboBox(self.form_card, values=["Cargando lotes..."], width=560, height=35, fg_color="#f9fafb", border_color="#d1d5db", text_color="black")
        self.lote_combo.grid(row=1, column=0, columnspan=2, padx=20, pady=(0, 15), sticky="w")
        
        # Código de Inspección
        ctk.CTkLabel(self.form_card, text="Cód. de Inspección de Muestra", font=ctk.CTkFont(weight="bold", size=13), text_color="#374151").grid(row=2, column=0, columnspan=2, sticky="w", padx=20, pady=(0, 5))
        self.codigo_entry = ctk.CTkEntry(self.form_card, placeholder_text="Ej. INS-455", width=560, height=35, fg_color="#f9fafb", border_color="#d1d5db", text_color="black")
        self.codigo_entry.grid(row=3, column=0, columnspan=2, padx=20, pady=(0, 15), sticky="w")
        
        # Peso y Almidón
        ctk.CTkLabel(self.form_card, text="Peso de Muestra (g)", font=ctk.CTkFont(weight="bold", size=13), text_color="#374151").grid(row=4, column=0, sticky="w", padx=20, pady=(0, 5))
        self.peso_entry = ctk.CTkEntry(self.form_card, placeholder_text="245.5", height=35, fg_color="#f9fafb", border_color="#d1d5db", text_color="black")
        self.peso_entry.grid(row=5, column=0, padx=20, pady=(0, 15), sticky="we")
        
        ctk.CTkLabel(self.form_card, text="Porcentaje de Almidón (%)", font=ctk.CTkFont(weight="bold", size=13), text_color="#374151").grid(row=4, column=1, sticky="w", padx=20, pady=(0, 5))
        self.almidon_entry = ctk.CTkEntry(self.form_card, placeholder_text="18.5", height=35, fg_color="#f9fafb", border_color="#d1d5db", text_color="black")
        self.almidon_entry.grid(row=5, column=1, padx=20, pady=(0, 15), sticky="we")
        
        # Textura y Color
        ctk.CTkLabel(self.form_card, text="Textura de la Papa", font=ctk.CTkFont(weight="bold", size=13), text_color="#374151").grid(row=6, column=0, sticky="w", padx=20, pady=(0, 5))
        self.textura_combo = ctk.CTkComboBox(self.form_card, values=["Sólida (Óptima)", "Firme", "Arenosa", "Flácida (Defecto)"], height=35, fg_color="#f9fafb", border_color="#d1d5db", text_color="black")
        self.textura_combo.grid(row=7, column=0, padx=20, pady=(0, 15), sticky="we")
        
        ctk.CTkLabel(self.form_card, text="Color de la Pulpa", font=ctk.CTkFont(weight="bold", size=13), text_color="#374151").grid(row=6, column=1, sticky="w", padx=20, pady=(0, 5))
        self.color_combo = ctk.CTkComboBox(self.form_card, values=["Amarillo Claro", "Blanco", "Rosáceo", "Crema"], height=35, fg_color="#f9fafb", border_color="#d1d5db", text_color="black")
        self.color_combo.grid(row=7, column=1, padx=20, pady=(0, 15), sticky="we")
        
        # Tamaño
        ctk.CTkLabel(self.form_card, text="Tamaño de la Muestra (tubérculos)", font=ctk.CTkFont(weight="bold", size=13), text_color="#374151").grid(row=8, column=0, columnspan=2, sticky="w", padx=20, pady=(0, 5))
        self.tamano_entry = ctk.CTkEntry(self.form_card, placeholder_text="25", width=560, height=35, fg_color="#f9fafb", border_color="#d1d5db", text_color="black")
        self.tamano_entry.grid(row=9, column=0, columnspan=2, padx=20, pady=(0, 25), sticky="w")
        
        # Botón Submit
        self.submit_btn = ctk.CTkButton(
            self.form_card, text="Registrar Atributos de Calidad", 
            width=560, height=45, fg_color="#046c4e", hover_color="#065f46", 
            font=ctk.CTkFont(weight="bold", size=15), text_color="white",
            command=self.registrar_laboratorio
        )
        self.submit_btn.grid(row=10, column=0, columnspan=2, padx=20, pady=(0, 10))
        
        self.status_label = ctk.CTkLabel(self.form_card, text="", font=ctk.CTkFont(size=12, weight="bold"))
        self.status_label.grid(row=11, column=0, columnspan=2, pady=(0, 20))
        
        self.cargar_lotes()
        
    def cargar_lotes(self):
        success, data = self.api_client.get_lotes()
        if success and data:
            lotes_list = [f"{l['id']} - {l['productor']} ({l['variedad']})" for l in data]
            self.lote_combo.configure(values=lotes_list)
            self.lote_combo.set(lotes_list[0])
        else:
            self.lote_combo.configure(values=["No hay lotes registrados"])
            self.lote_combo.set("No hay lotes registrados")
            
    def registrar_laboratorio(self):
        lote = self.lote_combo.get()
        codigo = self.codigo_entry.get()
        peso = self.peso_entry.get()
        almidon = self.almidon_entry.get()
        textura = self.textura_combo.get()
        color = self.color_combo.get()
        tamano = self.tamano_entry.get()
        
        if not (lote and codigo and peso and almidon and tamano):
            self.status_label.configure(text="Error: Complete todos los campos", text_color="#ef4444")
            return
            
        # Simulación de envío
        self.status_label.configure(text="✔ Atributos de calidad registrados exitosamente", text_color="#16a34a")
        
        # Limpiar
        self.codigo_entry.delete(0, 'end')
        self.peso_entry.delete(0, 'end')
        self.almidon_entry.delete(0, 'end')
        self.tamano_entry.delete(0, 'end')
