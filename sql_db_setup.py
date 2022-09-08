import mysql.connector

mydb = mysql.connector.connect(host="localhost", user="root", passwd="hgfjffdhb", auth_plugin='mysql_native_password')

my_cursor = mydb.cursor()

my_cursor.execute("CREATE DATABASE db")