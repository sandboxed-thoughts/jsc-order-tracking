import time

from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from django.contrib.staticfiles.testing import StaticLiveServerTestCase

from selenium import webdriver

from ..models import CustomUser as User


class TestWebsiteLogin(StaticLiveServerTestCase):
    driver = None
    port = 8888

    @classmethod
    def setUpClass(cls) -> None:
        driver_path = "C:/Users/Nate/AppData/Local/Microsoft/WindowsApps/geckodriver.exe"
        ContentType.objects.clear_cache()
        super().setUpClass()
        cls.driver = webdriver.Firefox(executable_path=driver_path)

    @classmethod
    def tearDownClass(cls) -> None:
        cls.driver.quit()
        super().tearDownClass()

    def setUp(self):
        self.user_password = "password"
        self.user = User.objects.create_user(
            email="test@dev.local", password=self.user_password, first_name="Test", last_name="User"
        )
        self.user.save()

    def test_login(self):
        driver = self.driver
        url = self.live_server_url + "/"
        driver.get(url)

        # input user email
        username_elm = driver.find_element_by_name("username")
        username_elm.clear()
        username_elm.send_keys(self.user.email)
        time.sleep(2)

        # input user password
        password_elm = driver.find_element_by_name("password")
        password_elm.clear()
        password_elm.send_keys(self.user_password)
        time.sleep(2)

        # submit the login info
        driver.find_element_by_tag_name("button").click()
        time.sleep(2)

        # if successful, redirected to landing page
        self.assertEqual(driver.current_url, url, msg="didn't work")
