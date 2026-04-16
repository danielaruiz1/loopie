import sqlite3

conn = sqlite3.connect('human_telemetry.db')
cursor = conn.cursor()

# Consultar los últimos 10 cambios de ventana
cursor.execute("SELECT * FROM activity_log ORDER BY timestamp DESC LIMIT 10")
rows = cursor.fetchall()

print(f"{'ID':<5} | {'Hora':<20} | {'Aplicación':<20}")
print("-" * 50)
for row in rows:
    print(f"{row[0]:<5} | {row[1]:<20} | {row[2]:<20}")

conn.close()