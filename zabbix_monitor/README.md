Для настройки Zabbix и мониторинга ресурсов сервера, доступности сервера и веб-чеков, а также для организации уведомлений в Телеграм и Slack, вам потребуется выполнить несколько шагов. Вот пример скрипта для настройки:

1. Установка Zabbix на вашу VPS (виртуальный сервер):
```shell
# Обновление системы
sudo apt update
sudo apt upgrade

# Установка необходимых пакетов
sudo apt install -y apache2 mysql-server php php-mysql php-ldap php-bcmath php-mbstring php-gd php-curl php-xml libapache2-mod-php snmp fping

# Установка сервера Zabbix
wget https://repo.zabbix.com/zabbix/5.4/ubuntu/pool/main/z/zabbix-release/zabbix-release_5.4-1%2Bfocal_all.deb
sudo dpkg -i zabbix-release_5.4-1+focal_all.deb
sudo apt update
sudo apt install -y zabbix-server-mysql zabbix-frontend-php zabbix-apache-conf zabbix-agent

# Создание базы данных для Zabbix
sudo mysql -u root -p
CREATE DATABASE zabbix CHARACTER SET utf8 COLLATE utf8_bin;
CREATE USER 'zabbix'@'localhost' IDENTIFIED WITH mysql_native_password BY 'password';
GRANT ALL PRIVILEGES ON zabbix.* TO 'zabbix'@'localhost';
FLUSH PRIVILEGES;
QUIT

# Импорт схемы базы данных
sudo zcat /usr/share/doc/zabbix-server-mysql*/create.sql.gz | sudo mysql -u zabbix -p zabbix

# Настройка файла конфигурации сервера Zabbix
sudo nano /etc/zabbix/zabbix_server.conf
# Раскомментируйте и измените параметр DBPassword, установив пароль, указанный ранее

# Настройка PHP для Zabbix
sudo nano /etc/zabbix/apache.conf
# Раскомментируйте и измените параметр php_value date.timezone на вашу временную зону

# Перезапуск сервисов Apache и Zabbix
sudo systemctl restart apache2
sudo systemctl enable zabbix-server zabbix-agent
sudo systemctl start zabbix-server zabbix-agent

# Настройка фронтенда Zabbix на веб-сервере
sudo nano /etc/apache2/conf-available/zabbix.conf
# Установите ServerName на IP-адрес вашей VPS (например, ServerName 192.168.0.100)

# Активация настроек и перезапуск Apache
sudo a2enconf zabbix.conf
sudo systemctl restart apache2
```

2. Настройка мониторинга сервера в Zabbix:
- Откройте веб-интерфейс Zabbix в браузере, перейдите по адресу `http://<IP-адрес-вашей-VPS>/zabbix`.
- Перейдите в раздел "Configuration" и настройте хост для мониторинга вашего сервера.
- Настройте элементы данных (items) для мониторинга нагрузки на сервер, использования жесткого диска и доступности сервера.
- Создайте триггеры для оповещения при превышении определенных значений.
- Проверьте работу мониторинга настроенных параметров.

3. Настройка веб-чеков в Zabbix:
- Перейдите в раздел "Configuration" и настройте новую группу или хост для веб-чеков.
- Создайте элементы данных (items) с использованием типа "Web" для мониторинга доступности доменов.
- Настройте триггеры для оповещения при недоступности доменов.
- Проверьте работу веб-чеков и оповещений.

4. Настройка уведомлений в Телеграм и Slack:
- Создайте бота в Телеграм и получите токен бота.
- Добавьте бота в группу или получите ID чата для отправки уведомлений.
- В настройках Zabbix, раздел "Administration" -> "Media Types", создайте новый тип медиа-канала "Telegram" или "Slack", указав необходимые настройки для каждого канала.
- Настройте действия (actions) в разделе "Configuration" -> "Actions", чтобы отправлять уведомления в выбранные медиа-каналы при возникновении проблем.

Надеюсь, этот пример скрипта поможет вам настроить Zabbix для мониторинга, веб-чеков и уведомлений. Если у вас возникнут вопросы или потребуется дополнительная помощь, буду рад помочь! 😊🚀

