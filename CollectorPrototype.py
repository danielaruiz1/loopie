# import pygetwindow as gw
# import time
# import sqlite3
# from datetime import datetime

# # Configuración de la base de datos
# def setup_db():
#     conn = sqlite3.connect('human_telemetry.db')
#     cursor = conn.cursor()
#     cursor.execute('''
#         CREATE TABLE IF NOT EXISTS activity_log (
#             id INTEGER PRIMARY KEY AUTOINCREMENT,
#             timestamp DATETIME,
#             app_name TEXT,
#             window_title TEXT
#         )
#     ''')
#     conn.commit()
#     return conn

# def log_activity():
#     conn = setup_db()
#     cursor = conn.cursor()
#     last_window = None
    
#     print("Colector iniciado. Presiona Ctrl+C para detener.")
    
#     try:
#         while True:
#             try:
#                 # Obtener la ventana activa actual
#                 active_window = gw.getActiveWindow()
                
#                 if active_window and active_window.title != last_window:
#                     app_name = active_window.title.split('-')[-1].strip()
#                     now = datetime.now().isoformat()
                    
#                     # Guardar en la base de datos
#                     cursor.execute(
#                         "INSERT INTO activity_log (timestamp, app_name, window_title) VALUES (?, ?, ?)",
#                         (now, app_name, active_window.title)
#                     )
#                     conn.commit()
                    
#                     print(f"[{now}] Cambio detectado: {app_name}")
#                     last_window = active_window.title
                    
#             except Exception as e:
#                 # Manejar casos donde la ventana no tiene título o desaparece rápido
#                 pass
                
#             time.sleep(2) # Poll cada 2 segundos para no saturar el CPU
#     except KeyboardInterrupt:
#         print("\nColector detenido.")
#     finally:
#         conn.close()

# if __name__ == "__main__":
#     log_activity()