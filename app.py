from flask import Flask, jsonify, request
from models.taxi import db, Taxi
from models.trajectory import Trajectory
import config
from sqlalchemy import cast, Date
from datetime import datetime

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = config.SQLALCHEMY_DATABASE_URI

db.init_app(app)


@app.route("/taxis", methods=["GET"])
def get_taxis():
    # Parámetros de paginación y filtro
    page = request.args.get("page", default=1, type=int)
    limit = request.args.get("limit", default=10, type=int)
    plate = request.args.get("plate", default=None, type=str)

    # Consulta base
    query = Taxi.query

    # Filtro opcional por placa
    if plate:
        query = query.filter(Taxi.plate.ilike(f"%{plate}%"))

    # Paginación
    pagination = query.paginate(page=page, per_page=limit, error_out=False)

    # Armar la respuesta
    taxis = [{"id": t.id, "plate": t.plate} for t in pagination.items]

    return jsonify(taxis)

@app.route("/trajectories", methods=["GET"])
def get_trajectories():
    taxi_id = request.args.get("taxiId", default=None, type=int)
    date = request.args.get("date", default=None, type=str)

    # Validación: ambos parámetros son obligatorios → 400 si falta alguno
    if taxi_id is None:
        return jsonify({"error": "El parametro taxiId es requerido"}), 400
    if date is None:
        return jsonify({"error": "El parametro date es requerido"}), 400

    # Validar que el taxi exista → 404 si no
    taxi = Taxi.query.get(taxi_id)
    if taxi is None:
        return jsonify({"error": "Taxi no encontrado"}), 404

    # Convertir la fecha de formato DD-MM-AAAA a objeto fecha
    try:
        fecha = datetime.strptime(date, "%d-%m-%Y").date()
    except ValueError:
        return jsonify({"error": "Formato de fecha invalido, use DD-MM-AAAA"}), 400

    # Consultar trayectorias del taxi en esa fecha
    query = Trajectory.query.filter(
        Trajectory.taxi_id == taxi_id,
        cast(Trajectory.date, Date) == fecha
    )
    trajectories = query.all()

    result = [
        {
            "id": t.id,
            "latitude": t.latitude,
            "longitude": t.longitude,
            "timestamp": t.date.isoformat()
        }
        for t in trajectories
    ]

    return jsonify(result)


if __name__ == "__main__":
    app.run(debug=True)