import pytest
from selenium import webdriver
from pages.faq_page import FAQPage
from data.test_data import EXPECTED_FAQ_RESPONSES

@pytest.mark.usefixtures("setup")
class TestFAQSection:
    @pytest.mark.parametrize("index, expected_text", [
        (i, text) for i, text in enumerate(EXPECTED_FAQ_RESPONSES)
    ])
    def test_faq_answers(self, index, expected_text):
        driver = self.driver
        faq_page = FAQPage(driver)
        
        driver.get("https://qa-scooter.praktikum-services.ru/")
        
        faq_page.click_faq_item(index)
        
        actual_text = faq_page.get_faq_text(index)
        
        assert actual_text == expected_text, f"Ответ для вопроса {index} не совпадает. Ожидалось: {expected_text}, получено: {actual_text}"