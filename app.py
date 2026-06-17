from flask import Flask, jsonify, request
from models.taxi import db, Taxi
import config

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


if __name__ == "__main__":
    app.run(debug=True)