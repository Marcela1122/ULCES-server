from flask import Flask
from app.endpoints.main import bp_main
from app.endpoints.image import bp_image


def create_app(class_config='config.Developement'):
    app = Flask(__name__)
    app.config.from_object(class_config)

    # Register blueprints
    app.register_blueprint(bp_main)
    app.register_blueprint(bp_image)
    return app