from mysql.connector import connect, Error

class sql_DB:

    def __init__(self):

        with open("config_sql", "r") as file:
            configs = file.readlines()
            file.close()
        with open(".my_sql_password", "r") as file:
            sqlpassword = file.read().strip()
            file.close()
        # print("building connection ")
        # print(str(configs[0]).strip() + str(configs[1]).strip() + sqlpassword)
        self.connection = connect(host=str(configs[0]).strip(), user=str(configs[1]).strip(), password=sqlpassword, database="pw_user_db")
        self.cursor = self.connection.cursor()

    def close_down(self):
        self.cursor.close()
        self.connection.close()
        pass


# print(check_admin("admin", "Lm(6QXlaYsk8"))#Works, returns True if admin details are correct
