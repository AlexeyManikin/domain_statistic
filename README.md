# Статистика доменов
Скрипт для сбора статистики для зон ru/su/rf. Собираются все записи c DNS, 
Автономная система, переод делегирования

Сайт проекта       http://firststat.ru

Статья с описанием https://habrahabr.ru/post/301894/

Для работы необходимы модули:
- mysqlclient==1.4.6
- dnspython==1.16.0
- prettytable==0.7.2
- pysubnettree==0.33
- psutil==5.7.0
- urllib3==1.25.8
- idna==2.9
- tqdm==4.45.0
- ipaddress==1.0.23

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

* https://habr.com/ru/post/66151/
* собирать статистику за сегодня из domain, а не из domain_history
* подключить RPKI
* скачивание и unzip сделать паралельно
* randomize_servers = on; ?? и в принуипе разобратся с рекурсером, можно ли его ускорить или все запросы так и пересылать в google
* pdnsd-ctl status

# Пример отчета (1 августа 2015 года)

![example](https://scontent.xx.fbcdn.net/hphotos-xpt1/t31.0-8/11779902_855515371153091_8587193411725580989_o.png)




