import pytest
from selenium import webdriver
from pages.order_page import OrderPage
import allure
from config.urls import HOME_PAGE, BASE_URL

@pytest.mark.usefixtures("setup")
class TestLogoNavigation:
    @allure.title('Проверка клика по логотипу "Самокат" и возвращения на главную страницу')
    @allure.step('Проверка клика по логотипу "Самокат" и возвращения на главную страницу')
    def test_scooter_logo_click(self):
        order_page = OrderPage(self.driver)
        
        order_page.navigate_to(HOME_PAGE)
        order_page.accept_cookies()
        
        order_page.click_logo_scooter()
        assert order_page.get_current_url() == f"{BASE_URL}{HOME_PAGE}", "Логотип 'Самокат' не возвращает на главную страницу"

    @allure.title('Проверка клика по логотипу "Яндекс" и открытия новой вкладки')
    @allure.step('Проверка клика по логотипу "Яндекс" и открытия новой вкладки')
    def test_yandex_logo_click(self):
        order_page = OrderPage(self.driver)
        
        order_page.navigate_to(HOME_PAGE)
        order_page.accept_cookies()
        
        original_window = order_page.get_current_window_handle()
        order_page.click_logo_yandex()
        
        new_window = order_page.switch_to_new_tab(original_window, "yandex.ru")
        current_url = order_page.get_current_url()
        assert "yandex.ru" in current_url or "ya.ru" in current_url, f"Логотип 'Яндекс' не открывает страницу Яндекса. Текущий URL: {current_url}"