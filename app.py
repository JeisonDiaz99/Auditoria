from flask import Flask
from src.routes.index import index_bp
from src.settings import Settings


settings_module = Settings.get_config()

app = Flask(__name__, instance_relative_config=True, template_folder='src/templates', static_folder='src/static')
app.config.from_object(settings_module)

app.register_blueprint(index_bp, url_prefix="/")

if __name__ == "__main__":
    app.run(debug=settings_module.DEBUG, host="0.0.0.0", port=5001)