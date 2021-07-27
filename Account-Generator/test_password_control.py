import pytest
import unittest
import configparser
import string
import random

from password_checks import UserPasswordDetails


class PassTest(unittest.TestCase):

    checker = UserPasswordDetails()

    def test_policy(self):
        self.assertFalse(self.checker.check_policy("password"))
        self.assertTrue(self.checker.check_policy("s$Y9h70OXO)nXb7Y"))

    def test_list(self):
        self.assertFalse(self.checker.check_list("password"))
        self.assertTrue(self.checker.check_list("s$Y9h70OXO)nXb7Y"))

    def test_user_details(self):
        self.assertFalse(self.checker.check_user_details("Kai", "Wolff","1992","passwordKai"))
        self.assertFalse(self.checker.check_user_details("Kai", "Wolff", "1992","passwordWolff"))
        self.assertFalse(self.checker.check_user_details("Kai", "Wolff", "1992", "password1992"))
        self.assertTrue(self.checker.check_user_details("Kai", "Wolff", "1992", "s$Y9h70OXO)nXb7Y"))

    def test_read_policy(self):
        self.assertEqual(self.checker.read_password_policy(),[1, 1, 1, 1, 8, 16, '~!$^*()_-+='])
        self.assertEqual(self.checker.read_salt_policy(),[5,5,5])

        # Has to match the numbers that are in the password_policy.txt file

# Tests 100% pass locally pytest doesn't agree with check_policy
