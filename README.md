# Статистика доменов
Скрипт для сбора статистики для зон ru/su/rf. Собираются все записи c DNS, 
Автономная система, переод делегирования

Сайт проекта       http://firststat.ru

Статья с описанием https://habrahabr.ru/post/301894/

Для работы необходимы модули:
- MySQLdb
- dnspython
- SubnetTree
- psutil >= 2.2

Самый простой вариант запуска через Docker.

# Пример запуска:

устанавливаем Docker и git

* sudo apt-get update 
* sudo apt-get install docker.io git

Скачиваем репозиторий

* cd /home
* git clone https://github.com/AlexeyManikin/domain_statistic.git

Собираем образы

* cd domain_statistic/docker
* docker-compose build

запускаем контейнеры

* docker-compose up -d

Далее каждую ночь база данных доменов будет обновляться. На двух 
процессорах E5-2690v2 с 225 гигабайтами памяти процесс обновления БД з
анимает 6-8 часов, плюс еще несколько часов агрегирование данных.

# TODO

https://habr.com/ru/post/66151/

# Пример отчета (1 августа 2015 года)

![example](https://raw.githubusercontent.com/AlexeyManikin/domain_statistic/master/doc/2015_01.png)




