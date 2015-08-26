# Статистика доменов
Скрипт для сбора статистики для зон ru/su/rf. Собираются все записи c DNS, 
Автономная система, переод делегирования

Для работы необходимы модули:
- MySQLdb
- dnspython
- SubnetTree
- psuntil >= 2.2

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

* docker-compoce up -d



Далее каждую ночь база данных доменов будет обновляться. На двух процессорах E5-2697v3 процесс обновления БД занимает 4-5 часов.


# Пример отчета (1 августа 2015 года)

![example](https://scontent.xx.fbcdn.net/hphotos-xpt1/t31.0-8/11779902_855515371153091_8587193411725580989_o.png)


