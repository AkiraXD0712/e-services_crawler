from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException
import time
import io
from log import logger


class Crawler:
    def __init__(self, name, passwd, executable_path):
        self.__name = name
        self.__passwd = passwd
        logger.info("Start driver")
        # self.driver = webdriver.PhantomJS(executable_path="C:\\Users\Akira.DESKTOP-HM7OVCC\Desktop\phantomjs.exe")
        self.driver = webdriver.PhantomJS(executable_path=executable_path)
        self.driver.set_window_size(1400, 1000)

    def connect(self):
        self.driver.implicitly_wait(10)
        logger.info("Navigating to e-services")
        self.driver.get(
            "https://cas.esigelec.fr/cas/login?service=http%3A%2F%2Fe-services.esigelec.fr%2Fj_spring_cas_security_check"
        )

        # Enter username
        logger.debug("Searching for 'username'")
        name = self.driver.find_element_by_name("username")
        logger.info("Entering username")
        name.send_keys(self.__name)

        # Enter passeword
        logger.debug("Searching for 'passeword'")
        password = self.driver.find_element_by_name("password")
        logger.info("Entering password")
        password.send_keys(self.__passwd, Keys.RETURN)

        logger.info("Login successfully")
        logger.debug("Click 'Scolarité'")
        try:
            WebDriverWait(self.driver, 40).until(
                EC.presence_of_element_located((By.LINK_TEXT, "Scolarité"))
            ).click()
        except NoSuchElementException:
            logger.error("'Scolarité' no found")
            self.driver.close()
        except TimeoutException:
            logger.error("Loading 40s time out")
            self.driver.close()

    def to_absence(self):
        logger.info("Navigating to 'Mes Absences'")
        logger.debug("Click ")
        try:
            WebDriverWait(self.driver, 40).until(
                EC.visibility_of_element_located((By.LINK_TEXT, "Mes Absences"))
            ).click()
        except NoSuchElementException:
            logger.error("'Mes Absences' no found")
            self.driver.close()
        except TimeoutException:
            logger.error("Loading 40s time out")
            self.driver.close()

        time.sleep(2)

        logger.debug("Click 'Mes Absences en 2016-2017'")
        try:
            WebDriverWait(self.driver, 40).until(
                EC.visibility_of_element_located((By.ID, "form:entree_10001683"))
            ).click()
        except NoSuchElementException:
            logger.error("'Mes Absences en 2016-2017' no found")
            self.driver.close()
        except TimeoutException:
            logger.error("Loading 40s time out")
            self.driver.close()

        logger.debug("Loading")
        try:
            WebDriverWait(self.driver, 40).until(
                EC.invisibility_of_element_located((By.ID, 'form:j_idt18'))
            )
        except TimeoutException:
            logger.error("Loading 40s time out")
            self.driver.close()

        logger.info("Reordering the data according to time")
        logger.debug("First click 'Date'")
        self.driver.find_element_by_id("form:j_idt111:j_idt112").click()

        logger.debug("Loading")
        try:
            WebDriverWait(self.driver, 40).until(
                EC.invisibility_of_element_located((By.ID, 'form:j_idt18'))
            )
        except TimeoutException:
            logger.error("Loading 40s time out")
            self.driver.close()

        logger.debug("Second click 'Date'")
        self.driver.find_element_by_id("form:j_idt111:j_idt112").click()

        logger.debug("Loading")
        try:
            WebDriverWait(self.driver, 40).until(
                EC.invisibility_of_element_located((By.ID, 'form:j_idt18'))
            )
        except TimeoutException:
            logger.error("Loading 40s time out")
            self.driver.close()

        logger.info("Reading data")
        data = self.driver.find_element_by_id("form:dataTableFavori")

        '''
        logger.debug("Reading data")
        duree = self.driver.find_element_by_id("form:dureeAbs").text
        print("Durée totale des absences: " + duree)
        absences = self.driver.find_elements_by_xpath("//tbody[@id='form:j_idt109_data']/tr")
        date_time_now = datetime.datetime.now()
        logger.info("Current time: " + str(date_time_now))
        logger.info("Filtering data")
        for absence in absences:
            date = absence.find_element_by_xpath("./td[1]").text
            date_time = datetime.datetime.strptime(date, '%d/%m/%y')
            diff = (date_time_now - date_time).days
            if diff < 100:
                print("Date: " + str(date_time))
                epreuve = absence.find_element_by_xpath("./td[4]").text
                print("Horaire: " + epreuve)
                note = absence.find_element_by_xpath("./td[5]").text
                print("Cours: " + note)
                print("\n")
        '''

        return data.get_attribute("innerHTML")

    def to_note(self):
        logger.info("Navigating to 'Mes Notes'")
        logger.debug("Click 'Mes notes'")
        try:
            WebDriverWait(self.driver, 40).until(
                EC.visibility_of_element_located((By.LINK_TEXT, "Mes notes"))
            ).click()
        except NoSuchElementException:
            logger.error("'Mes notes' no found")
            self.driver.close()
        except TimeoutException:
            logger.error("Loading 40s time out")
            self.driver.close()

        logger.debug("Loading")
        try:
            WebDriverWait(self.driver, 40).until(
                EC.invisibility_of_element_located((By.ID, 'form:j_idt18'))
            )
        except TimeoutException:
            logger.error("Loading 40s time out")
            self.driver.close()

        logger.info("Reading data")
        data = self.driver.find_element_by_id("form:j_idt144")

        '''
        logger.debug("Reading data")
        table = self.driver.find_element_by_id("form:j_idt144_data")
        notes = table.find_elements_by_xpath("./tr")
        for note in notes:
            date = note.find_element_by_xpath("./td[1]/span[2]").text
            print("Date: " + date)
            matiere = note.find_element_by_xpath("./td[2]/span[2]").text
            print("Matière: " + matiere)
            module = note.find_element_by_xpath("./td[3]/span[2]").text
            print("Module: " + module)
            epreuve = note.find_element_by_xpath("./td[4]/span[2]").text
            print("Epreuve: " + epreuve)
            note = note.find_element_by_xpath("./td[5]/span[2]").text
            print("Note obtenue: " + note)
            print("\n")
        '''

        return data.get_attribute("innerHTML")

if __name__ == "__main__":
    spider = Crawler()
    spider.connect()
    txt = spider.to_absence()
    with io.open("text.txt", 'w', encoding='utf8') as f:
        f.write(txt)