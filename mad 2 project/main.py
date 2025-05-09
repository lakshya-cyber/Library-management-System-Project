from flask import Flask
from application.model import db,User,Role
from flask_security import SQLAlchemyUserDatastore,Security
from Config import DevelopmentConfig
from application.resources import api
from application.sec import datastore
from application.worker import celery_init_app
import bcrypt
import flask_excel as excel
from celery.schedules import crontab
from application.tasks import daily_reminder, Monthly_reminder
from application.instances import cache


print(bcrypt.__version__)


def create_app():
    app = Flask(__name__)
    app.config.from_object(DevelopmentConfig)
    db.init_app(app)
    api.init_app(app)
    excel.init_excel(app)
    app.sequrity = Security(app,datastore)
    cache.init_app(app)
    with app.app_context():
        import application.view



    return app


app= create_app()
celery_app = celery_init_app(app)

@celery_app.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    sender.add_periodic_task(
        crontab(0, 0, day_of_month=1),
         Monthly_reminder.s()
    )

    sender.add_periodic_task(
       crontab(minute=0, hour=0),
         daily_reminder.s()
    )

if __name__ == '__main__':
    app.run(debug=True)

