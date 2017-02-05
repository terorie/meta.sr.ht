from flask import Flask, render_template, request, g, Response, redirect, url_for
from flask_login import LoginManager, current_user
from jinja2 import FileSystemLoader, ChoiceLoader

import random
import sys
import os
import locale

from srht.config import cfg, cfgi
from srht.database import DbSession
db = DbSession(cfg("sr.ht", "connection-string"))
from meta.types import User
db.init()

from meta.common import loginrequired
from meta.validation import Validation
from meta.flask import MetaFlask

app = MetaFlask(__name__)
app.secret_key = cfg("server", "secret-key")
app.jinja_env.cache = None
login_manager = LoginManager()
login_manager.init_app(app)

app.jinja_loader = ChoiceLoader([
    FileSystemLoader("overrides"),
    FileSystemLoader("templates"),
])

@login_manager.user_loader
def load_user(username):
    return User.query.filter(User.username == username).first()

login_manager.anonymous_user = lambda: None

try:
    locale.setlocale(locale.LC_ALL, 'en_US')
except:
    pass

from meta.blueprints.auth import auth
from meta.blueprints.profile import profile
from meta.blueprints.security import security
from meta.blueprints.keys import keys
from meta.blueprints.privacy import privacy
from meta.blueprints.oauth import oauth
from meta.blueprints.billing import billing
from meta.blueprints.api import api

app.register_blueprint(auth)
app.register_blueprint(profile)
app.register_blueprint(security)
app.register_blueprint(keys)
app.register_blueprint(privacy)
app.register_blueprint(oauth)
app.register_blueprint(billing)
app.register_blueprint(api)

if not app.debug:
    @app.errorhandler(500)
    def handle_500(e):
        # shit
        try:
            db.session.rollback()
            db.session.close()
        except:
            # shit shit
            sys.exit(1)
        return render_template("internal_error.html"), 500
    # Error handler
    if cfg("mail", "error-to") != "":
        import logging
        from logging.handlers import SMTPHandler
        mail_handler = SMTPHandler((cfg("mail", "smtp-host"), cfg("mail", "smtp-port")),
           cfg("mail", "error-from"),
           [cfg("mail", "error-to")],
           'sr.ht application exception occured',
           credentials=(cfg("mail", "smtp-user"), cfg("mail", "smtp-password")))
        mail_handler.setLevel(logging.ERROR)
        app.logger.addHandler(mail_handler)

@app.errorhandler(404)
def handle_404(e):
    if request.path.startswith("/api"):
        return { "errors": [ { "reason": "404 not found" } ] }, 404
    return render_template("not_found.html"), 404

@app.context_processor
def inject():
    return {
        'root': cfg("server", "protocol") + "://" + cfg("server", "domain"),
        'domain': cfg("server", "domain"),
        'protocol': cfg("server", "protocol"),
        'len': len,
        'any': any,
        'request': request,
        'locale': locale,
        'url_for': url_for,
        'user': current_user,
        'owner': cfg("sr.ht", "owner-name"),
        'owner_email': cfg("sr.ht", "owner-email"),
        'cfg': cfg,
        'cfgi': cfgi,
        'valid': Validation(request),
        'datef': lambda d: d.strftime('%Y-%m-%d %H:%M:%S UTC') if d is not None else 'Never',
    }
