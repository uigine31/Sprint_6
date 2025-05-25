from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains

class FAQPage:
    def __init__(self, driver):
        self.driver = driver

    # Локатор для заголовка раздела
    HEADING_FAQ_SECTION = (By.XPATH, '//div[@class="Home_SubHeader__zwi_E" and text()="Вопросы о важном"]')

    # Локатор для cookie-баннера
    COOKIE_BANNER_ACCEPT = (By.XPATH, '//button[contains(text(), "Принять") or contains(text(), "Согласен") or contains(text(), "ОК") or contains(text(), "Да все привыкли")]')

    # Локаторы для вопросов и ответов
    PRICE_AND_PAYMENT = (By.ID, 'accordion__heading-0')
    TEXT_PRICE_AND_PAYMENT = (By.ID, 'accordion__panel-0')
    MULTIPLE_SCOOTERS = (By.ID, 'accordion__heading-1')
    TEXT_MULTIPLE_SCOOTERS = (By.ID, 'accordion__panel-1')
    RENTAL_DURATION = (By.ID, 'accordion__heading-2')
    TEXT_RENTAL_DURATION = (By.ID, 'accordion__panel-2')
    ORDER_TODAY = (By.ID, 'accordion__heading-3')
    TEXT_ORDER_TODAY = (By.ID, 'accordion__panel-3')
    EXTEND_OR_RETURN_EARLY = (By.ID, 'accordion__heading-4')
    TEXT_EXTEND_OR_RETURN_EARLY = (By.ID, 'accordion__panel-4')
    CHARGER_WITH_SCOOTER = (By.ID, 'accordion__heading-5')
    TEXT_CHARGER_WITH_SCOOTER = (By.ID, 'accordion__panel-5')
    ORDER_CANCELLATION = (By.ID, 'accordion__heading-6')
    TEXT_ORDER_CANCELLATION = (By.ID, 'accordion__panel-6')
    DELIVERY_OUTSIDE_MKAD = (By.ID, 'accordion__heading-7')
    TEXT_DELIVERY_OUTSIDE_MKAD = (By.ID, 'accordion__panel-7')

    # Метод для закрытия cookie-баннера
    def accept_cookies(self):
        try:
            WebDriverWait(self.driver, 5).until(EC.element_to_be_clickable(self.COOKIE_BANNER_ACCEPT)).click()
        except:
            pass  

    # Методы для работы с локаторами
    def click_faq_item(self, index):
        faq_item = (By.ID, f"accordion__heading-{index}")
        element = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located(faq_item))
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", element)
        self.driver.execute_script("window.scrollBy(0, -100);")  
        WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable(faq_item)).click()

    def get_faq_text(self, index):
        faq_text = (By.ID, f"accordion__panel-{index}")
        return WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located(faq_text)).text