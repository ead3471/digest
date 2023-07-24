# Тестовое задание: Разработка микросервиса для подготовки дайджестов контента

## Цель

Разработайте микросервис, который будет формировать дайджесты контента для пользователей на основе их подписок. Дайджест представляет собой выборку постов из различных источников, на которые подписан пользователь. Вы можете выбрать любую технологию и форматы обмена данными.

## Деплой проекта

Протестировать развернутый проект можно [по этой ссылке](http://193.233.23.68:8080/docs)
#### 1. Клонировать проект на локальный компьютер или удаленный сервер:

    git clone git@github.com:ead3471/digest.git

#### 2. Установить Docker и docker-compose если необходимо
#### 3. Изменить (при необходимости) файл .env в корне проекта:

    cd digest
    nano .env

#### 4. Запустить проект:

    docker-compose up

#### 5. Выполнить создание таблиц баз данных:

    docker-compose exec api sh
    alembic upgrade head

#### 6. Описание API станет доступно по адресу:

    http://127.0.0.1:8080/docs

## Требования к микросервису

1. Получение запроса на формирование дайджеста: Микросервис должен уметь принимать запросы от основного приложения на формирование дайджеста для пользователя, идентифицируемого по уникальному ID.

2. Определение подписок пользователя: После получения запроса, микросервис должен определить источники, на которые подписан пользователь, используя информацию о подписках пользователя.

3. Сбор постов из подписок: Зная подписки пользователя, микросервис должен собирать посты из этих источников. Подумайте о нём как о "сканере" подписок пользователя в поисках нового контента.

4. Фильтрация постов: Из собранных постов отфильтруйте те, которые не соответствуют интересам пользователя или недостаточно популярны. Микросервис должен использовать определенные критерии для фильтрации.

5. Создание дайджеста: После фильтрации, оставшиеся посты упаковываются в дайджест. Дайджест - это совокупность постов, отобранных для пользователя.

6. Отправка дайджеста: Сформированный дайджест возвращается в главное приложение, которое предоставит его пользователю.

## Структура данных

- Модель User: Хранит данные о пользователе, включая ID и имя.
- Модель Subscription: Содержит информацию о подписках пользователя, включая ID подписки, название источника и ID пользователя.
- Модель Post: Включает информацию о постах из подписок пользователя, включая ID поста, ID подписки, содержание поста и популярность.
- Модель Digest: Содержит информацию о сформированном дайджесте, включая ID дайджеста, список постов и ID пользователя.

## Дополнительные требования (по желанию)

- Использование Docker для создания контейнеризованного микросервиса.
- Использование SQLAlchemy для взаимодействия с базой данных.
- Использование RabbitMQ для асинхронной обработки запросов на формирование дайджеста.
- Написание автоматических тестов для проверки функциональности микросервиса.

## Критерии оценки

- Работоспособность микросервиса.
- Качество кода (организованность, чистота, следование стандартам).
- Соответствие функциональным требованиям.
- Реализация дополнительных требований (если выбраны).


