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

    def check_input_char(self, search_term):
        sql_input_check = self.read_sql_characters()
        disallowed_characters= list(sql_input_check[0])

        if self.read_sql_characters(user_firstname, user_lastname, user_birthyear, user_password):
            return False
        else:
            return True




# print(check_admin("admin", "Lm(6QXlaYsk8"))#Works, returns True if admin details are correct
