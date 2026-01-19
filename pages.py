from playwright.sync_api import Page

class AtidStorePage:
    def __init__(self, page: Page):
        self.page = page
        
        
        self.home_Page_url = "https://atid.store/"
        self.store_page_url = f"{self.home_Page_url}store/"
        self.women_category_url = f"{self.home_Page_url}product-category/women/"
        self.contact_us_page = f"{self.home_Page_url}contact-us/"
        
        
        self.store_btn = self.page.locator("[class='elementor-button-text']").nth(0)
        self.contact_btn = self.page.locator("[class='elementor-button-text']").nth(1)
        self.women_menu_link = self.page.locator("[class='menu-link']").nth(3)
        self.contact_menu_link = self.page.locator("[class='menu-link']").nth(6)
        
        self.product_title = self.page.locator("[class='woocommerce-loop-product__title']").nth(0)
        self.add_to_cart_btn = self.page.locator("[type='submit']").nth(0)
        self.cart_count_icon = self.page.locator("[class='count']").nth(0)
        self.quantity_selector = "input[name*='[qty]']"

    def navigate(self):
        self.page.goto(self.home_Page_url)