from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from abc import ABC

class BasePage(ABC):
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(self.driver, 10)
        self.action = ActionChains(self.driver)

    def accept_cookies(self, locator):
        """Закрытие cookie-баннера."""
        try:
            self.wait.until(EC.element_to_be_clickable(locator)).click()
        except:
            pass

    def wait_for_element(self, locator):
        """Ожидание появления элемента."""
        return self.wait.until(EC.presence_of_element_located(locator))

    def wait_for_element_to_be_clickable(self, locator):
        """Ожидание, пока элемент станет кликабельным."""
        return self.wait.until(EC.element_to_be_clickable(locator))

    def click_element(self, locator):
        """Клик по элементу с ожиданием."""
        element = self.wait_for_element_to_be_clickable(locator)
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", element)
        self.driver.execute_script("window.scrollBy(0, -100);")
        element.click()

    def move_to_element(self, locator):
        """Перемещение курсора к элементу."""
        element = self.wait_for_element(locator)
        self.action.move_to_element(element).perform()

    def send_keys_to_element(self, locator, text):
        """Ввод текста в элемент."""
        element = self.wait_for_element(locator)
        element.clear()
        element.send_keys(text)

    def get_element_text(self, locator):
        """Получение текста элемента."""
        element = self.wait_for_element(locator)
        return element.text
    