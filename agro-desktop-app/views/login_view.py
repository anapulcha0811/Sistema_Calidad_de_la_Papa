import customtkinter as ctk
from PIL import Image
import os

class LoginView(ctk.CTkFrame):
    def __init__(self, master, api_client, on_success):
        super().__init__(master, fg_color="#f9fafb") # Fondo gris clarito web
        self.api_client = api_client
        self.on_success = on_success
        
        # Center container (Card blanca)
        self.container = ctk.CTkFrame(
            self, 
            width=450, 
            corner_radius=10, 
            fg_color="#ffffff", # Fondo blanco puro
            border_width=1,
            border_color="#e5e7eb" # Borde gris muy sutil como sombra
        )
        self.container.pack(expand=True, pady=40)
        
        # Header Box
        self.header_frame = ctk.CTkFrame(self.container, fg_color="transparent")
        self.header_frame.pack(pady=(40, 20), fill="x", padx=40)
        
        # Intentar cargar logo (placeholder_logo.png)
        logo_path = os.path.join(os.path.dirname(__file__), "..", "..", "fronted", "public", "placeholder-logo.png")
        if os.path.exists(logo_path):
            img = ctk.CTkImage(light_image=Image.open(logo_path), size=(60, 60))
            self.logo_label = ctk.CTkLabel(self.header_frame, image=img, text="")
            self.logo_label.pack(pady=(0, 10))
            
        self.title = ctk.CTkLabel(
            self.header_frame, 
            text="AgroTalavera", 
            font=ctk.CTkFont(family="Helvetica", size=24, weight="bold"),
            text_color="#111827"
        )
        self.title.pack(pady=(0, 5))
        
        self.subtitle = ctk.CTkLabel(
            self.header_frame, 
            text="Sistema de Información para determinar la calidad de la papa", 
            font=ctk.CTkFont(family="Helvetica", size=11),
            text_color="#6b7280"
        )
        self.subtitle.pack()
        
        # Form Box
        self.form_frame = ctk.CTkFrame(self.container, fg_color="transparent")
        self.form_frame.pack(fill="x", padx=40, pady=(10, 30))
        
        # Usuario
        self.user_label = ctk.CTkLabel(
            self.form_frame, text="Usuario", text_color="#374151", 
            font=ctk.CTkFont(weight="bold", size=12)
        )
        self.user_label.pack(anchor="w", pady=(0, 5))
        
        self.user_entry = ctk.CTkEntry(
            self.form_frame, 
            placeholder_text="ej. teriyaki", 
            width=350, 
            height=45,
            fg_color="#fefce8", # Fondo amarillento como la imagen
            text_color="#111827",
            border_color="#fef08a",
            border_width=2,
            corner_radius=6
        )
        self.user_entry.pack(pady=(0, 15))
        
        # Contraseña
        self.pass_label = ctk.CTkLabel(
            self.form_frame, text="Contraseña", text_color="#374151", 
            font=ctk.CTkFont(weight="bold", size=12)
        )
        self.pass_label.pack(anchor="w", pady=(0, 5))
        
        self.pass_entry = ctk.CTkEntry(
            self.form_frame, 
            placeholder_text="••••••••", 
            show="*", 
            width=350, 
            height=45,
            fg_color="#fefce8",
            text_color="#111827",
            border_color="#fef08a",
            border_width=2,
            corner_radius=6
        )
        self.pass_entry.pack(pady=(0, 5))
        
        # Error Label
        self.error_label = ctk.CTkLabel(
            self.form_frame, 
            text="", 
            text_color="#ef4444",
            font=ctk.CTkFont(size=12, weight="bold")
        )
        self.error_label.pack(pady=(0, 10))
        
        # Login Button
        self.login_btn = ctk.CTkButton(
            self.form_frame, 
            text="Ingresar al Sistema", 
            width=350, 
            height=45,
            fg_color="#046c4e", # Verde oscuro (Tailwind bg-green-800)
            hover_color="#065f46",
            text_color="white",
            corner_radius=6,
            font=ctk.CTkFont(weight="bold", size=14),
            command=self.handle_login
        )
        self.login_btn.pack(pady=(5, 20))
        
        # Footer
        self.footer = ctk.CTkLabel(
            self.form_frame, 
            text="¿Olvidó sus credenciales? Contacte al administrador técnico", 
            text_color="#046c4e", # Color verde para simular link
            font=ctk.CTkFont(size=11, weight="bold")
        )
        self.footer.pack(pady=(10, 0))
        
    def handle_login(self):
        user = self.user_entry.get()
        pwd = self.pass_entry.get()
        
        if not user or not pwd:
            self.error_label.configure(text="Por favor ingrese todos los datos")
            return
            
        self.error_label.configure(text="Conectando...", text_color="#16a34a")
        self.login_btn.configure(state="disabled", fg_color="#6ee7b7")
        
        # Call API
        self.after(100, self._process_login, user, pwd)
        
    def _process_login(self, user, pwd):
        success, msg = self.api_client.login(user, pwd)
        
        if success:
            self.on_success()
        else:
            self.error_label.configure(text=msg, text_color="#ef4444")
            self.login_btn.configure(state="normal", fg_color="#046c4e")
