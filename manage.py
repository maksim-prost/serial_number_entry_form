from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from mkapp import app, db
from model import TypeDevice


migrate = Migrate(app, db)
manager = Manager(app)
manager.add_command('db', MigrateCommand)

serial_number_mask_by_device_type = {
    "D-Link DIR-300": "NXXAAXZXaa",
    "TP-Link TL-WR74": "XXAAAAAXAA",
    "D-Link DIR-300 S": "NXXAAXZXXX",
    }


# Создать таблицу TypeDevice в БД, заполнить значениями
@manager.command
def db_create():
    db.create_all()
    for type_device in serial_number_mask_by_device_type:
        db.session.add(TypeDevice(title=type_device,
                       serial_number_mask=serial_number_mask_by_device_type[type_device]))

    db.session.commit()


if __name__ == '__main__':
    manager.run()
