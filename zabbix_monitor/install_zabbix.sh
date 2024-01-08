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
