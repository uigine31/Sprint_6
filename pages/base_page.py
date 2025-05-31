from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import TimeoutException, ElementClickInterceptedException
from abc import ABC
import allure
import time
from config.urls import BASE_URL

class BasePage(ABC):
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(self.driver, 10)
        self.action = ActionChains(self.driver)

    @allure.step('Закрытие cookie-баннера с локатором {locator}')
    def accept_cookies(self, locator):
        """Закрытие cookie-баннера с ожиданием его исчезновения."""
        try:
            # Ждём, пока баннер станет кликабельным
            banner = self.wait.until(EC.element_to_be_clickable(locator))
            # Прокручиваем к баннеру
            self.scroll_to_element(banner)
            # Кликаем
            banner.click()
            # Ждём, пока баннер исчезнет
            self.wait.until(EC.invisibility_of_element_located(locator))
        except (TimeoutException, ElementClickInterceptedException) as e:
            # Пропускаем вывод, оставляем только обработку исключения
            pass
        except Exception as e:
            # Пробрасываем другие неожиданные исключения для дальнейшего анализа
            raise e

    @allure.step('Ожидание появления элемента с локатором {locator}')
    def wait_for_element(self, locator):
        """Ожидание появления элемента."""
        return self.wait.until(EC.presence_of_element_located(locator))

    @allure.step('Ожидание кликабельности элемента с локатором {locator}')
    def wait_for_element_to_be_clickable(self, locator, timeout=10):
        """Ожидание, пока элемент станет кликабельным с указанным таймаутом."""
        wait = WebDriverWait(self.driver, timeout)
        return wait.until(EC.element_to_be_clickable(locator))

    @allure.step('Клик по элементу с локатором {locator}')
    def click_element(self, locator):
        """Клик по элементу с ожиданием."""
        element = self.wait_for_element_to_be_clickable(locator)
        self.scroll_to_element(element)
        element.click()

    @allure.step('Перемещение курсора к элементу с локатором {locator}')
    def move_to_element(self, locator):
        """Перемещение курсора к элементу."""
        element = self.wait_for_element(locator)
        self.action.move_to_element(element).perform()

    @allure.step('Ввод текста {text} в элемент с локатором {locator}')
    def send_keys_to_element(self, locator, text):
        """Ввод текста в элемент."""
        element = self.wait_for_element(locator)
        element.clear()
        element.send_keys(text)

    @allure.step('Получение текста элемента с локатором {locator}')
    def get_element_text(self, locator):
        """Получение текста элемента."""
        element = self.wait_for_element(locator)
        return element.text

    @allure.step('Получение текущего URL')
    def get_current_url(self):
        """Получение текущего URL."""
        return self.driver.current_url

    @allure.step('Переключение на новую вкладку и ожидание URL {expected_url_part}')
    def switch_to_new_tab(self, original_window, expected_url_part):
        """Переключение на новую вкладку и ожидание URL."""
        self.wait.until(EC.number_of_windows_to_be(2))
        all_windows = self.driver.window_handles
        new_window = None
        for window in all_windows:
            if window != original_window:
                new_window = window
                break
        if new_window is None:
            raise Exception("Новая вкладка не найдена")
        self.driver.switch_to.window(new_window)
        self.wait.until(lambda d: expected_url_part in d.current_url)
        return new_window

    @allure.step('Закрытие текущей вкладки и возврат к оригинальной')
    def close_tab_and_switch_back(self, original_window):
        """Закрытие текущей вкладки и возврат к оригинальной."""
        if len(self.driver.window_handles) > 1:
            self.driver.close()
            self.driver.switch_to.window(original_window)

    @allure.step('Прокрутка к элементу')
    def scroll_to_element(self, element):
        """Прокрутка к элементу с небольшим смещением."""
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", element)
        self.driver.execute_script("window.scrollBy(0, -100);")

    @allure.step('Переход по пути {path}')
    def navigate_to(self, path):
        """Переход по указанному пути с учётом базового URL."""
        full_url = f"{BASE_URL}{path}"
        self.driver.get(full_url)

    @allure.step('Получение текущего дескриптора окна')
    def get_current_window_handle(self):
        """Получение дескриптора текущего окна."""
        return self.driver.current_window_handle