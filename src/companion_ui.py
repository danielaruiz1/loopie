import tkinter as tk
from tkinter import messagebox

def ask_break_intent(app_name):
    root = tk.Tk()
    root.withdraw() # Ocultar ventana principal de tkinter
    root.attributes("-topmost", True) # Que aparezca encima de todo

    # Crear una ventana personalizada
    window = tk.Toplevel(root)
    window.title("Compañero Virtual")
    window.geometry("300x150")
    
    tk.Label(window, text=f"Detecté {app_name}.\n¿Es un descanso planeado?", pady=10).pack()

    def set_timer(minutes):
        print(f"Modo descanso activado por {minutes} minutos.")
        window.destroy()
        root.destroy()
        return minutes

    btn_frame = tk.Frame(window)
    btn_frame.pack(pady=10)

    tk.Button(btn_frame, text="5 min", command=lambda: set_timer(5)).pack(side=tk.LEFT, padx=5)
    tk.Button(btn_frame, text="15 min", command=lambda: set_timer(15)).pack(side=tk.LEFT, padx=5)
    tk.Button(btn_frame, text="No, regreso al trabajo", command=window.destroy, bg="red", fg="white").pack(side=tk.LEFT, padx=5)

    window.mainloop()