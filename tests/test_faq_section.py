import pytest
from selenium import webdriver
from pages.faq_page import FAQPage
from data.test_data import EXPECTED_FAQ_RESPONSES
import time
import allure
from config.urls import HOME_PAGE

@pytest.mark.usefixtures("setup")
class TestFAQSection:
    @allure.title('Проверка ответа FAQ с индексом {index} на соответствие тексту "{expected_text}"')
    @allure.step('Проверка ответа FAQ с индексом {index} на соответствие тексту {expected_text}')
    @pytest.mark.parametrize("index, expected_text", [
        (i, text) for i, text in enumerate(EXPECTED_FAQ_RESPONSES)
    ])
    def test_faq_answers(self, index, expected_text):
        faq_page = FAQPage(self.driver)
        
        faq_page.navigate_to(HOME_PAGE)
        faq_page.accept_cookies()
        time.sleep(1)  # Даём дополнительное время на анимацию закрытия баннера
        
        faq_page.click_faq_item(index)
        actual_text = faq_page.get_faq_text(index)
        
        assert actual_text == expected_text, f"Ответ для вопроса {index} не совпадает. Ожидалось: {expected_text}, получено: {actual_text}"