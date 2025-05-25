import pytest
from selenium import webdriver
from pages.order_page import OrderPage
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

@pytest.mark.usefixtures("setup")
class TestLogoNavigation:
    def test_scooter_logo_click(self):
        driver = self.driver
        order_page = OrderPage(driver)
        
        driver.get("https://qa-scooter.praktikum-services.ru/")
        
        order_page.accept_cookies()
        
        order_page.click_logo_scooter()
        
        assert driver.current_url == "https://qa-scooter.praktikum-services.ru/", "Логотип 'Самокат' не возвращает на главную страницу"

    def test_yandex_logo_click(self):
        driver = self.driver
        order_page = OrderPage(driver)
        
        driver.get("https://qa-scooter.praktikum-services.ru/")
        
        order_page.accept_cookies()
        
        original_window = driver.current_window_handle
        
        yandex_logo = WebDriverWait(driver, 10).until(EC.element_to_be_clickable(order_page.YANDEX_LOGO_LINK))
        yandex_logo.click()
        
        try:
            WebDriverWait(driver, 10).until(EC.number_of_windows_to_be(2))
            all_windows = driver.window_handles
            new_window = [window for window in all_windows if window != original_window][0]
            driver.switch_to.window(new_window)
            
            WebDriverWait(driver, 20).until(
                lambda d: "yandex.ru" in d.current_url or "ya.ru" in d.current_url,
                "URL не изменился на страницу Яндекса"
            )
            
            assert "yandex.ru" in driver.current_url or "ya.ru" in driver.current_url, f"Логотип 'Яндекс' не открывает страницу Яндекса. Текущий URL: {driver.current_url}"
        except Exception as e:
            print(f"Ошибка при открытии вкладки: {e}")
            raise
        finally:
            if len(driver.window_handles) > 1:
                driver.close()
                driver.switch_to.window(original_window)