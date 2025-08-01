from flask import Flask
from threading import Thread

app = Flask(__name__)

@app.get("/")
def health_check():
    return {"status": "healthy"}, 200


def run_server():
    app.run(host="0.0.0.0", port=5000)

def keep_alive():
    t = Thread(target=run_server)
    t.start()