# domain_statistic
Статистика доменов ru/su/rf, с историей изменения A,MX,TXT,NS,CNAME записей, а так же 
миграции доменов между разными автономными системами. 

Для работы необходим docker (либо можно установить все библиотеки в ручную)
mysql - необходимо создать пользователя и загрузит дамп

Установка
- создаем базу 
  create database DBNAME;
- создаем пользователя
  GRANT ALL PRIVILEGES ON DBNAME.* TO DBUSER@'ip с которого будет подключение' IDENTIFIED BY 'DBPASS';
  FLUSH PRIVILEGES:
- собираем образ
  cd docker/docker-build/runner
  docker build -t domain_statistic . 
