from mysql.connector import connect, Error
from password_checks import UserPasswordDetails
import hashlib
from hashfunctions import HashFunctions
from sql_init import sql_DB

class UserAccountDetails():
    # pw_user_db, user_info, username, FirstName, LastName, BirthYear, password, Manager
    # host=configs[0]52.214.153.42

    def user_login(self, username, password):
        print(password)
        print(username)
        if self.check_existence(username):
            print("ok, you're real")
            if HashFunctions().check_pass(username, password):
                print("even your password is real")
                return True # change it to return a JSON token

            else:
                print("password is wrong")
                return False # Wrong password
        else:
            print("password is wrong")
            return False # Wrong username



    def check_admin(self, user_name: str, user_password: str) -> bool:  # check if the admin value is true

        command = "SELECT * FROM `user_info` WHERE `username`= '{}' AND `password`='{}' AND `Manager` = 1;".format(
            user_name,  HashFunctions().get_user_pass(user_name))
        command = "SELECT * FROM `user_info` WHERE username = %(username)s AND password = %(password)s AND Manager = %(Manager)s, {`username`: user_name, `password`:user_password, `Manager`:1}"
        db = sql_DB()
        cursor = db.cursor
        cursor.execute(command)
        #connection.commit()
        cursor.fetchall()
        num_occurences = cursor.rowcount
        # print("num_occurences assigned")
        db.close_down()
        # print(HashFunctions().get_user_pass(user_name))
        if num_occurences > 0:
            return True
        elif num_occurences == 0:
            return False

    def check_existence(self, user_name: str) -> bool:  # checks if a user exists in a database
        print("check_existence says hi to {}".format(user_name))
        db = sql_DB()
        print("db established")
        cursor = db.cursor
        print("cursor made")
        #command = "SELECT * FROM `user_info` WHERE `username`= '{}';".format(user_name)
        command = "SELECT * FROM `user_info` WHERE `username` = %(username)s, {username: user_name}"
        print(command)
        print("command created")
        cursor.execute(command)
        print("command executed")
        # connection.commit()
        cursor.fetchall()
        print("cursor fetched")
        num_occurences = cursor.rowcount
        # print("num_occurences assigned")
        db.close_down()

        if num_occurences > 0:
            return True  # if it exists it will return True
        else:
            return False  # if doesnt exists will return False

    def create_new_user(self, user_name, first_name, last_name, birth_year, password):  # creates user details
        # check_admin()
        # birth_year = int(birth_year)
        db = sql_DB()
        cursor = db.cursor
        print(password)

        if self.check_existence(user_name):
            return "{} already exists.".format(user_name)

        elif not UserPasswordDetails().check_list(password) or not UserPasswordDetails().check_policy(password) or not UserPasswordDetails().check_user_details(first_name, last_name, birth_year,
                                                                          password):
            password = UserPasswordDetails().generate_password()

            return "Your password is weak. How about {}".format(password)

        else:
            list = HashFunctions().hashpass(password)
            #INSERT INTO `user_info`(`Key`, `username`, `FirstName`, `LastName`, `BirthYear`, `password`, `Manager`, `salt`) VALUES ('[value-1]','[value-2]','[value-3]','[value-4]','[value-5]','[value-6]','[value-7]','[value-8]')
            command = "INSERT INTO `user_info`(`username`, `FirstName`, `LastName`, `BirthYear`, `password`, `salt`) VALUES ('{}', '{}', '{}', '{}', '{}', '{}');".format(
                user_name, first_name, last_name, birth_year, list[0], list[1])
            cursor.execute(command)
            db.connection.commit()
            db.close_down()
            list = []
            return "You have been successfully added to the database system."

    def change_to_manager(self, user_name, manager_name, manager_password):  # changes the value of user role back to manager role
        db = sql_DB()
        cursor = db.cursor

        if self.check_admin(manager_name, manager_password):
            if self.check_existence(user_name):
                command = "UPDATE `user_info` SET `Manager`= '1' WHERE `username` = '{}';".format(user_name)
                cursors.execute(command)
                db.connection.commit()
                db.close_down()
                return "The account has been changed to admin status."
            else:
                return "The user doesn't exist"
        else:
            return "You require an admin level account to change from user to admin status."

    def change_to_user(self, user_name, manager_name, manager_password):  # changes the value of manager role back to user role
        db = sql_DB()
        cursor = db.cursor
        sql_safe = db.check_input_char(user_name)
        if sql_safe:
            if self.check_existence(user_name):
                command = "UPDATE `user_info` SET `Manager`=NULL WHERE `username` = '{}';".format(user_name)
                cursor.execute(command)
                db.connection.commit()
                db.close_down()
                return "The account has been changed to user"
            else:
                return "The user doesn't exist"
        else:
            return "Potential SQL Injection - Query not carried out"

    def change_username(self, old_user_name, new_user_name, manager_name,
                        manager_password):  # only if the user is an admin, allows to change the user name
        db = sql_DB()
        cursor = db.cursor
        if self.check_admin(manager_name, manager_password):
            if self.check_existence(old_user_name):
                if not self.check_existence(new_user_name):
                    command = "UPDATE `user_info` SET `username` = '{}' WHERE `username` = '{}';".format(
                        new_user_name, old_user_name)
                    cursor.execute(command)
                    db.connection.commit()
                    db.close_down()
                    return "{} has been changed to {}".format(old_user_name, new_user_name)
                else:
                    return "The new user already exists in the database"
            else:
                return "The user doesn't exist"
        else:
            return "You require an admin level account to update a username."


    def delete_user(self, usernameArg : str, manager_name, manager_password) > bool:  # deletes user details
        db = sql_DB()
        cursor = db.cursor
        if self.check_admin(manager_name, manager_password):
            if self.check_existence(user_name):
                # command = "DELETE FROM `user_info` WHERE `username`= '{}';".format(user_name)
                command = "DELETE FROM `user_info` WHERE username = %(usernameVar)s, ('usernameVar': usernameArg)
                cursor.execute(command)
                db.connection.commit()
                db.close_down()
                return "The account {} has been deleted from the database".format(user_name)
            else:
                return "The user you are trying to delete isn't on the database"
        else:
            return "You require an admin level account to delete user details."

# File Test

#print(UserAccountDetails().delete_user("TestUser97", "adin", "Lm(6QXlaYsk8")) #Works, Used a test DB to delete an entry
# print(UserAccountDetails().change_to_user("admin", "admin", "Lm(6QXlaYsk8")) #Works, returns the right strings depends on the input
# print(UserAccountDetails().create_new_user("TestUser97", "test_first", "test_last", "1990", "SPKNEZGM+hC9kS")) #Works, if accort already exists will infom user, if password is weak will generate new pass inserts to DB
# print(UserAccountDetails().check_admin("admin", "Lm(6QXlaYsk8"))#Works, returns True if admin details are correct
# print(UserAccountDetails().change_username("test_user", "New_user", "admin", "admin"))#Works, doesnt let the new username change if it's already in uses, only lets you change name if you have admin details
# print(UserAccountDetails().change_to_manager("admin", "admin", "Lm(6QXlaYsk8"))#Works, Only works if you have admin details and the username is in the database
# print(UserAccountDetails().check_existence("admin"))#Works, Check is a username is in teh database
# print(UserAccountDetails().user_login("TestUser","SPKNEZGM+hC9kS"))
