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
процессорах E5-2620v3 с 32 гигабайтами памяти процесс обновления БД з
анимает 11-12 часов, плюс еще несколько часов агрегирование данных.

# Тестовый доступ к БД

* Сервер: manikin.beget.ru
* Порт: 3310
* Пользователь: amanikin_stat
* Пароль: openstatistic
* База: domain_statistic

Если кто не умеет пользоваться консолью, установил PhpMyAdmin: http://pma.amanikin.ru


# Пример отчета (1 августа 2015 года)

![example](https://scontent.xx.fbcdn.net/hphotos-xpt1/t31.0-8/11779902_855515371153091_8587193411725580989_o.png)




