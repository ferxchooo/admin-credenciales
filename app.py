from flask import Flask, render_template, jsonify, request
from pymongo import MongoClient

app = Flask(__name__)

# Enlace de conexión configurado con tus credenciales
MONGO_URI = "mongodb+srv://al222410839_db_user:fernando.123@cluster0.5x95bfb.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"

client = MongoClient(MONGO_URI)
db = client["portal_de_gestion"]
collection = db["credenciales"]

# --- RUTAS ---

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/api/credenciales", methods=["GET"])
def get_credenciales():
    # Obtiene todos los registros desde MongoDB
    data = list(collection.find({}, {"_id": False}))
    return jsonify(data)

@app.route("/api/credenciales/actualizar", methods=["POST"])
def actualizar_credencial():
    req_data = request.json
    num_cred = req_data.get("numero de credencial")
    
    # Actualiza los campos en MongoDB
    collection.update_one(
        {"numero de credencial": num_cred},
        {"$set": {
            "entregada": req_data.get("entregada"),
            "persona a la que se le entrego": req_data.get("persona a la que se le entrego"),
            "numero de telefono": req_data.get("numero de telefono"),
            "municipio": req_data.get("municipio"),
            "tipo de credencial": req_data.get("tipo de credencial"),
            "expedicion": req_data.get("expedicion"),
            "vigencia": req_data.get("vigencia"),
            "norma": req_data.get("norma")
        }},
        upsert=True # Crea el registro si no existe
    )
    return jsonify({"success": True, "message": "¡Actualizado en la nube con éxito!"})

if __name__ == "__main__":
    app.run(debug=True, port=5000)