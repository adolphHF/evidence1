from flask import Flask, jsonify, session
from city_model.model import CityModel

model = None 

def create_app():
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
    )

    @app.route('/healthz')
    def healthz():
        return jsonify({"message": "server is running"}), 200
    
    @app.route('/init')
    def init():
        global model
        model = CityModel(width=24, height=24, num_buildings=11, num_parking=17, num_cars=30, seed=420)
        car_data = model.get_car_positions()
        return jsonify(car_data), 200
    
    @app.route('/step')
    def step():
        if not model:
            return jsonify({"message": "Model not initialized}"}), 400
        model.step()
        car_data = model.get_car_positions()
        return jsonify(car_data), 200

    return app