# =================================================================
# Loopie™ - Analysis Engine
# Logic for context-switching and telemetry processing
# © 2026 Daniela Ruiz. All rights reserved.
# =================================================================

import sqlite3
import os
from datetime import datetime, timedelta

# Ruta absoluta para evitar errores de base de datos
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_PATH = os.path.join(BASE_DIR, 'data', 'human_telemetry.db')

# Configuración de categorías por palabras clave
KEYWORDS = {
    "Distracción": ['roblox', 'facebook', 'instagram', 'tiktok', 'amazon', 'mercadolibre', 'shopee', 'netflix', 'juego', 'compra'],
    "Comunicación": ['whatsapp', 'slack', 'outlook', 'teams', 'discord', 'gmail', 'messenger'],
    "Productivo": ['visual studio code', 'vscode', 'terminal', 'powershell', 'github', 'stackoverflow', 'overleaf', 'python']
}

def get_category(title):
    title_low = title.lower()
    for cat, words in KEYWORDS.items():
        if any(word in title_low for word in words):
            return cat
    return "Otros/Navegación General"

def get_report(hours=1):
    if not os.path.exists(DB_PATH):
        return "Error: Base de datos no encontrada."

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    since = (datetime.now() - timedelta(hours=hours)).isoformat()
    cursor.execute("SELECT timestamp, app_name, window_title FROM activity_log WHERE timestamp > ? ORDER BY timestamp ASC", (since,))
    rows = cursor.fetchall()
    conn.close()

    if len(rows) < 2:
        return "Esperando más datos para generar el primer reporte..."

    # Diccionarios para estadísticas
    time_per_app = {}
    time_per_cat = {"Distracción": 0, "Comunicación": 0, "Productivo": 0, "Otros/Navegación General": 0}
    switches = len(rows) - 1

    # Cálculo de tiempos entre registros
    for i in range(len(rows) - 1):
        t1 = datetime.fromisoformat(rows[i][0])
        t2 = datetime.fromisoformat(rows[i+1][0])
        duration = (t2 - t1).total_seconds() / 60 # Convertir a minutos
        
        app = rows[i][1]
        title = rows[i][2]
        cat = get_category(title)

        time_per_app[app] = time_per_app.get(app, 0) + duration
        time_per_cat[cat] += duration

    # Ordenar apps por tiempo (Top 3)
    top_apps = sorted(time_per_app.items(), key=lambda x: x[1], reverse=True)[:3]
    total_time = sum(time_per_cat.values())
    
    # Determinar Estado
    if total_time == 0: return "Sin actividad significativa."
    
    dist_ratio = time_per_cat["Distracción"] / total_time
    if dist_ratio > 0.20: estado = "⚠️ DISTRAÍDO"
    elif switches > 25: estado = "🌀 FRAGMENTADO"
    elif time_per_cat["Productivo"] / total_time > 0.6: estado = "✅ ENFOQUE PROFUNDO"
    else: estado = "😐 ACTIVIDAD MIXTA"

    return {
        "estado": estado,
        "switches": switches,
        "time_per_cat": time_per_cat,
        "top_apps": top_apps,
        "total_min": total_time
    }

def generate_final_summary():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Obtener todo lo de hoy
    hoy = datetime.now().strftime('%Y-%m-%d')
    cursor.execute("SELECT timestamp, app_name, window_title FROM activity_log WHERE timestamp LIKE ? ORDER BY timestamp ASC", (f"{hoy}%",))
    rows = cursor.fetchall()
    
    if len(rows) < 2:
        return "No hay suficiente actividad hoy para un resumen."

    stats = {"Distracción": 0, "Comunicación": 0, "Productivo": 0, "Otros/Navegación General": 0}
    
    for i in range(len(rows) - 1):
        t1 = datetime.fromisoformat(rows[i][0])
        t2 = datetime.fromisoformat(rows[i+1][0])
        duration = (t2 - t1).total_seconds() / 60
        stats[get_category(rows[i][2])] += duration

    total_min = sum(stats.values())
    eficiencia = (stats["Productivo"] / total_min * 100) if total_min > 0 else 0
    
    # Guardar en TXT para que Daniela lo vea fácil
    with open("resumen_jornada.txt", "a", encoding="utf-8") as f:
        f.write(f"\n{'='*30}\n")
        f.write(f"RESUMEN DEL DÍA: {hoy}\n")
        f.write(f"Tiempo Total: {total_min:.1f} min\n")
        f.write(f"Eficiencia: {eficiencia:.1f}%\n")
        f.write(f"Distribución:\n")
        for cat, t in stats.items():
            f.write(f" - {cat}: {t:.1f} min\n")
        f.write(f"{'='*30}\n")
    
    return f"¡Resumen guardado! Eficiencia hoy: {eficiencia:.1f}%"