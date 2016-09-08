[![Build Status](https://travis-ci.org/vir-mir/exness_comment.svg?branch=master)](https://travis-ci.org/vir-mir/exness_comment)

```bash
$ docker create -v /var/lib/postgresql/data --name postgres-data busybox
$ docker run --name pg -e POSTGRES_PASSWORD=qweqweqwe -e POSTGRES_DB=comments \
-d --volumes-from postgres-data --restart=always postgres:latest

$ docker pull virmir49/exness_comment:latest
$ docker run -d --name exness_comment -p 0.0.0.0:80:8888 -e DB_NAME=comments -e DB_PWD=qweqweqwe \
-e DB_USER=postgres -e DB_HOST=postgres --restart=always --link pg:postgres virmir49/exness_comment:latest
```

```bash
$ docker pull virmir49/exness_comment:latest
$ docker run -d --name exness_comment -p 0.0.0.0:80:8888 -e DB_NAME=comments -e DB_PWD=qweqweqwe \
-e DB_USER=postgres -e DB_HOST=postgres --restart=always --add-host=postgres:{ip_address_pg_pool} virmir49/exness_comment:latest
```

```bash
$ ip a | grep docker0
3: docker0: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc noqueue state UP group default 
    inet 172.17.0.1/16 scope global docker0
109: vethc52d11b@if108: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc noqueue master docker0 state UP group default 
131: vethac28c3e@if130: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc noqueue master docker0 state UP group default 
```

**pg_hba.conf**

`host	all		all		172.17.0.0/16		md5`

**postgresql.conf**

`listen_addresses = '*'`

`ufw allow from 172.17.0.0/16 to any port 5432`


## Основы основ

* **Окружение**

* * [Настройки](Настройки)

* **Тестирование**

* * [Как работают тесты](Как работают тесты)

* **Деплой**

* * [Распределенная БД](Распределенная БД)

* * [Не распределенная БД](Не распределенная БД)

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
