import pytest
from selenium import webdriver
from pages.faq_page import FAQPage
from data.test_data import EXPECTED_FAQ_RESPONSES
import allure
from config.urls import HOME_PAGE
from selenium.webdriver.support import expected_conditions as EC

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
        # Ждём исчезновения баннера вместо time.sleep
        faq_page.wait.until(EC.invisibility_of_element_located(faq_page.COOKIE_BANNER_ACCEPT))
        
        faq_page.click_faq_item(index)
        actual_text = faq_page.get_faq_text(index)
        
        assert actual_text == expected_text, f"Ответ для вопроса {index} не совпадает. Ожидалось: {expected_text}, получено: {actual_text}"