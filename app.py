from flask import Flask, render_template
from flask_wtf import FlaskForm
from wtforms import SubmitField, TextAreaField, SelectField

from wtforms.validators import ValidationError, DataRequired 
import re


'''
    Тип оборудования    Маска SN
1   TP-Link TL-WR74     XXAAAAAXAA      11QAZWS2ER
2   D-Link DIR-300      NXXAAXZXaa
3   D-Link DIR-300 S    NXXAAXZXXX

Где 
N – цифра от 0 до 9,
A – прописная буква латинского алфавита,
a – строчная буква латинского алфавита,
X – прописная буква латинского алфавита либо цифра от 0 до 9,
Z –символ из списка: “-“, “_”, “@”.
'''


serial_number_mask_by_device_type = {
    "D-Link DIR-300": re.compile('\d[A-Z\d]{2}[A-Z]{2}[A-Z\d]{1}[-_@]{1}[A-Z\d]{1}[a-z]{2}'),
    "TP-Link TL-WR74": re.compile('[A-Z\d]{2}[A-Z]{5}[A-Z\d]{1}[A-Z]{2}'),
    "D-Link DIR-300 S": re.compile('\d[A-Z\d]{2}[A-Z]{2}[A-Z\d]{1}[-_@]{1}[A-Z\d]{3}'),
}
NUMBER_CHAR_MASK = 10
list_serial_number = []

DEFAULT_SERIAL_NUMBERS = []

class CreateUserForm(FlaskForm):

    serial_numbers = TextAreaField(
        'Серийные номера',
        render_kw={"rows": 10, "cols": 10, 'class':'form-control'},
        validators=[DataRequired(), ],
        # default = DEFAULT_SERIAL_NUMBERS
        )
    type_device = SelectField(
            'Тип оборудования', 
            render_kw={'class':'form-control'}, 
            choices= serial_number_mask_by_device_type.keys(),
        ) 

    submit = SubmitField(
            "Добавить",
        )

    def validate_serial_numbers(self, serial_numbers):
        # DEFAULT_SERIAL_NUMBERS = []
        self.does_not_match_mask = []
        self.contains_db = []
        list_rows = self.serial_numbers.data.split("\r\n")
        for row in list_rows:
            for serial_number in [row[i:i+NUMBER_CHAR_MASK] for i in range(0, len(row), NUMBER_CHAR_MASK)]:
                self.processing_serial_number(serial_number)
        if (self.does_not_match_mask or self.contains_db ):
            DEFAULT_SERIAL_NUMBERS.extend(self.does_not_match_mask)
            message_error_mask = self.does_not_match_mask and \
                                f"{' '.join(self.does_not_match_mask)} не соответсвуют шаблону" 
            message_error_db = self.contains_db and \
                                f"{' '.join(self.contains_db)} есть в БД"   
            raise ValidationError(f"{message_error_mask} {message_error_db}" )   

           

    def processing_serial_number(self, serial_number):
        result = serial_number_mask_by_device_type[self.type_device.data].match(serial_number)
        if result: 
            serial_number = result.group(0)
            if serial_number in list_serial_number:
                self.contains_db.append(serial_number)
                return
            list_serial_number.append(serial_number)
            return
        self.does_not_match_mask.append(serial_number)

app = Flask(__name__, template_folder='.')

app.config['SECRET_KEY']='A0Zr98j/3yX R~XHH!jmN]LWX/,?RTU'

@app.route('/', methods=('GET', 'POST'))
def index():
    global DEFAULT_SERIAL_NUMBERS
    DEFAULT_SERIAL_NUMBERS = []
    form = CreateUserForm()
    message='Заполните форму'
    if form.validate_on_submit():
        message = f'''Welcome {form.serial_numbers.data} {form.type_device.data}'''
    form.serial_numbers.data = '\n'.join(DEFAULT_SERIAL_NUMBERS)
    
    return render_template('index.html', form=form, message=message)

    