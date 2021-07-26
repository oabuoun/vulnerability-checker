import hashlib
import bcrypt
import base64
import configparser
from hashing.salting import Salting

class HashSelection():

    def print_hash_options(self):

        return hashlib.algorithms_available


    def read_password_hash_policy(self):
        policy = configparser.ConfigParser()
        policy.read('hash_policy.txt')
        password_hash = policy.get('Policy', 'password_hash').lower()
        print(password_hash)
        return password_hash

    def read_file_hash_policy(self):
        policy = configparser.ConfigParser()
        policy.read('hash_policy.txt')
        password_hash = policy.get('Policy', 'file_hash').lower()

        return password_hash

    def sha1_hash(self, plaintext, salt):
        # HF = Salting()
        # salt = HF.generate_salt()
        # salt_64 = HF.generate_base64_salt(salt)
        saltedpass = salt + plaintext
        return(hashlib.sha1(saltedpass.encode()).hexdigest()), salt

    def sha256_hash(self, plaintext, salt):
        # HF = Salting()
        # salt = HF.generate_salt()
        # salt_64 = HF.generate_base64_salt(salt)
        #print("plaintext is: ", plaintext)
        #print("Salt in hasfunction is: " + salt)
        saltedpass = salt + plaintext
        #print("*****************************************************************" + saltedpass)
        return(hashlib.sha256(saltedpass.encode()).hexdigest()), salt

    def sha3_256_hash(self, plaintext, salt):
        # HF = Salting()
        # salt = HF.generate_salt()
        # salt_64 = HF.generate_base64_salt(salt)
        saltedpass = salt + plaintext
        return(hashlib.sha3_256(saltedpass.encode()).hexdigest()), salt

    def sha3_512_hash(self, plaintext, salt):
        # HF = Salting()
        # salt = HF.generate_salt()
        # salt_64 = HF.generate_base64_salt(salt)
        saltedpass = salt + plaintext
        return(hashlib.sha3_512(saltedpass.encode()).hexdigest()), salt

    def bcrypt_hash(self, plaintext):
        salt = bcrypt.gensalt()
        plainencode = plaintext.encode()
        # print(type(salt))
        # print(type(plainencode))
        return(bcrypt.hashpw(plainencode, salt).decode()), salt.decode()
        #return(hashlib.sha3_512(saltedpass.encode()).hexdigest()), salt_64

    def bcrypt_check(self, plaintext, salt):
        plainencode = plaintext.encode()
        salt = salt.encode()
        return(bcrypt.hashpw(plainencode, salt).decode()), salt.decode()

        # if bcrypt.checkpw(plaintext.encode(), hashed.encode()):
        #     print("It Matches!")
        # else:
        #     ("It Does not Match :(")
    # def hash_password(self, password):
    #     HF = Salt()
    #     salt = HF.generate_salt()
    #     salt_64 = HF.generate_base64_salt(salt)
    #     saltedpass = salt_64 + password
    #     hash_type = self.read_password_hash_policy()
    #     return(hashlib.hash_type(saltedpass.encode()).hexdigest()), salt_64
    #     pass
# get the choiceof hash from the hash_policy file and hashes the input with the correct hashing type
# print(HashSelection().print_hash_options())
# print(HashSelection().read_password_hash_policy())
# print(HashSelection().read_file_hash_policy())
# print(HashSelection().sha1_hash("greatpass"))
# print(HashSelection().sha512_256_hash("greatpass"))
# print(HashSelection().bcrypt_hash("greatpass"))
# print(HashSelection().bcrypt_check("i4dzJzj~", "$2b$12$MUrhtHRC8CMfG.ui4HeyeuD.EQEELqhIDmp9XsTm4ckvM4GxHOMsW"))
