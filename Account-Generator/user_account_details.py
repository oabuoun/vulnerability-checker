from hashing.hashfunctions import HashFunctions
from sql_init import sql_DB
import json
from password_checks import UserPasswordDetails

class UserAccountDetails():
    # pw_user_db, user_info, username, FirstName, LastName, BirthYear, password, Manager
    # host=configs[0]52.214.153.42

    def user_login(self, username, password):
        hf_access = HashFunctions()
        print(password)
        print(username)
        if self.check_existence(username):
            #print("ok, you're real")
            if hf_access.check_pass(username, password):
                print("even your password is real")
                return True

            else:
                print("password is wrong")
                return False # Wrong password
        else:
            print("Username is wrong")
            return False # Wrong username



    def check_admin(self, user_name, user_password):  # check if the admin value is true

        command = "SELECT * FROM `user_info` WHERE `username`= '{}' AND `password`='{}' AND `Manager` = 1;".format(
            user_name,  HashFunctions().get_user_pass(user_name))
        db = sql_DB()
        cursor = db.cursor
        cursor.execute(command)
        #connection.commit()
        cursor.fetchall()
        num_occurences = cursor.rowcount
        print(num_occurences)
        # print("num_occurences assigned")
        db.close_down()
        # print(HashFunctions().get_user_pass(user_name))
        if num_occurences > 0:
            return True
        elif num_occurences == 0:
            return False

    def check_existence(self, user_name):  # checks if a user exists in a database
        # print("check_existence says hi to {}".format(user_name))
        db = sql_DB()
        # print("db established")
        cursor = db.cursor
        # print("cursor made")
        command = "SELECT `user_id` FROM `user_info` WHERE `username`= '{}';".format(user_name)
        # print(command)
        # print("command created")
        cursor.execute(command)
        # print("command executed")
        # connection.commit()
        cursor.fetchone()#["user_id"]
        # print("cursor fetched")
        num_occurences = cursor.rowcount
        # if num_occurences > 0:
        #     user_id = cursor.getColumnIndex("user_id")
        # print("num_occurences assigned")
        db.close_down()

        if num_occurences > 0:
            return True  # if it exists it will return True
        else:
            return None # if doesnt exists will return False

    def create_new_user(self, user_name, first_name, last_name, birth_year, password):  # creates user details
        # check_admin()
        # birth_year = int(birth_year)
        db = sql_DB()
        cursor = db.cursor
        # print(password)

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


    def change_to_manager(self, user_name):  # changes the value of user role back to manager role

        db = sql_DB()
        cursor = db.cursor
        if self.check_existence(user_name):
            command = "UPDATE `user_info` SET `Manager`= '1' WHERE `username` = '{}';".format(user_name)
            cursor.execute(command)
            db.connection.commit()
            db.close_down()
            return "The account has been changed to admin status."
        else:
            return "The user doesn't exist"


    def change_to_user(self, user_name):  # changes the value of manager role back to user role
        db = sql_DB()
        cursor = db.cursor

        if self.check_existence(user_name):
            command = "UPDATE `user_info` SET `Manager`= '0' WHERE `username` = '{}';".format(user_name)
            cursor.execute(command)
            db.connection.commit()
            db.close_down()
            return "The account has been changed to user"
        else:
            return "The user doesn't exist"



    def change_username(self, old_user_name, new_user_name):  # only if the user is an admin, allows to change the user name
        db = sql_DB()
        cursor = db.cursor
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



    def delete_user(self, user_name):  # deletes user details
        db = sql_DB()
        cursor = db.cursor
        #need to sanitise user_name input to prevent sql injection
        if self.check_existence(user_name):
            command = "DELETE FROM `user_info` WHERE `username`= '{}';".format(user_name)
            cursor.execute(command)
            db.connection.commit()
            db.close_down()
            return "The account {} has been deleted from the database".format(user_name)
        else:
            return "The user you are trying to delete isn't on the database"

    def fetch_userlist_page(self, page, pagesize):

        #start by opening sql database
        db = sql_DB()
        cursor = db.cursor
        print(page, pagesize)
        gather_command = "SELECT `user_id`, `username`, `FirstName`, `LastName` FROM `user_info` ORDER BY `username` LIMIT {} OFFSET {}".format(pagesize, (int(page) - 1)*pagesize)
        cursor.execute(gather_command)
        row_headers=[x[0] for x in cursor.description] #this will extract row headers
        page = cursor.fetchall()

        json_page = []

        #readable_page.insert(0,(row_headers[0],row_headers[1],row_headers[2]))
        #db.close_down()
        for result in page:
            json_page.append(dict(zip(row_headers,result)))
        print("HEADERS", row_headers)
        print(json_page)
        return json_page
# File Test

#print(UserAccountDetails().delete_user("TestUser97", "adin", "Lm(6QXlaYsk8")) #Works, Used a test DB to delete an entry
# print(UserAccountDetails().change_to_user("admin", "admin", "Lm(6QXlaYsk8")) #Works, returns the right strings depends on the input
# print(UserAccountDetails().create_new_user("test_username1", "test_first", "test_last", "1990", "h_sux9jY")) #Works, if accort already exists will infom user, if password is weak will generate new pass inserts to DB
# print(UserAccountDetails().check_admin("admin", "Lm(6QXlaYsk8"))#Works, returns True if admin details are correct
# print(UserAccountDetails().change_username("test_user", "New_user", "admin", "admin"))#Works, doesnt let the new username change if it's already in uses, only lets you change name if you have admin details
# print(UserAccountDetails().change_to_manager("admin", "admin", "Lm(6QXlaYsk8"))#Works, Only works if you have admin details and the username is in the database
# print(UserAccountDetails().check_existence("admin"))#Works, Check is a username is in teh database
# print(UserAccountDetails().user_login("test_user", "i4dzJzj~"))
