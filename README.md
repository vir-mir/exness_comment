## Основы основ

* **Окружение**

* * [Настройки](Настройки)

* **Тестирование**

* * [Как работают тесты](Как работают тесты)

* **Деплой**

* * [Распределенная БД](Распределенная БД)

* * [Не распределенная БД](Не распределенная БД)

## API

**Сущности (посты, блоги...)**

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
