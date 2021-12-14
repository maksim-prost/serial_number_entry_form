Перед запуском приложения:
  - установить зависимости
    pip install -r requirements.txt 
  
  - создать базу данных
    python create_db.py 
    
Запуск приложения 
    flask run
    
В поле ввода вводятся  серийные номера, 
которые разделяются "разделительными" символами, 
номера длинною более 10 символов считаются введеными неверно 
и разделяются по 10 символов

Если номер не соответсвует маски оборудования, то выводится
сообщение, что номер не соответсвует маски оборудования,
номер остается в поле ввода для исправления.

Если номер сохранен в бд, то выводится сообщения, что номер есть в бд,
номер из поле ввода удаляется.