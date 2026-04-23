from flask import Flask
from flask_login import LoginManager
from flask_migrate import Migrate
from app.models import db, User
from app.config import Config

login_manager = LoginManager()
migrate = Migrate()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    
    # Init extensions
    db.init_app(app)
    login_manager.init_app(app)
    migrate.init_app(app, db)
    
    login_manager.login_view = 'auth.login'
    login_manager.login_message = 'Silakan login terlebih dahulu.'
    login_manager.login_message_category = 'warning'
    
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))
    
    # Register blueprints
    from app.routes.auth      import auth_bp
    from app.routes.surat     import surat_bp
    from app.routes.pengaduan import pengaduan_bp
    from app.routes.admin     import admin_bp
    from app.routes.main      import main_bp
    
    app.register_blueprint(main_bp)
    app.register_blueprint(auth_bp,      url_prefix='/auth')
    app.register_blueprint(surat_bp,     url_prefix='/surat')
    app.register_blueprint(pengaduan_bp, url_prefix='/pengaduan')
    app.register_blueprint(admin_bp,     url_prefix='/admin')
    
    return app