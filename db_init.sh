echo "DROP DATABASE IF EXISTS hbnb_dev_db;" | mysql;
cat setup_mysql_dev.sql | mysql;
echo "quit" | sh run_console.sh
