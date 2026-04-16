# =========================================================
# Loopie™ - Your Mindful Companion
# ---------------------------------------------------------
# Version: 1.0.0
# Author: Daniela Ruiz (@danielaruiz1)
# License: MIT
# © 2026 Daniela Ruiz. All rights reserved.
# =========================================================

import threading
import time
import os
from src.collector import start_collecting
from src.analyzer import get_report

def clear_console():
    os.system('cls' if os.name == 'nt' else 'clear')

def main():
    # Iniciar colector en segundo plano
    t = threading.Thread(target=start_collecting, daemon=True)
    t.start()
    
    print("--- Human Telemetry Companion Activo ---")
    print("Monitoreando actividad... El primer reporte saldrá en breve.")

    try:
        while True:
            time.sleep(15) # Esperar 15 segundos entre actualizaciones
            report = get_report(hours=1)
            
            if isinstance(report, dict):
                clear_console()
                print("========================================")
                print("   INFORME DE TELEMETRÍA HUMANA")
                print("========================================")
                print(f"Estado Actual: {report['estado']}")
                print(f"Tiempo monitoreado: {report['total_min']:.1f} min")
                print("----------------------------------------")
                print(f"MÉTRICAS:")
                print(f"- Cambios de Contexto: {report['switches']}")
                print(f"- Tiempo en Foco: {report['time_per_cat']['Productivo']:.1f} min")
                print(f"- Tiempo en Distracción: {report['time_per_cat']['Distracción']:.1f} min")
                print("----------------------------------------")
                print("TOP 3 APLICACIONES:")
                for i, (app, t_min) in enumerate(report['top_apps'], 1):
                    print(f"{i}. {app} ({t_min:.1f} min)")
                print("========================================\n")
                print("Presiona Ctrl+C para salir.")
            else:
                print(f"\r{report}", end="")

    except KeyboardInterrupt:
        print("\n\n--- Generando Resumen de Jornada... ---")
        from src.analyzer import generate_final_summary
        mensaje = generate_final_summary()
        print(mensaje)
        print("Cerrando sistema... ¡Descansa, Daniela!")

if __name__ == "__main__":
    main()