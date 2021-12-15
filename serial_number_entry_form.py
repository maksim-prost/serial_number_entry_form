from flask_wtf import FlaskForm
from wtforms import SubmitField, TextAreaField, SelectField
from wtforms.validators import ValidationError, DataRequired 
import re
from model import TypeDevice, Device
import itertools

CONVERTING_MASK_TO_REGEX ={ "N":"\d",
                            "A":"[A-Z]",
                            "a":"[a-z]" ,
                            "X":"[A-Z\d]",
                            "Z":"[-_@]", 
                          }


class SerialNumberEntryForm(FlaskForm):

    def __init__(self, *args, **kwargs):
        super(SerialNumberEntryForm, self).__init__(*args, **kwargs)
        self.serial_numbers_with_wrong_format = []

    serial_numbers = TextAreaField(
        'Серийные номера',
        render_kw = {"rows":"10", "cols": "10"},
        validators = [DataRequired(),]
        )
    type_device = SelectField(
        'Тип оборудования', 
        choices = [td.title for td in TypeDevice.query.all() ]
        ) 
    submit = SubmitField("Добавить")

    def validate_serial_numbers(self, validation_field):
        
        list_errors = []
        type_device = TypeDevice.query.filter_by(title=self.type_device.data).first()
        
        pattern = re.compile("".join(["%s{%d}" % (CONVERTING_MASK_TO_REGEX[key], len(list(value))) 
                            for key, value in itertools.groupby(type_device.serial_number_mask)]))
        
        for serial_number in validation_field.data.split():
            result = pattern.match(serial_number)
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


