# dls.v1

установить все зависимости с файла requirements.txt

установить на линукс RabbitMQ,	sudo apt-get install rabbitmq-server

создать миграции
```bash
    ./manage.py makemigrations
```
накатить миграции
```bash
    ./manage.py migrate
```


Запускаем сельдерей
```bash
    celery -A core worker --loglevel=INFO
```


Запускаем планировщик
```bash
    celery -A core beat -l INFO
```

