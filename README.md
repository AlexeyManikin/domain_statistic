# Статистика доменов
Скрипт для сбора статистики для зон ru/su/rf. Собираются все записи c DNS (A, AAAA, NS, MX, TXT), 
данные об автономной системе к который пренадлежит домен, переоду делегирования и так далее. На основе этих данных можно
строить статистику. 

* Сайт проекта       http://firststat.ru
* Статья с описанием https://habrahabr.ru/post/301894/

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
анимает 3-6 часов.



