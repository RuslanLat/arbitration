# [Цифровой прорыв 2024, Сочи](https://hacks-ai.ru/events/1077372) 


## Кейс №3 "Семантическая классификация документов"


### Запуск сервиса

Для локального использования сервиса:
1. Загрузить все файлы репозитория **arbitration** \
    или выполнить команду в терминале bash ```git clone https://github.com/RuslanLat/arbitration```
2. В директории backend\app создать директорию mlmodel 
3. Скачать архив с обученной моделью и разархивировать ее в директорию mlmodel

***Примечание:*** структура файлов должна быть следующая

mlmodel:

        - `__init__.py`
        - `bert_inference.py`
        - `bert_model.py`
        - `best_f1_state.pth`
        - `config.yml`
        - `labels.json`
        - `Ru-bert-Pavlov-Gusev-fine-tuned.pt`
        - `train_nn.py`

4. Порядок запуска сервиса:
* в директории с проектом в терминале выполнить команду ```docker-compose up -d --build``` (сборка контейнеров и запуск их в работе в фоновом режиме)
* для остановки работы сервера в директории с проектом в терминале выполнить команду ```docker-compose stop```
* для повторного запуска в директории с проектом в терминале выполнить команду ```docker-compose start```

***Примечание:*** в директории с проектом (mirgovorit) создается папка ***pgdata*** с данными базы данных

3. Проверка в работе (после запуска контейнеров)
* web - сервис на локальном хосте port 5981 (http://127.0.0.1:5981/ или http://localhost:5981/)
* API доступно на локальном хосте port 8080 (http://127.0.0.1:8080/ или http://localhost:8080/)



## Команда "ЛИФТ"

Юрий Дон <img src="images/telegram_logo.png" width="30"> @Yuriy_Nikitich \
Руслан Латипов <img src="images/telegram_logo.png" width="30"> @rus_lat116 \
Алексей Верт-Миллер <img src="images/telegram_logo.png" width="30"> @alexwert3