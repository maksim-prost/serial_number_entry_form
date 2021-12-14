from wtforms import SubmitField, TextAreaField, SelectField
from flask_wtf import FlaskForm
from wtforms.validators import ValidationError, DataRequired 
import re
# from sqlalchemy import exc
from model import TypeDevice, Device, db


class SerialNumberEntryForm(FlaskForm):

    def __init__(self, *args, **kwargs):
        super(SerialNumberEntryForm, self).__init__(*args, **kwargs)
        self.serial_numbers_with_wrong_format = []

    serial_numbers = TextAreaField(
        'Серийные номера',
        render_kw = {"rows":"10", "cols": "10"},
        validators = [DataRequired(), ],
        )
    type_device = SelectField(
        'Тип оборудования', 
        choices = [td.title for td in TypeDevice.query.all() ],
        ) 

    submit = SubmitField("Добавить")

    def validate_serial_numbers(self, validation_field):
        
        list_errors = []
        type_device = TypeDevice.query.filter_by( title=self.type_device.data ).first()
        
        for serial_number in validation_field.data.split():
            result = re.match(type_device.serial_number_mask, serial_number)
            if result:
                if Device.query.filter_by(serial_number=serial_number, type_device_id=type_device.id).first():
                    list_errors.append(f"Номер {serial_number} есть в БД")
                    continue
                Device(type_device_id=type_device.id, serial_number=serial_number).save()
                continue
            list_errors.append(f"Номер {serial_number} не соответсвует формату {self.type_device.data}")
            self.serial_numbers_with_wrong_format.append(serial_number)
        
        if list_errors:
            raise ValidationError(list_errors)


