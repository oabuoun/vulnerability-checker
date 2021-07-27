chmod -R a+rwx /data/mysql/
#gives permission for data/mysql. WHEN RESTARTING, THIS DOES NOT BELONG TO THE USER SO

export MYSQL_USER=root
export MYSQL_ROOT_PASSWORD=$(cat ../.my_sql_password)
#export user and password

docker-compose up -d
#start docker_compose

while [ "$(docker exec mysql_dbms mysqladmin --user=$MYSQL_USER --password=$MYSQL_ROOT_PASSWORD ping --silent)" != "mysqld is alive" ] ;
do
	echo "MYSQL Server is being initialised ...."
	sleep 1
done

echo "MYSQL Server is ready"

docker exec -it mysql_dbms service mysql restart || true

#docker exec -it mysql_dbms mysql --user=root --password=$MYSQL_ROOT_PASSWORD
#docker exec -it mysql_dbms mysql --user=root --password=$MYSQL_ROOT_PASSWORD < path-to-file.sql
