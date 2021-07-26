import hashlib
from password_checks import UserPasswordDetails

lass HashFunctions():

    def getusersalt(self, username):
        with connect(host=str(configs[0]), user=str(configs[1]), password=sqlpassword, database="pw_user_db") as connection:
            with connection.cursor() as cursor:
                command = "SELECT 'salt' FROM `user_info` WHERE `username`= '{}';".format(
                    user_name)

                cursor.execute(command)
                cursor.fetchall()


    def hashpass(self, password):
        # encode it to bytes using UTF-8 encoding
        salt = self.generate_salt()
        salt_64 = self.generate_base64_salt(salt)
        saltedpass = salt_64 + password
        return (hashlib.sha256(saltedpass.encode()).hexdigest()), salt_64

    # def saltpass(self, password):
    #     salted_pass = self.generate_salt().encode() + password.encode()
    #     return salted_pass

    def generate_salt(self):

        # reading through the password policy and looping through to extract necessary values to check and generates the password
        policy_checklist = UserPasswordDetails().read_salt_policy()
        max_length = sum(policy_checklist)

        # Generating the password using random and string modules
        salt = ""
        for character in range(max_length):

            random_character = random.randint(1,4)

            if random_character == 1:
                salt += random.choice(string.ascii_lowercase)
            elif random_character == 3:
                salt += random.choice(string.ascii_uppercase)
            else:
                salt += random.choice(string.digits)

        return salt

    def generate_base64_salt(self, salt):
        salt_64 = base64.b64encode(salt.encode())
        salt_final = salt_64.decode('ascii')
        return salt_final
hashpass("Tyree", "Thisisastrongpass")
    with connect(host=str(configs[0]), user=str(configs[1]), password=sqlpassword, database="pw_user_db") as connection:
    list = hashpass(password)
        with connection.cursor()as cursor:
            command = "INSERT INTO `user_info`(`username`, `FirstName`, `LastName`, `BirthYear`, `password`, `Manager`, 'salt') VALUES ('{}', '{}', '{}', '{}', '{}', 0, {});".format(user_name, first_name, last_name, birth_year, str(list[0]), str(list[1]))
            cursor.execute(command)
            connection.commit()
            cursor.close()
