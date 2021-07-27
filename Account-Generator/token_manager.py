from sql_init import sql_DB
import jwt

class TokenManager():

    def store_token(self, token, username, user_agent):
        db = sql_DB()
        cursor = db.cursor
        command = "INSERT INTO `token_table` (`username`,`user_agent`,`token`) VALUES('{}','{}','{}')".format(username, user_agent, token)
        print(command)
        cursor.execute(command)
        db.connection.commit()
        #should now have stored username, user_agent, and the token in the appropriate table.
        db.close_down()

        return ("Token stored in database")

    def check_token(self, token, username, user_agent):
        #craft search command
        token_data = jwt.decode(token, 'SECRET_KEY_123456798', 'HS256')
        command = "SELECT * FROM token_table WHERE `token` = '{}'".format(token)
        #open cursor & execute command
        db = sql_DB()
        cursor = db.cursor
        cursor.execute(command)
        #grab result
        result = cursor.fetchall()
        # print("username from db is " + result[0][1]+"+")
        # print("username from header is " + username+"+")
        # print("user-agent from db is " + result[0][2]+"+")
        # print("user_agent from header is " + user_agent+"+")
        print(result)

        db_user_agent = result[0][2]
        print("lengths are:")
        print("for db_user_agent: "+ str(len(db_user_agent)))
        print("for user_agent: "+ str(len(user_agent)))
        db_username = result[0][1]
        print("for db_username: "+ str(len(db_username)))
        print("for username: "+ str(len(username)))
        #Extract token and user value
        print(cursor.rowcount)
        if cursor.rowcount > 0:
            print("rowcount passed")
            if str(username) == str(db_username):
                print("username passed")
                if str(user_agent) == str(db_user_agent):
                    print("user_agent passed")

                    print("details match token in database")
                    db.close_down()
                    return True
        else:
            db.close_down()
            return False
        #rowcount mroe than one

        #username matches
