from flask import Flask, render_template, jsonify, request
from pymongo import MongoClient

app = Flask(__name__)

# Enlace a tu MongoDB Atlas
MONGO_URI = "mongodb+srv://al222410839_db_user:fernando.123@cluster0.5x95bfb.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"

client = MongoClient(MONGO_URI)
db = client["portal_de_gestion"]
collection = db["credenciales"]

@app.route("/")
def index():
    # 1. Total absoluto de registros en la colección
    total_registradas = collection.count_documents({})

    # 2. Conteo de Acreditación (incluye variaciones)
    acreditacion_inicial = collection.count_documents({
        "tipo de tramite": {"$regex": r"^acreditaci[oó]n", "$options": "i"}
    })
    
    # 3. Conteo exclusivo de Refrendos
    refrendos = collection.count_documents({
        "tipo de tramite": {"$regex": r"^refrendo", "$options": "i"}
    })

    # 4. Conteo exclusivo de Canjes
    canjes = collection.count_documents({
        "tipo de tramite": {"$regex": r"^canje", "$options": "i"}
    })

    # 5. Conteo de Entregadas
    entregadas = collection.count_documents({
        "entregada": {"$in": ["Sí", "Si", "si", "SI", "SÍ", True]}
    })

    # Enviamos los conteos a la plantilla index.html
    return render_template(
        "index.html",
        total=total_registradas,
        acreditacion=acreditacion_inicial,
        refrendos=refrendos,
        canjes=canjes,
        entregadas=entregadas
    )

@app.route("/api/credenciales", methods=["GET"])
def get_credenciales():
    return jsonify(list(collection.find({}, {"_id": False})))

@app.route("/api/credenciales/actualizar", methods=["POST"])
def actualizar_credencial():
    req_data = request.json
    num_cred = req_data.get("numero de credencial")
    
    # Aquí estamos enviando todos los datos al mismo tiempo
    collection.update_one(
        {"numero de credencial": num_cred},
        {"$set": {
            "nombre": req_data.get("nombre"),
            "tipo de tramite": req_data.get("tipo de tramite"),
            "entregada": req_data.get("entregada"),
            "persona a la que se le entrego": req_data.get("persona a la que se le entrego"),
            "numero de telefono": req_data.get("numero de telefono"),
            "municipio": req_data.get("municipio"),
            "tipo de credencial": req_data.get("tipo de credencial"),
            "expedicion": req_data.get("expedicion"),
            "vigencia": req_data.get("vigencia"),
            "norma": req_data.get("norma")
        }},
        upsert=True
    )
    return jsonify({"success": True})

if __name__ == "__main__":
    app.run()
