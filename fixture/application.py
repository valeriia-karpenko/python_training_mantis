from selenium import webdriver

from fixture.james import JamesHelper
from fixture.mail import MailHelper
from fixture.project import ProjectHelper
from fixture.session import SessionHelper
from fixture.signup import SignupHelper
from fixture.soap import SoapHelper


class Application:

    def __init__(self, browser, config):
        if browser == "firefox":
            self.wd = webdriver.Firefox()
        elif browser == "chrome":
            self.wd = webdriver.Chrome()
        elif browser == "ie":
            self.wd = webdriver.Ie()
        else:
            raise ValueError("Unrecornized browser %s" % browser)
        self.session = SessionHelper(self)
        self.project = ProjectHelper(self)
        self.james = JamesHelper(self)
        self.signup = SignupHelper(self)
        self.mail = MailHelper(self)
        self.soap = SoapHelper(self)
        self.config = config
        self.base_url = config['web']['baseUrl']

    def is_valid(self):
        try:
            self.wd.current_url
            return True
        except:
            return False

    def open_home_page(self):
        wd = self.wd
        wd.get(self.base_url)
        # if not (wd.current_url.endswith("/index.php") and len(wd.find_elements_by_name("Number of results:")) > 0):
        #     wd.get("http://localhost/addressbook/index.php")

    def destroy(self):
        self.wd.quit()
