from flask import render_template
from mkapp import app
from serial_number_entry_form import SerialNumberEntryForm


@app.route('/', methods=('GET', 'POST'))
def index():
    form = SerialNumberEntryForm()
    message = 'Заполните форму'
    if form.validate_on_submit():
        message = 'Все серийные номера добавлены в БД'

    form.serial_numbers.data = '\n'.join(form.serial_numbers_with_wrong_format)
    return render_template('index.html', form=form, message=message)
