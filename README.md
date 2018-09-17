# Описание

Веб-приложение для отображения логов от соответсвующего микросервиса. Поддерживает фильтрацию по ряду параметрам и сортировку.

Используемый стек: ```python3.7```, ```aiohttp3.4```

# Установка

1. Создать и активировать виртуальную среду

    ```$ virtualenv -p python3.7 venv```
    
    ```$ source venv/bin/activate```

2. Установить зависимости

    ```$ pip install -r requirements.txt```

3. Задать настройки приложения

    В папке ```config``` находятся заготовки для разных режимов запуска. Для локального запуска необходимо создать файл dev.yaml и задать требуемые параметры (в качестве примера можно использовать ```dev.yaml.example```).
    Парамтреы микросервиса настраиваются в секции ```api```

# Запуск приложения
Приложение можно запускать в трех различных вариантов, а именно:

- С помощью встроенного сервера

    ```$ python run.py --config=<config_name> ```
    Параметр ```--config``` можно пропустить, в таком случае по-умолчанию будет использован файл ```config/dev.yaml```

- С помощью Gunicorn

    ```$ gunicorn 'app.main:wsgi("<config_name>")' -b 0.0.0.0:<port> -k aiohttp.GunicornWebWorker -w <workers>```,  где ```<config_name>``` - имя конфигурационного файла (**внимание**, в данном способе запуска указывать кофнигурационный файл обязательно, по-умолчанию значение не подставляется), ```<port>``` - TCP-порт, по которому будет доступно приложение, ```<workers>``` - количество "воркеров".

- C помощью Docker

    Необходимо собрать docker-образ
    ```docker build . -t <image_name>```, где ```<image_name>``` - желаемое имя docker-образа
    После чего запустить контейтнер
    ```docker run -d -p <port>:8080 -e CONFIG=<config_name> --name <container_name> <image_name>```, где ```<port>``` - желаемый TCP-порт, ```<config_name>``` - имя конфигурационного файла, обязательное значение , ```<container_name>``` - желаемое имя контейера, ```<image_name>``` - docker-образ, из которого будет запущен контейнер.
    Если микросервис логов также запущен в контенере, необходимо добавить к комманде к запуску "линковку" данного контейнера с контейнером микросервиса - ```--link <log_container_name>:<log_image_name>```,  где ```<log_container_name>``` - наименование существующего docker-контейнера с микросервисом.
    В случае развертывания микросервиса иным способом настройка связки "контенер-микросервис" ложится полностью на плечи читающего данный файл.


# Использование

##### Главная страница

Метод: ```GET```
URL:  ```/logs/```

To be continued...

