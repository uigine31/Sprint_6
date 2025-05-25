import pytest
from selenium import webdriver
from pages.order_page import OrderPage
from data.test_data import FIRST_ORDER_DETAILS, SECOND_ORDER_DETAILS

@pytest.mark.usefixtures("setup")
class TestOrderFlow:
    @pytest.mark.parametrize("order_data, button_position", [
        (FIRST_ORDER_DETAILS, True),  # Верхняя кнопка
        (SECOND_ORDER_DETAILS, False),  # Нижняя кнопка
    ])
    def test_create_order(self, order_data, button_position):
        driver = self.driver
        order_page = OrderPage(driver)
        
        driver.get("https://qa-scooter.praktikum-services.ru/")
        
        order_page.click_order_button(top=button_position)
        
        order_page.fill_first_form(
            name=order_data["name"],
            surname=order_data["surname"],
            address=order_data["address"],
            metro=order_data["metro_station"],
            phone=order_data["phone"]
        )
        
        order_page.fill_second_form(
            date=order_data["date"],
            rental_period=order_data["rental_period"],
            color=order_data["color"],
            comment=order_data["comment"]
        )
        
        order_page.submit_order()
        
        assert order_page.check_success_modal(), "Модальное окно 'Заказ оформлен' не отображается"