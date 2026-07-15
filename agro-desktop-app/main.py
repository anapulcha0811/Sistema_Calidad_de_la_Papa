import customtkinter as ctk
from api_client import APIClient
from views.login_view import LoginView
from views.dashboard_view import DashboardView

# Configuración del tema
ctk.set_appearance_mode("light")
ctk.set_default_color_theme("green")

class AgroApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        self.title("AgroTalavera - Sistema de Control")
        self.geometry("900x600")
        self.minsize(800, 500)
        
        self.api = APIClient()
        self.current_frame = None
        
        self.show_login()
        
    def show_login(self):
        if self.current_frame:
            self.current_frame.destroy()
        self.current_frame = LoginView(self, self.api, self.show_dashboard)
        self.current_frame.pack(fill="both", expand=True)
        
    def show_dashboard(self):
        if self.current_frame:
            self.current_frame.destroy()
        self.current_frame = DashboardView(self, self.api, self.show_login)
        self.current_frame.pack(fill="both", expand=True)

if __name__ == "__main__":
    app = AgroApp()
    app.mainloop()
