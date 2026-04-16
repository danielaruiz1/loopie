# =================================================================
# Loopie™ - Telemetry Collector Module
# Ingestion engine for window activity and system events
# © 2026 Daniela Ruiz. All rights reserved.
# =================================================================

import pygetwindow as gw
import time
import sqlite3
from datetime import datetime
import os

DB_PATH = os.path.join('data', 'human_telemetry.db')
os.makedirs('data', exist_ok=True)

def setup_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS activity_log (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp DATETIME,
            app_name TEXT,
            window_title TEXT
        )
    ''')
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS daily_summary (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        fecha DATE,
        minutos_totales REAL,
        eficiencia_porcentaje REAL,
        estado_predominante TEXT
    )
    ''')
    conn.commit()
    return conn

def start_collecting():
    conn = setup_db()
    cursor = conn.cursor()
    last_window = None
    
    print("Colector iniciado. Presiona Ctrl+C para detener.")
    
    try:
        while True:
            try:
                active_window = gw.getActiveWindow()
                
                if active_window and active_window.title != last_window:
                    app_name = active_window.title.split('-')[-1].strip()
                    now = datetime.now().isoformat()
                    
                    cursor.execute(
                        "INSERT INTO activity_log (timestamp, app_name, window_title) VALUES (?, ?, ?)",
                        (now, app_name, active_window.title)
                    )
                    conn.commit()
                    
                    print(f"[{now}] Cambio detectado: {app_name}")
                    last_window = active_window.title
                    
            except Exception as e:
                pass
                
            time.sleep(2)
    except KeyboardInterrupt:
        print("\nColector detenido.")
    finally:
        conn.close()