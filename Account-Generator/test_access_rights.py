import pytest
import unittest
import configparser
import string
import random

from user_account_details import UserAccountDetails

# UserAccountDetails().create_new_user("TestUser", "test_first", "test_last", "1990", "This1$A3trongPass")

class TestAccessRights(unittest.TestCase):

    checker = UserAccountDetails()

    def test_change_to_manger(self):
        #change user name
        #check admin
        UserAccountDetails().create_new_user("TestUser", "test_first", "test_last", "1990", "This1$A3trong")
        self.assertTrue(self.checker.check_admin("admin","admin")) # Fun Checkadmin takes user,pass from input User login Test admin account
        self.assertEqual(self.checker.change_to_manager("TestUser"),"The account has been changed to admin status.") # changing the TestUser account into a admin should return 1 row edited

    def test_change_to_user(self):
        self.assertTrue(self.checker.check_admin("admin","admin")) # Fun Checkadmin takes user,pass from input User login Test admin account
        self.assertEqual(self.checker.change_to_user("TestUser"),"The account has been changed to user")
        self.assertEqual(self.checker.change_username("TestUser", "admin"),"The new user already exists in the database")
        self.assertEqual(self.checker.change_username("TestUser", "NewAdmin"), "{} has been changed to {}".format("TestUser", "NewAdmin"))#takes the Username and chnages it to the new username
        self.checker.delete_user("NewAdmin")
        self.checker.delete_user("TestUser")
