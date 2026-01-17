import pytest
from playwright.sync_api import Playwright
from playwright.sync_api import expect

class TestAtidStore:
    home_Page_url = "https://atid.store/"
    store_page_url = f"{home_Page_url}store/"
    women_category_url = f"{home_Page_url}product-category/women/"
    contact_us_page = f"{home_Page_url}contact-us/"

    @pytest.fixture(autouse=True)
    def setup(self,playwright:Playwright):
        global browser,context,page
        browser = playwright.chromium.launch(headless=False,channel="chrome",slow_mo=1500)
        context = browser.new_context()
        context.tracing.start(screenshots=True, snapshots=True, sources=True)
        page = context.new_page() 
        page.goto(self.home_Page_url)
        
        yield
        context.tracing.stop(path="final_trace.zip")
        context.close()
        page.close()

    def test_verify_store_navigation(self):
      page.locator("[class='elementor-button-text']").nth(0).click()
      assert page.url == self.store_page_url
    
    def test_verify_contacut_us_navigation(self):
      page.locator("[class='elementor-button-text']").nth(1).click()
      assert page.url == self.contact_us_page
    
    def test_verify_women_navigation(self):
      page.locator("[class='menu-link']").nth(3).click()
      assert page.url == self.women_category_url


    def test_verify_product_can_be_added_to_cart(self):
       page.locator(f"[href='{self.women_category_url}']").nth(0).click()
       page.locator("[class='woocommerce-loop-product__title']").nth(0).click()
       page.locator("[type='submit']").nth(0).click()
       page.locator("[class='count']").nth(0).click()
       product = "Anchor Bracelet"
       assert page.get_by_text(product).first.is_visible()


    def test_verify_successful_checkout_flow(self):
       page.locator(f"[href='{self.women_category_url}']").nth(0).click()
       page.locator("[class='woocommerce-loop-product__title']").nth(0).click()
       page.locator("[type='submit']").nth(0).click()
       page.locator("[class='count']").nth(0).click()
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
       actual_payement_methods =  page.locator("//div[@class='woocommerce-info']").last.inner_text() 
       assert expected_payment_method in actual_payement_methods,"No Payment Methods Found!"

    def test_verify_cart_quantity_update_works(self):
      page.locator(f"[href='{self.women_category_url}']").nth(0).click()
      page.locator("[class='woocommerce-loop-product__title']").nth(0).click()
      page.locator("[type='submit']").nth(0).click()
      page.locator("[class='count']").nth(0).click()
      page.locator("[name='cart[b73ce398c39f506af761d2277d853a92][qty]']").fill("2")
      quantity = ("[name='cart[b73ce398c39f506af761d2277d853a92][qty]']")
      quantity_selector = "input[name*='[qty]']"
      current_value = page.locator(quantity_selector).input_value()
      assert current_value == "2"


    def test_verify_contact_form_shows_confirmation_message(self):
      page.locator("[class='menu-link']").nth(6).click()
      details = ["tzedek","nksnjkasnfjds@gmail.com"]
      attribute = page.locator(".wpforms-field-large.wpforms-field-required")
      for i in range(len(details)):
         attribute.nth(i).fill(details[i])
      page.locator("[id='wpforms-15-field_5']").fill("project")
      page.locator("[id ='wpforms-15-field_2']").fill("i want a refund!")
      page.locator("[id ='wpforms-submit-15']").click()
      confirmation_element = page.locator(".wpforms-confirmation-container")

      assert "Thanks" in confirmation_element.inner_text() 
           

