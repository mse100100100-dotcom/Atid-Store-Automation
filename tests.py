from pages import AtidStorePage
import pytest

class TestAtidStore:

    def test_verify_store_navigation(self, page):
        atid = AtidStorePage(page)
        atid.navigate()
        atid.store_btn.click()
        assert page.url == atid.store_page_url
        
    def test_verify_contacut_us_navigation(self, page):
        atid = AtidStorePage(page)
        atid.navigate()
        atid.contact_btn.click()
        assert page.url == atid.contact_us_page
        
    def test_verify_women_navigation(self, page):
        atid = AtidStorePage(page)
        atid.navigate()
        atid.women_menu_link.click()
        assert page.url == atid.women_category_url

    def test_verify_product_can_be_added_to_cart(self, page):
        atid = AtidStorePage(page)
        atid.navigate()
        page.locator(f"[href='{atid.women_category_url}']").nth(0).click()
        atid.product_title.click()
        atid.add_to_cart_btn.click()
        atid.cart_count_icon.click()
        product = "Anchor Bracelet"
        assert page.get_by_text(product).first.is_visible()

    def test_verify_successful_checkout_flow(self, page):
        atid = AtidStorePage(page)
        atid.navigate()
        page.locator(f"[href='{atid.women_category_url}']").nth(0).click()
        atid.product_title.click()
        atid.add_to_cart_btn.click()
        atid.cart_count_icon.click()
        page.locator("[class = 'checkout-button button alt wc-forward']").click()
        page.click('#select2-billing_country-container')
        page.locator("li.select2-results__option", has_text="Israel").click()

        billing_data = {
                "#billing_first_name": "tzedek",
                "#billing_last_name": "wasi",
                "#billing_company": "tech-career",
                "#billing_address_1": "Hanita 6",
                "#billing_city": "Lod",
                "#billing_postcode": "71234",
                "#billing_phone": "0546276984",
                "#billing_email": "tzedek@example.com"}

        for selector, value in billing_data.items():
                page.locator(selector).fill(value)
                
        page.locator("[id='place_order']").click()
        
        expected_payment_method = "visa"
        actual_payement_methods = page.locator("//div[@class='woocommerce-info']").last.inner_text() 
        assert expected_payment_method in actual_payement_methods

    def test_verify_cart_quantity_update_works(self, page):
        atid = AtidStorePage(page)
        atid.navigate()
        page.locator(f"[href='{atid.women_category_url}']").nth(0).click()
        atid.product_title.click()
        atid.add_to_cart_btn.click()
        atid.cart_count_icon.click()
        
        page.locator(atid.quantity_selector).first.fill("2")
        current_value = page.locator(atid.quantity_selector).first.input_value()
        assert current_value == "2"

    def test_verify_contact_form_shows_confirmation_message(self, page):
        atid = AtidStorePage(page)
        atid.navigate()
        atid.contact_menu_link.click()
        details = ["tzedek", "nksnjkasnfjds@gmail.com"]
        attribute = page.locator(".wpforms-field-large.wpforms-field-required")
        for i in range(len(details)):
            attribute.nth(i).fill(details[i])
        page.locator("[id='wpforms-15-field_5']").fill("project")
        page.locator("[id ='wpforms-15-field_2']").fill("i want a refund!")
        page.locator("[id ='wpforms-submit-15']").click()
        confirmation_element = page.locator(".wpforms-confirmation-container")
        assert "Thanks" in confirmation_element.inner_text()