in mysql console:
create user 'biomio_mysql_user'@'localhost' identified by password 'b10m10p@$$';
GRANT ALL PRIVILEGES ON * . * TO 'biomio_mysql_user'@'localhost';
FLUSH PRIVILEGES;

to create a database:
CREATE SCHEMA `biomio_storage` DEFAULT CHARACTER SET utf8 ;

use also:  gnome-keyring mysql-workbench

to test data stores run:
       *  worker.py
       * redis-rest.py
and make post request: http://localhost:8880/redis
      
