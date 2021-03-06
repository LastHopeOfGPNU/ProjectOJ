from django.test import TestCase
from .utils import pwCheck, pwGen
from .models import Users

class UserModelTest(TestCase):
    def setUp(self):
        self.password = "cFoqYj1KzV7nTlv0fGckWZ9y8XRmYzg0"
        # self.password = "cFoqYj1KzV7nTlv0fGckWZ9y8XRmYzg0"
        # self.user = Users(password=self.password)

    def test_password_check(self):
        """
        当输入正确密码时pwCheck返回True
        否则返回False
        :return:
        """
        true_pwd = "a28721054"
        false_pwd = "123546"
        saved_pwd = self.password
        self.assertEqual(pwCheck(true_pwd, saved_pwd), True)
        self.assertEqual(pwCheck(false_pwd, saved_pwd), False)

    def test_pwGen_can_gen_pwd_and_check_it(self):
        """
        pwGen生成的hash能在pwCheck中检验
        :return:
        """
        true_pwd = "a28721054"
        false_pwd = "123546"
        hash = pwGen(true_pwd)
        self.assertEqual(pwCheck(true_pwd, hash), True)
        self.assertEqual(pwCheck(false_pwd, hash), False)