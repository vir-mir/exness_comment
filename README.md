[![Build Status](https://travis-ci.org/vir-mir/test_comment.svg?branch=master)](https://travis-ci.org/vir-mir/exness_comment)


## Основы основ

* **Окружение**

* * [Настройки](https://github.com/vir-mir/exness_comment/wiki/environment-settings)

* **Тестирование**

* * [Как работают тесты](https://github.com/vir-mir/exness_comment/wiki/testing)

* **Деплой**

* * [Распределенная БД](https://github.com/vir-mir/exness_comment/wiki/deployment#%D0%A0%D0%B0%D1%81%D0%BF%D1%80%D0%B5%D0%B4%D0%B5%D0%BB%D0%B5%D0%BD%D0%BD%D0%B0%D1%8F-%D0%91%D0%94)

* * [Не распределенная БД](https://github.com/vir-mir/exness_comment/wiki/deployment#%D0%9D%D0%B5-%D1%80%D0%B0%D1%81%D0%BF%D1%80%D0%B5%D0%B4%D0%B5%D0%BB%D0%B5%D0%BD%D0%BD%D0%B0%D1%8F-%D0%91%D0%94)

## API

* **Сущности (посты, блоги...)**

* * [Описание](Описание)

* * [Получение списка](Получение списка)

* * [Создание](Создание)

* **Комментарии**

* * [Описание](Описание)

* * [Создание](Создание)

* * [Получение списка](Получение списка)

* **Комментарий**

* * [Удаление](Удаление) 

* * [Редактирование](Редактирование)

* **История комментария**

* * [Список редактирование/удаление/создание комментария](Список редактирование/удаление/создание комментария) 

* **Коментарии пользователя**

* * [Получение списка комментарий пользователя](Получение списка комментарий пользователя)

* * [Экспорт комментарий пользователя (json, xml)](Экспорт комментарий пользователя (json, xml))

* * [Получение списка/истории экспорта комментарий ](Получение списка/истории экспорта комментарий )

* **Подписка на уведомление комментарий для сущности**

* * [Описание](Описание)

* * [Подписка](Подписка)

* * [Отписка](Отписка) 

```javascript
var protocol_one = document.location.protocol == 'http:' ? 'ws' : 'wss',
    port = document.location.port,
    url_one = protocol_one + "://" + document.location.hostname + (port ? ":" + port : "") + "/ws",
    socket = window['MozWebSocket'] ? new MozWebSocket(url_one) : new WebSocket(url_one);

socket.onopen = function() {this.send('open-{user_id}')};

socket.onmessage = function(e) {
    console.log(e.data);
};
```
