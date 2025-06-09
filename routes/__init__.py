from .chat_routes import chat_bp
from .widget_routes import widget_bp

def register_routes(app):
    app.register_blueprint(chat_bp)
    app.register_blueprint(widget_bp)
