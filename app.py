from flask import Flask, request
import psycopg

app = Flask(__name__)

DB_HOST = "db"
DB_NAME = "myapp"
DB_USER = "appuser"
DB_PASS = "apppassword"


def get_connection():
    return psycopg.connect(
        host=DB_HOST,
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASS
    )


@app.route("/")
def home():
    return "<h1>Hello Docker! 🚀</h1>"


@app.route("/add")
def add():

    nama = request.args.get("nama")

    if not nama:
        return "Contoh penggunaan: /add?nama=Altov"

    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        CREATE TABLE IF NOT EXISTS mahasiswa(
            id SERIAL PRIMARY KEY,
            nama VARCHAR(100)
        )
    """)

    cur.execute(
        "INSERT INTO mahasiswa(nama) VALUES (%s)",
        (nama,)
    )

    conn.commit()

    cur.close()
    conn.close()

    return f"Data {nama} berhasil ditambahkan."


@app.route("/list")
def list_data():

    conn = get_connection()
    cur = conn.cursor()

    cur.execute("SELECT * FROM mahasiswa")

    rows = cur.fetchall()

    cur.close()
    conn.close()

    html = "<h2>Data Mahasiswa</h2><ul>"

    for row in rows:
        html += f"<li>{row[0]} - {row[1]}</li>"

    html += "</ul>"

    return html


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
