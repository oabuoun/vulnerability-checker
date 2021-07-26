import configparser
import random
import string
import base64

class Salting():

    def read_salt_policy(self):
        # reads in password policy, returns variables as a list. Written by KW
        # password_policy = open('password_policy.txt', 'r')
        policy = configparser.ConfigParser()
        policy.read('password_policy.txt')
        salt_lowercase = policy.getint('Policy', 'salt_lowercase')
        salt_uppercase = policy.getint('Policy', 'salt_uppercase')
        salt_numbers = policy.getint('Policy', 'salt_numbers')

        return [int(salt_lowercase), int(salt_uppercase), int(salt_numbers)]


    def generate_salt(self):

        # reading through the password policy and looping through to extract necessary values to check and generates the password
        policy_checklist = self.read_salt_policy()
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
        salt_final = salt_64.decode()
        #print("This is the final salt" + salt_final)
        return salt_final
