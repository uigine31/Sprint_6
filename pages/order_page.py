from selenium.webdriver.common.by import By
from pages.base_page import BasePage
import allure

class OrderPage(BasePage):
    def __init__(self, driver):
        super().__init__(driver)

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

    # Динамические локаторы
    def get_metro_station_locator(self, station):
        return (By.XPATH, ".//div[text()='{}']/ancestor::button".format(station))

    def get_date_locator(self):
        return self.CALENDAR_DATE_TODAY

    def get_rental_period_locator(self, period):
        return (By.XPATH, f'//div[@class="Dropdown-menu"]/div[text()="{period}"]')

    def get_color_locator(self, color):
        return (By.ID, color)

    @allure.step('Клик по кнопке "Заказать" (верхняя или нижняя)')
    def click_order_button(self, top=False):
        locator = self.ORDER_BUTTON_UPPER if top else self.ORDER_BUTTON_LOWER
        self.click_element(locator)

    @allure.step('Заполнение первой формы заказа с данными: {name}, {surname}, {address}, {metro}, {phone}')
    def fill_first_form(self, name, surname, address, metro, phone):
        self.send_keys_to_element(self.INPUT_NAME, name)
        self.send_keys_to_element(self.INPUT_SURNAME, surname)
        self.send_keys_to_element(self.INPUT_ADDRESS, address)
        metro_input = self.wait_for_element_to_be_clickable(self.INPUT_METRO)
        metro_input.click()
        self.wait_for_element((By.CLASS_NAME, "select-search__row"))
        metro_element = self.wait_for_element_to_be_clickable(self.get_metro_station_locator(metro))
        if not metro_element:
            raise Exception(f"Станция метро '{metro}' не найдена в выпадающем списке. Проверьте доступные станции.")
        metro_element.click()
        self.send_keys_to_element(self.INPUT_PHONE, phone)
        self.click_element(self.NEXT_BUTTON)

    @allure.step('Заполнение второй формы заказа с данными: {date}, {rental_period}, {color}, {comment}')
    def fill_second_form(self, date, rental_period, color, comment):
        self.send_keys_to_element(self.INPUT_DELIVERY_DATE, date)
        self.click_element(self.get_date_locator())
        self.click_element(self.INPUT_RENTAL_DURATION)
        self.click_element(self.get_rental_period_locator(rental_period))
        self.click_element(self.get_color_locator(color))
        self.send_keys_to_element(self.INPUT_COURIER_COMMENT, comment)

    @allure.step('Подтверждение заказа')
    def submit_order(self):
        self.click_element(self.SUBMIT_ORDER_BUTTON)
        self.click_element(self.CONFIRM_ORDER_BUTTON)

    @allure.step('Проверка отображения модального окна успешного заказа')
    def check_success_modal(self):
        return self.wait_for_element(self.SUCCESS_MODAL).is_displayed()

    @allure.step('Клик по логотипу "Самокат"')
    def click_logo_scooter(self):
        self.click_element(self.SCOOTER_LOGO_LINK)

    @allure.step('Клик по логотипу "Яндекс"')
    def click_logo_yandex(self):
        self.click_element(self.YANDEX_LOGO_LINK)

    @allure.step('Закрытие cookie-баннера')
    def accept_cookies(self):
        super().accept_cookies(self.COOKIE_BANNER_ACCEPT)