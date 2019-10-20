import sys
import logging
from flask import Flask, g
from flask import render_template

def create_app():
    """Construct the core application."""
    app = Flask(__name__)
    app.config.from_object(__name__)
    app.config.from_envvar('APP_CONFIG_FILE', silent=True)
    with app.app_context():
        register_extensions(app)
        register_blueprints(app)
        register_errorhandlers(app)
        register_shellcontext(app)
        configure_logger(app)

    return app


def register_extensions(app):
    """Register Flask extensions."""
    return None


def register_blueprints(app):
    """Register Flask blueprints."""
    from clips.maps import route
    app.register_blueprint(route.map_blueprint)
    return None


def register_errorhandlers(app):
    """Register error handlers."""

    def render_error(error):
        """Render error template."""
        # If a HTTPException, pull the `code` attribute; default to 500
        error_code = getattr(error, "code", 500)
        return render_template("{0}.html".format(error_code)), error_code

    for errcode in [401, 404, 500]:
        app.errorhandler(errcode)(render_error)
    return None


def register_shellcontext(app):
    """Register shell context objects."""
    from .database import engine

    def shell_context():
        """Shell context objects."""
        return {"db": engine}

    app.shell_context_processor(shell_context)



def configure_logger(app):
    """Configure loggers."""
    handler = logging.StreamHandler(sys.stdout)
    if not app.logger.handlers:
        app.logger.addHandler(handler)
