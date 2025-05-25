from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class OrderPage:
    def __init__(self, driver):
        self.driver = driver

    # Локаторы для кнопок "Заказать" на главной странице
    ORDER_BUTTON_UPPER = (By.XPATH, "//button[@class='Button_Button__ra12g' and not(contains(@class, 'Button_UltraBig__UU3Lp'))]")
    ORDER_BUTTON_LOWER = (By.XPATH, '//button[contains(@class, "Button_Button__ra12g") and contains(@class, "Button_Middle__1CSJM") and text()="Заказать"]')

    # Локатор для cookie-баннера
    COOKIE_BANNER_ACCEPT = (By.XPATH, '//button[contains(text(), "Принять") or contains(text(), "Согласен") or contains(text(), "ОК") or contains(text(), "Да все привыкли")]')

    # Локаторы для формы заказа
    INPUT_NAME = (By.XPATH, '//input[@placeholder="* Имя"]')
    INPUT_SURNAME = (By.XPATH, '//input[@placeholder="* Фамилия"]')
    INPUT_ADDRESS = (By.XPATH, '//input[contains(@placeholder,"Адрес")]')
    INPUT_METRO = (By.CLASS_NAME, 'select-search__input')
    INPUT_PHONE = (By.XPATH, '//input[contains(@placeholder,"Телефон")]')
    NEXT_BUTTON = (By.XPATH, '//button[text()="Далее"]')
    INPUT_DELIVERY_DATE = (By.XPATH, '//input[@placeholder="* Когда привезти самокат"]')
    CALENDAR = (By.CLASS_NAME, 'react-datepicker')
    CALENDAR_NEXT_MONTH_BUTTON = (By.XPATH, '//button[contains(@class,"navigation--next")]')
    CALENDAR_DATE_TODAY = (By.XPATH, '//div[contains(@class,"today")]')
    CALENDAR_DATE_SELECTED = (By.XPATH, '//*[contains(@class,"selected") and not(contains(@class, "outside-month"))]')
    INPUT_RENTAL_DURATION = (By.CLASS_NAME, 'Dropdown-control')
    INPUT_COURIER_COMMENT = (By.XPATH, '//input[contains(@placeholder,"Комментарий")]')
    SUBMIT_ORDER_BUTTON = (By.XPATH, '//*[contains(@class,"Order_Buttons")]//button[text()="Заказать"]')
    CONFIRM_ORDER_BUTTON = (By.XPATH, '//button[text()="Да"]')
    SUCCESS_MODAL = (By.XPATH, '//div[text()="Заказ оформлен"]')

    # Локаторы для логотипов
    SCOOTER_LOGO_LINK = (By.CSS_SELECTOR, ".Header_LogoScooter__3lsAR")
    YANDEX_LOGO_LINK = (By.CSS_SELECTOR, ".Header_LogoYandex__3TSOI")

    # Метод для закрытия cookie-баннера
    def accept_cookies(self):
        try:
            WebDriverWait(self.driver, 5).until(EC.element_to_be_clickable(self.COOKIE_BANNER_ACCEPT)).click()
        except:
            pass  

    # Динамические локаторы
    def get_metro_station_locator(self, station):
        return (By.XPATH, ".//div[text()='{}']/ancestor::button".format(station))

    def get_date_locator(self):
        return self.CALENDAR_DATE_TODAY

    def get_rental_period_locator(self, period):
        return (By.XPATH, f'//div[@class="Dropdown-menu"]/div[text()="{period}"]')

    def get_color_locator(self, color):
        return (By.ID, color)

    # Методы для работы с локаторами
    def click_order_button(self, top=False):
        locator = self.ORDER_BUTTON_UPPER if top else self.ORDER_BUTTON_LOWER
        try:
            element = WebDriverWait(self.driver, 30).until(EC.presence_of_element_located(locator))
            self.driver.execute_script("arguments[0].scrollIntoView(true);", element)
            WebDriverWait(self.driver, 30).until(EC.element_to_be_clickable(locator))
            element.click()
        except Exception as e:
            print(f"Ошибка при клике на кнопку 'Заказать': {e}")
            raise

    def fill_first_form(self, name, surname, address, metro, phone):
        self.driver.find_element(*self.INPUT_NAME).send_keys(name)
        self.driver.find_element(*self.INPUT_SURNAME).send_keys(surname)
        self.driver.find_element(*self.INPUT_ADDRESS).send_keys(address)
        metro_input = WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable(self.INPUT_METRO))
        metro_input.click()
        WebDriverWait(self.driver, 15).until(EC.presence_of_element_located((By.CLASS_NAME, "select-search__row")))
        if not self.driver.find_elements(*self.get_metro_station_locator(metro)):
            raise Exception(f"Станция метро '{metro}' не найдена в выпадающем списке. Проверьте доступные станции.")
        metro_element = WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable(self.get_metro_station_locator(metro)))
        metro_element.click()
        self.driver.find_element(*self.INPUT_PHONE).send_keys(phone)
        self.driver.find_element(*self.NEXT_BUTTON).click()

    def fill_second_form(self, date, rental_period, color, comment):
        self.driver.find_element(*self.INPUT_DELIVERY_DATE).send_keys(date)
        WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable(self.get_date_locator())).click()
        self.driver.find_element(*self.INPUT_RENTAL_DURATION).click()
        self.driver.find_element(*self.get_rental_period_locator(rental_period)).click()
        self.driver.find_element(*self.get_color_locator(color)).click()
        self.driver.find_element(*self.INPUT_COURIER_COMMENT).send_keys(comment)

    def submit_order(self):
        self.driver.find_element(*self.SUBMIT_ORDER_BUTTON).click()
        WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable(self.CONFIRM_ORDER_BUTTON)).click()

    def check_success_modal(self):
        return WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located(self.SUCCESS_MODAL)).is_displayed()

    def click_logo_scooter(self):
        WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable(self.SCOOTER_LOGO_LINK)).click()

    def click_logo_yandex(self):
        element = WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable(self.YANDEX_LOGO_LINK))
        element.click()