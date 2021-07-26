# delete account I have created

import pytest
import unittest
import configparser
import string
import random

from user_account_details import UserAccountDetails


# use mock  package to run tests
class PassTest(unittest.TestCase):
    checker = UserAccountDetails()

    def test_delete_account(self):
        self.checker.create_new_user("test_user", "test_first", "test_last", "1990", "Th1$trong")
        self.assertEqual(self.checker.delete_user("test_user"),"The account {} has been deleted from the database".format("test_user"))
    #check if the database has been updated
    def test_check_deletion(self):
        self.assertFalse(self.checker.check_existence("test_user"))
    #check if the account no longer exists
    def test_extra_check_deletion(self):
        self.assertEqual(self.checker.delete_user("Random_user"), "The user you are trying to delete isn't on the database")
        self.checker.delete_user("test_user")
# 100% pass rate no issues
