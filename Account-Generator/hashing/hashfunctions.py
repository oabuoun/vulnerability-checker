import hashlib
import string
# from password_checks import UserPasswordDetails
import random
import base64
from sql_init import sql_DB
from hashing.hash_selection import HashSelection
from hashing.salting import Salting

class HashFunctions():

    def get_user_pass(self,username):
        try:
            db = sql_DB()
            cursor = db.cursor
            command = "SELECT `password` FROM `user_info` WHERE `username` = '{}';".format(username)
            cursor.execute(command)
            password = cursor.fetchone()
            db.connection.close()
            return password[0]
        except TypeError:
            return None

# Create new if statment that links to the policy and checks the hash type needed bcrypt will return true or false
# Figure out the best way to do the other hashing functions
    def check_pass(self, username, plain_password):
        # print(username)
        try:
            salt = self.get_user_salt(username)
            # print("User salt = " + salt)
            check_pass = self.hash_no_salt(plain_password, salt)
            # print("Check pass line 33")
            # print(check_pass)
            db = sql_DB()
            cursor = db.cursor
            command = "SELECT `password` FROM `user_info` WHERE `username` = '{}';".format(username)
            cursor.execute(command)
            hashed_pass = cursor.fetchone()
            db.connection.close()
            # print("Hashed pass line 40")
            # print(hashed_pass)
            #print("Compare check and hashed line 42")
            #print (check_pass[0])
            #print(hashed_pass[0])
            if check_pass[0] == hashed_pass[0]:
                return True
            else:
                return False
        except TypeError:
            # print("Returning error")
            return None
        # print(check_pass)
        # print(hashed_pass)
        # print(salt)



    def get_user_salt(self, username):
        try:
            db = sql_DB()
            cursor = db.cursor
            command = "SELECT `salt` FROM `user_info` WHERE `username` = '{}';".format(username)
            cursor.execute(command)
            salt = cursor.fetchone()
            db.connection.close()
            #print("salt is: " + salt[0])
            return salt[0]
        except TypeError:
            return None


    def hash_no_salt(self, password, salt):
        HS = HashSelection()
        policy = HS.read_password_hash_policy()
        #print("Policy is: " + policy)
        #print("salt is: " + salt)
        #print("Password is: " + password)
        if policy == "sha1":
            return HS.sha1_hash(password, salt)
        if policy == "sha_256":
            #print("this is being sent to sha256: "+ password + " "+ salt)
            return HS.sha256_hash(password, salt)
        if policy == "sha3_256":
            return HS.sha3_256_hash(password, salt)
        if policy == "bcrypt":
            return HS.bcrypt_check(password, salt)

        else:
            error_message="Incorrect hash policy. Check hash_policy.txt file. Using Sha256 as default "
            # print(error_message)
            #salt = Salting().generate_salt() - THERE IS NO NEED FOR THIS LINE AS YOU ALREADY HAVE THE SALT
            return HS.sha256_hash(password, salt)
    #try:
        # print(type(password))
        # print(type(salt))
        #saltedpass = salt + password
        #print(saltedpass)
        # return hashlib.sha256(saltedpass.encode()).hexdigest()
        # return HashSelection().bcrypt_check(password, salt)
    # except TypeError:
    #     return "74"

    def hashpass(self, password):
        # # encode it to bytes using UTF-8 encoding
        HS = HashSelection()
        HF = Salting()
        policy = HS.read_password_hash_policy()
        salt = HF.generate_salt()
        salt = HF.generate_base64_salt(salt)
        # print(policy)
        if policy == "sha1":
            return HS.sha1_hash(password, salt)
        if policy == "sha256":
            return HS.sha256_hash(password, salt)
        if policy == "sha3_256":
            return HS.sha3_256_hash(password, salt)
        if policy == "bcrypt":
            return HS.bcrypt_hash(password)

        else:
            error_message="Incorrect hash policy. Check hash_policy.txt file. Using Sha256 as default "
            # print(error_message)
            salt = HF.generate_salt()
            salt = HF.generate_base64_salt(salt)
            return HS.sha256_hash(password, salt)

        # salt = self.generate_salt()
        # salt_64 = self.generate_base64_salt(salt)
        # saltedpass = salt_64 + password
        # #print(self.hash_no_salt("7$!5I6c2-F1r7m1S", salt_64))
        # return (hashlib.sha256(saltedpass.encode()).hexdigest()), salt_64

    # def saltpass(self, password):
    #     salted_pass = self.generate_salt().encode() + password.encode()
    #     return salted_pass

    # def generate_salt(self):
    #
    #     # reading through the password policy and looping through to extract necessary values to check and generates the password
    #     policy_checklist = UserPasswordDetails().read_salt_policy()
    #     max_length = sum(policy_checklist)
    #
    #     # Generating the password using random and string modules
    #     salt = ""
    #     for character in range(max_length):
    #
    #         random_character = random.randint(1,4)
    #
    #         if random_character == 1:
    #             salt += random.choice(string.ascii_lowercase)
    #         elif random_character == 3:
    #             salt += random.choice(string.ascii_uppercase)
    #         else:
    #             salt += random.choice(string.digits)
    #
    #     return salt
    #
    # def generate_base64_salt(self, salt):
    #     salt_64 = base64.b64encode(salt.encode())
    #     salt_final = salt_64.decode()
    #     #print("This is the final salt" + salt_final)
    #     return salt_final

    # salted_pass = username.encode() + password.encode()
    # b_salt = base64.b64encode(salted_pass)
    # b_message = b_salt.decode('ascii')
    # print(b_message)

# print("Hased password = " + HashFunctions().hashpass(" GreatPass")[0]) # Will return the hashed_value
# print("Salt = " + HashFunctions().hashpass(" GreatPass")[1]) # Will return the salt
# print(HashFunctions().get_user_salt("User"))
# print(HashFunctions().check_pass("test_user", "i4dzJzj~"))
# print(HashFunctions().get_user_pass("admin"))
# print(HashFunctions().hash_no_salt("i4dzJzj~", "$2b$12$MUrhtHRC8CMfG.ui4HeyeuD.EQEELqhIDmp9XsTm4ckvM4GxHOMsW" ))
