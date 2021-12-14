from flask import Flask, render_template
from flask_wtf import FlaskForm
from wtforms import SubmitField, TextAreaField, SelectField

from wtforms.validators import ValidationError, DataRequired 
import re
from sqlalchemy import exc
NUMBER_CHAR_MASK = 10

app = Flask(__name__, template_folder='.')

app.config['SECRET_KEY']='A0Zr98j/3yX R~XHH!jmN]LWX/,?RTU'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///device.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# app.config['SQLALCHEMY_ECHO'] = True


from model import TypeDevice, Device, db


class CreateUserForm(FlaskForm):

    def __init__(self, *args, **kwargs):
        super(CreateUserForm, self).__init__(*args, **kwargs)
        self.serial_numbers_with_wrong_format = []


    serial_numbers = TextAreaField(
        'Серийные номера',
        render_kw = {"rows":10, "cols": "10"},
        validators = [DataRequired(), ],
        )
    type_device = SelectField(
        'Тип оборудования', 
        # render_kw = {'class':'form-control'}, 
        choices = [td.title for td in TypeDevice.query.all() ],
        ) 
    submit = SubmitField("Добавить")

    def validate_serial_numbers(self, validation_field):
        print(validation_field.data)
        list_errors = []
        list_rows = self.serial_numbers.data.split() #"\r\n"
        for row in list_rows:
            for serial_number in [row[i:i+NUMBER_CHAR_MASK] for i in range(0, len(row), NUMBER_CHAR_MASK)]:
                try:
                    processing_serial_number(self.type_device.data, serial_number)
                except exc.IntegrityError:
                    db.session.rollback()
                    # serial_numbers_save_db.append(serial_number)
                    list_errors.append(f"Номер {serial_number} есть в БД")
                except ValidationError:
                    list_errors.append(f"Номер {serial_number} не соответсвует формату {self.type_device.data}")
                    self.serial_numbers_with_wrong_format.append(serial_number)
        
        if (list_errors):  raise ValidationError(list_errors)



def processing_serial_number(type_device_str,  serial_number):

    type_device = TypeDevice.query.filter_by(title = type_device_str).first_or_404()
    result = re.match(type_device.serial_number_mask, serial_number)
    
    if not result: 
        raise ValidationError(f"{serial_number} не соответсвует шаблону" )
    
    Device(type_device=type_device, serial_number=serial_number).save()



@app.route('/', methods=('GET', 'POST'))
def index():
    form = CreateUserForm()
    message='Заполните форму'
    if form.validate_on_submit():
        message = 'Все серийные номера добавлены в БД'
    form.serial_numbers.data = '\n'.join(form.serial_numbers_with_wrong_format)
    
    return render_template('index.html', form=form, message=message)
