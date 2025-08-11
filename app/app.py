from flask import Flask, request, redirect
import mysql.connector, os

app = Flask(__name__)


def get_db():
    return mysql.connector.connect(
        host=os.getenv("DB_HOST", "mysql"),
        user=os.getenv("DB_USER", "todo"),
        password=os.getenv("DB_PASSWORD", "todopass"),
        database=os.getenv("DB_NAME", "todoapp"),
    )


@app.route("/", methods=["GET", "POST"])
def index():
    conn = get_db()
    cur = conn.cursor(dictionary=True)
    cur.execute(
        "CREATE TABLE IF NOT EXISTS todos (id INT AUTO_INCREMENT PRIMARY KEY, text VARCHAR(255))"
    )
    if request.method == "POST":
        cur.execute("INSERT INTO todos (text) VALUES (%s)", (request.form["text"],))
        conn.commit()
        cur.close()
        conn.close()
        return redirect("/")
    cur.execute("SELECT id, text FROM todos")
    rows = cur.fetchall()
    cur.close()
    conn.close()
    html = "<form method='post'><input name='text'><button>Add</button></form><ul>"
    for r in rows:
        html += f"<li>{r['text']}</li>"
    return html + "</ul>"


@app.route("/health")
def health():
    return "OK", 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
