import pytest
import unittest
import configparser
import string
import random

from user_account_details import UserAccountDetails


class PassTest(unittest.TestCase):

    checker = UserAccountDetails()

    def test_login(self):
        self.checker.create_new_user("test_user", "test_first", "test_last", "1990", "h_sux9jY")
        self.assertTrue(self.checker.user_login("test_user", "h_sux9jY"))
        self.checker.delete_user("test_user")
    def test_existence(self):
        self.assertTrue(self.checker.check_existence("admin"))
        self.checker.delete_user("test_user")




# craete_new_user may have some issues with permantly adding to database otherwise 100%
