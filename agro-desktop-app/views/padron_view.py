import customtkinter as ctk

class PadronView(ctk.CTkFrame):
    def __init__(self, master, api_client):
        super().__init__(master, fg_color="transparent")
        self.api_client = api_client
        
        # Contenedor principal que alternará entre Tabla y Formulario
        self.main_container = ctk.CTkFrame(self, fg_color="transparent")
        self.main_container.pack(fill="both", expand=True)
        
        # Referencias a las vistas
        self.table_view = None
        self.form_view = None
        
        self.show_table_view()
        
    def show_table_view(self):
        # Limpiar contenedor
        for widget in self.main_container.winfo_children():
            widget.destroy()
            
        self.table_view = ctk.CTkFrame(self.main_container, fg_color="transparent")
        self.table_view.pack(fill="both", expand=True)
        
        # Tarjeta blanca principal
        card = ctk.CTkFrame(self.table_view, fg_color="white", corner_radius=10, border_width=1, border_color="#e5e7eb")
        card.pack(fill="both", expand=True, padx=20, pady=(0, 20))
        
        title = ctk.CTkLabel(card, text="Lotes Registrados", font=ctk.CTkFont(size=18, weight="bold"), text_color="#1f2937")
        title.pack(anchor="w", padx=20, pady=(20, 10))
        
        # Cabecera de la tabla (sin fondo, solo texto con padding)
        header_frame = ctk.CTkFrame(card, fg_color="transparent")
        header_frame.pack(fill="x", padx=20, pady=(10, 5))
        header_frame.grid_columnconfigure((0,1,2,3,4,5,6), weight=1)
        
        headers = ["Código", "Nombre", "Cantidad (Kg)", "Tipo", "Fecha", "Inspección", "Acciones"]
        for i, h in enumerate(headers):
            ctk.CTkLabel(header_frame, text=h, font=ctk.CTkFont(weight="bold", size=13), text_color="#1f2937").grid(row=0, column=i, sticky="w")
            
        # Contenedor scrolleable
        self.scroll_table = ctk.CTkScrollableFrame(card, fg_color="transparent")
        self.scroll_table.pack(fill="both", expand=True, padx=20, pady=(0, 20))
        self.scroll_table.grid_columnconfigure((0,1,2,3,4,5,6), weight=1)
        
        self.cargar_lotes()
        
        # Botón Nuevo Lote flotante abajo a la derecha
        bottom_frame = ctk.CTkFrame(self.table_view, fg_color="transparent")
        bottom_frame.pack(fill="x", padx=20, pady=(0, 20))
        
        btn_nuevo = ctk.CTkButton(
            bottom_frame, text="+ Nuevo Lote", 
            fg_color="#046c4e", hover_color="#065f46", text_color="white",
            corner_radius=20, width=150, height=45, font=ctk.CTkFont(weight="bold", size=14),
            command=self.show_form_view
        )
        btn_nuevo.pack(side="right")
        
    def show_form_view(self):
        # Limpiar contenedor
        for widget in self.main_container.winfo_children():
            widget.destroy()
            
        self.form_view = ctk.CTkFrame(self.main_container, fg_color="transparent")
        self.form_view.pack(fill="both", expand=True)
        
        # Tarjeta blanca para el formulario
        card = ctk.CTkFrame(self.form_view, fg_color="white", corner_radius=10, border_width=1, border_color="#e5e7eb")
        card.pack(fill="x", padx=20, pady=(0, 20))
        
        title = ctk.CTkLabel(card, text="Registrar Lote de Cultivo", font=ctk.CTkFont(size=18, weight="bold"), text_color="#1f2937")
        title.grid(row=0, column=0, columnspan=2, sticky="w", padx=20, pady=(20, 20))
        
        # Fila 1
        ctk.CTkLabel(card, text="Código de Lote", font=ctk.CTkFont(weight="bold", size=13), text_color="#374151").grid(row=1, column=0, sticky="w", padx=20, pady=(0, 5))
        self.codigo_entry = ctk.CTkEntry(card, placeholder_text="LOT-Sachaca-2026-01", width=350, height=40, fg_color="white", border_color="#d1d5db")
        self.codigo_entry.grid(row=2, column=0, sticky="w", padx=20, pady=(0, 15))
        
        ctk.CTkLabel(card, text="Nombre de la Parcela", font=ctk.CTkFont(weight="bold", size=13), text_color="#374151").grid(row=1, column=1, sticky="w", padx=20, pady=(0, 5))
        self.nombre_entry = ctk.CTkEntry(card, placeholder_text="Sachaca Sector Alto", width=350, height=40, fg_color="white", border_color="#d1d5db")
        self.nombre_entry.grid(row=2, column=1, sticky="w", padx=20, pady=(0, 15))
        
        # Fila 2
        ctk.CTkLabel(card, text="Cantidad del Lote (Kg)", font=ctk.CTkFont(weight="bold", size=13), text_color="#374151").grid(row=3, column=0, sticky="w", padx=20, pady=(0, 5))
        self.cantidad_entry = ctk.CTkEntry(card, placeholder_text="500", width=350, height=40, fg_color="white", border_color="#d1d5db")
        self.cantidad_entry.grid(row=4, column=0, sticky="w", padx=20, pady=(0, 15))
        
        ctk.CTkLabel(card, text="Tipo de Producto", font=ctk.CTkFont(weight="bold", size=13), text_color="#374151").grid(row=3, column=1, sticky="w", padx=20, pady=(0, 5))
        self.tipo_combo = ctk.CTkComboBox(card, values=["Papa Única", "Papa Canchán INIA", "Papa Perricholi", "Papa Amarilla"], width=350, height=40, fg_color="white", border_color="#d1d5db")
        self.tipo_combo.grid(row=4, column=1, sticky="w", padx=20, pady=(0, 15))
        
        # Fila 3
        ctk.CTkLabel(card, text="Fecha de Ingreso", font=ctk.CTkFont(weight="bold", size=13), text_color="#374151").grid(row=5, column=0, sticky="w", padx=20, pady=(0, 5))
        self.fecha_entry = ctk.CTkEntry(card, placeholder_text="yyyy-mm-dd", width=350, height=40, fg_color="white", border_color="#d1d5db")
        self.fecha_entry.grid(row=6, column=0, sticky="w", padx=20, pady=(0, 25))
        
        ctk.CTkLabel(card, text="Cód. de Inspección", font=ctk.CTkFont(weight="bold", size=13), text_color="#374151").grid(row=5, column=1, sticky="w", padx=20, pady=(0, 5))
        self.inspeccion_entry = ctk.CTkEntry(card, placeholder_text="INS-455", width=350, height=40, fg_color="white", border_color="#d1d5db")
        self.inspeccion_entry.grid(row=6, column=1, sticky="w", padx=20, pady=(0, 25))
        
        # Botones de Acción (Fila 4)
        btn_frame = ctk.CTkFrame(card, fg_color="transparent")
        btn_frame.grid(row=7, column=0, columnspan=2, sticky="ew", padx=20, pady=(0, 20))
        btn_frame.grid_columnconfigure((0,1,2), weight=1)
        
        btn_registrar = ctk.CTkButton(btn_frame, text="Registrar en Padrón", fg_color="#046c4e", hover_color="#065f46", text_color="white", height=45, font=ctk.CTkFont(weight="bold"), command=self.registrar_lote)
        btn_registrar.grid(row=0, column=0, sticky="ew", padx=(0,10))
        
        btn_limpiar = ctk.CTkButton(btn_frame, text="Limpiar", fg_color="#e5e7eb", hover_color="#d1d5db", text_color="#374151", height=45, font=ctk.CTkFont(weight="bold"), command=self.limpiar_form)
        btn_limpiar.grid(row=0, column=1, sticky="ew", padx=10)
        
        btn_cancelar = ctk.CTkButton(btn_frame, text="Cancelar", fg_color="#fecaca", hover_color="#fca5a5", text_color="#b91c1c", height=45, font=ctk.CTkFont(weight="bold"), command=self.show_table_view)
        btn_cancelar.grid(row=0, column=2, sticky="ew", padx=(10,0))
        
        self.status_label = ctk.CTkLabel(card, text="", font=ctk.CTkFont(size=12))
        self.status_label.grid(row=8, column=0, columnspan=2, pady=(0, 10))

    def limpiar_form(self):
        self.codigo_entry.delete(0, 'end')
        self.nombre_entry.delete(0, 'end')
        self.cantidad_entry.delete(0, 'end')
        self.fecha_entry.delete(0, 'end')
        self.inspeccion_entry.delete(0, 'end')
        self.status_label.configure(text="")

    def cargar_lotes(self):
        for widget in self.scroll_table.winfo_children():
            widget.destroy()
            
        success, data = self.api_client.get_lotes()
        if success and data:
            for row_idx, lote in enumerate(data):
                # Columnas según backend: codigo, nombre, cantidad_lote, tipo_producto, fecha_ingreso, cod_inspeccion
                ctk.CTkLabel(self.scroll_table, text=lote.get("codigo", ""), text_color="#4b5563").grid(row=row_idx*2, column=0, pady=15, sticky="w")
                
                # Nombre envuelto en un frame para simular multiline si es largo
                f_nom = ctk.CTkFrame(self.scroll_table, fg_color="transparent")
                f_nom.grid(row=row_idx*2, column=1, sticky="w")
                ctk.CTkLabel(f_nom, text=lote.get("nombre", ""), text_color="#4b5563", wraplength=120, justify="left").pack(anchor="w")
                
                ctk.CTkLabel(self.scroll_table, text=str(lote.get("cantidad_lote", "")), text_color="#4b5563").grid(row=row_idx*2, column=2, pady=15, sticky="w")
                ctk.CTkLabel(self.scroll_table, text=lote.get("tipo_producto", ""), text_color="#4b5563").grid(row=row_idx*2, column=3, pady=15, sticky="w")
                ctk.CTkLabel(self.scroll_table, text=str(lote.get("fecha_ingreso", "")), text_color="#4b5563").grid(row=row_idx*2, column=4, pady=15, sticky="w")
                ctk.CTkLabel(self.scroll_table, text=lote.get("cod_inspeccion", ""), text_color="#1f2937", font=ctk.CTkFont(weight="bold")).grid(row=row_idx*2, column=5, pady=15, sticky="w")
                
                # Acciones (Lápiz y Basurero)
                actions_frame = ctk.CTkFrame(self.scroll_table, fg_color="transparent")
                actions_frame.grid(row=row_idx*2, column=6, pady=15, sticky="w")
                
                edit_btn = ctk.CTkButton(actions_frame, text="✎", width=30, height=30, fg_color="transparent", hover_color="#e0f2fe", text_color="#0284c7", font=ctk.CTkFont(size=18))
                edit_btn.pack(side="left", padx=(0, 5))
                
                delete_btn = ctk.CTkButton(
                    actions_frame, text="🗑", width=30, height=30, fg_color="transparent", hover_color="#fee2e2", text_color="#ef4444", font=ctk.CTkFont(size=18),
                    command=lambda l_id=lote.get("id"): self.eliminar_lote(l_id)
                )
                delete_btn.pack(side="left")
                
                # Línea separadora
                separator = ctk.CTkFrame(self.scroll_table, height=1, fg_color="#e5e7eb")
                separator.grid(row=row_idx*2 + 1, column=0, columnspan=7, sticky="ew")
        else:
            ctk.CTkLabel(self.scroll_table, text="No hay lotes registrados", text_color="#6b7280").grid(row=0, column=0, columnspan=7, pady=20)
            
    def registrar_lote(self):
        try:
            data = {
                "codigo": self.codigo_entry.get(),
                "nombre": self.nombre_entry.get(),
                "cantidad_lote": float(self.cantidad_entry.get()),
                "tipo_producto": self.tipo_combo.get(),
                "fecha_ingreso": self.fecha_entry.get(),
                "cod_inspeccion": self.inspeccion_entry.get()
            }
        except ValueError:
            self.status_label.configure(text="Error: Ingrese una cantidad válida (número)", text_color="#ef4444")
            return
            
        if not all(data.values()):
            self.status_label.configure(text="Complete todos los campos", text_color="#ef4444")
            return
            
        success, msg = self.api_client.create_lote(data)
        if success:
            self.show_table_view()
        else:
            self.status_label.configure(text=msg, text_color="#ef4444")

    def eliminar_lote(self, lote_id):
        success, msg = self.api_client.delete_lote(lote_id)
        if success:
            self.cargar_lotes()
