in mysql console:
mysql -u root -p


create user 'biomio_user'@'localhost' identified by 'b10m10p@$$';
GRANT ALL PRIVILEGES ON * . * TO 'biomio_user'@'localhost';
FLUSH PRIVILEGES;

to create a database:
CREATE SCHEMA `biom_website` DEFAULT CHARACTER SET utf8 ;

use also:  gnome-keyring mysql-workbench

to test data stores run:
       *  worker.py
       * redis-rest.py
and make post request: http://localhost:8880/redis
      
