File server
=====

## Engish
Course work in BMSTU

Users have got catalogues, where they download files.
For each file a passport is created, which is stored in a storage.
The passport contains a title, description, file attributes and a set of additional attributes.
The subsystems of administrator and user are developed.

#### Prepare
```
sudo apt-get install wkhtmltopdf
mysql -u root -p < schema.sql
```

## Русский
Курсовая работа

Пользователи имеют каталоги, в которые загружают файлы.
Для каждого файла создаётся его паспорт, хранящийся в базе данных.
Паспорт содержит название, описание, атрибуты файла и набор дополнительных атрибутов.
Реализованы подсистемы администратора и пользователя.

#### Подготовка
```
sudo apt-get install wkhtmltopdf
mysql -u root -p < schema.sql
```
