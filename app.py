import os
import psycopg2
from dotenv import load_dotenv
from flask import *
from flask_cors import CORS


load_dotenv()

INSERT_PRICE = "INSERT INTO prices (price) VALUES (%s)"
INSERT_TEXT = "INSERT INTO texts (text) VALUES (%s)"
SELECT_PRICE = "SELECT * FROM prices WHERE price_id = (%s)"
SELECT_TEXT = "SELECT * FROM texts WHERE text_id = (%s)"
UPDATE_TEXT = "UPDATE texts SET text = (%s) WHERE text_id = (%s)"
UPDATE_PRICE = "UPDATE prices SET price = (%s) WHERE price_id = (%s)"
SELECT_ALL_TEXT = "SELECT * FROM texts ORDER BY text_id"
app = Flask(__name__)
CORS(app)
url = os.getenv("DATABASE_URL")
connection = psycopg2.connect(url)


@app.post("/api/create/price")
def create_price():
    data = request.get_json()
    preco = data["price"]
    with connection:
        with connection.cursor() as cursor:
            cursor.execute(INSERT_PRICE, (preco,))
    return "201"


@app.post("/api/create/text")
def create_text():
    data = request.get_json()
    text = data["text"]
    with connection:
        with connection.cursor() as cursor:
            cursor.execute(INSERT_TEXT, (text,))
    return "201"


@app.route("/api/update/text", methods=["GET", "POST"])
def update_text():
    data = json.loads(request.data)
    text = data["text"]
    id = data["id"]
    with connection:
        with connection.cursor() as cursor:
            cursor.execute(UPDATE_TEXT, (text, id))
    return "201"


@app.route("/api/update/price", methods=["GET", "POST"])
def update_price():
    data = json.loads(request.data)
    print(data)
    price = data["price"]
    id = data["id"]
    with connection:
        with connection.cursor() as cursor:
            cursor.execute(UPDATE_PRICE, (price, id))
    return "201"


@app.get("/api/get/text")
def get_text():
    id = request.args.get("id")
    with connection:
        with connection.cursor() as cursor:
            cursor.execute(SELECT_TEXT, (id,))
            texstos = cursor.fetchall()[0]
            response = make_response(texstos[1])
            response.mimetype = "text/plain"
            print(response.mimetype)

    return response

@app.get("/api/get/price")
def get_price():
    id = request.args.get("id")
    with connection:
        with connection.cursor() as cursor:
            cursor.execute(SELECT_PRICE, (id,))
            precos = cursor.fetchall()[0]
    return str(precos[1])

@app.get("/api/get/all/text")
def get_all_texts():
    with connection:
        with connection.cursor() as cursor:
            cursor.execute(SELECT_ALL_TEXT)
            texstos = cursor.fetchall()
            texstos = dict(texstos)
    return jsonify(texstos)

