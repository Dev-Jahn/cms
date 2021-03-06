from flask import Flask
from flask_cors import CORS
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager, get_jwt
from flaskconfig import *

from util.logger import logger

app = Flask(__name__)

try:
    app.config.from_object(configmap[app.config['ENV']]())
except KeyError:
    logger.error('Improper ENV name for config')
    exit()

# initialize db
with app.app_context():
    from model import db_base

    db_base.db.init_app(app)
    db_base.db.create_all()

# enable CORS
CORS(app, resources={r'*': {'origins': '*'}}, supports_credentials=True)

bcrypt = Bcrypt(app)
jwt = JWTManager(app)

# test entry for development
if app.env == 'development':
    from service.data.company_service import create_company
    from service.data.user_service import create_user, read_user
    from service.data.device_service import create_device

    with app.app_context():
        create_company({
            'name': 'illo',
            'subscription': True,
            'expiration_date': datetime.datetime.now() + datetime.timedelta(days=365)
        })
        create_user(
            userid='root',
            password='root',
            username='root',
            company='illo',
            is_admin=True
        )
        root_user = read_user(userid='root')[0]
        create_device(
            model='testmodel',
            serial='testserial',
            company='illo',
            owner='root',
            ip='123.123.123.123',
            is_deleted=False,
            created_by=root_user,
            edited_by=root_user,
        )

        if __name__ == '__main__':
            logger.info('Loaded ENV:' + str(list(os.environ)))
        with app.app_context():
            from router.cv_router import cv_route
        from router.task_callback_router import task_callback_route
        from router import api

        api.init_app(app)
        app.register_blueprint(task_callback_route, url_prefix='/task_callback')
        app.register_blueprint(cv_route, url_prefix='/cv')
        app.run(host='0.0.0.0',
                port=os.getenv('FLASK_RUN_PORT'),
                debug=os.getenv('FLASK_DEBUG'))
