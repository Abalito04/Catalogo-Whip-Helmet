import os
import psycopg2

DATABASE_URL = os.getenv("DATABASE_URL")

if DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)

conn = psycopg2.connect(DATABASE_URL)
cur = conn.cursor()

cur.execute("ALTER TABLE cascos ADD COLUMN IF NOT EXISTS precio_1_cuota FLOAT;")
cur.execute("ALTER TABLE cascos ADD COLUMN IF NOT EXISTS precio_3_cuotas FLOAT;")
cur.execute("ALTER TABLE cascos ADD COLUMN IF NOT EXISTS precio_6_cuotas FLOAT;")

conn.commit()
cur.close()
conn.close()

print("✅ Migración completada sin perder datos")
