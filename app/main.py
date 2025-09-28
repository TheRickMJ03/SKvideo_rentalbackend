from flask import Flask
from app.routes.films import films_bp   
from app.routes.actor import actor_bp
from app.routes.customers import customer_bp
from app.routes.top_films import top_filmsbp
from app.routes.alldata import alldatabp
from flask_cors import CORS


def create_app():
    app = Flask(__name__)
    
    CORS(app) 
    # register routes
    app.register_blueprint(films_bp)
    app.register_blueprint(actor_bp)
    app.register_blueprint(customer_bp)
    app.register_blueprint(top_filmsbp)
    app.register_blueprint(alldatabp)


    
    return app

if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)
