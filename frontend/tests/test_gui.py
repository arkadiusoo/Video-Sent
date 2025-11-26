import time
import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options


BASE_URL = "http://localhost:51731/"


class TestGUI:

    @pytest.fixture(autouse=True)
    def setup(self):
        chrome_options = Options()
        # chrome_options.add_argument("--headless=new")
        self.driver = webdriver.Chrome(options=chrome_options)
        self.driver.set_window_size(1400, 900)
        self.driver.get(BASE_URL)
        yield
        self.driver.quit()

    def fill_form(self, url, device, lang="pl"):
        url_input = self.driver.find_element(By.ID, "url")
        device_input = self.driver.find_element(By.ID, "device")

        url_input.clear()
        device_input.clear()

        url_input.send_keys(url)
        device_input.send_keys(device)

        if lang == "pl":
            self.driver.find_element(By.ID, "lang-pl").click()
        else:
            self.driver.find_element(By.ID, "lang-en").click()


    def test_VS_GUI_01_empty_fields(self):
        submit = self.driver.find_element(By.CSS_SELECTOR, "button[type=submit]")
        submit.click()
        err = self.driver.find_element(By.ID, "url-err").text
        assert "URL jest wymagany." in err


    def test_VS_GUI_02_valid_youtube(self):
        self.fill_form(
            "https://www.youtube.com/watch?v=dQw4w9WgXcQ",
            "Test Device",
            lang="pl"
        )

        submit = self.driver.find_element(By.CSS_SELECTOR, "button[type=submit]")
        submit.click()

        btn = self.driver.find_element(By.CSS_SELECTOR, "button.btn-brand[disabled]")
        assert btn is not None



    def test_VS_GUI_03_invalid_url(self):
        self.fill_form("abcd1234", "Test Device")

        submit = self.driver.find_element(By.CSS_SELECTOR, "button[type=submit]")
        submit.click()
        err = self.driver.find_element(By.ID, "url-err").text
        assert "Podaj poprawny adres URL." in err


    def test_VS_GUI_04_lang_switch(self):
        self.fill_form(
            "https://www.youtube.com/watch?v=dQw4w9WgXcQ",
            "Test Device",
            lang="en"
        )

        submit = self.driver.find_element(By.CSS_SELECTOR, "button[type=submit]")
        submit.click()
        time.sleep(1)

        assert self.driver.find_element(By.ID, "lang-en").is_selected()


    def test_VS_GUI_06_results_section(self):
        self.fill_form(
            "https://www.youtube.com/watch?v=dQw4w9WgXcQ",
            "Phone X"
        )

        self.driver.find_element(By.CSS_SELECTOR, "button[type=submit]").click()
        time.sleep(25)

        elem = self.driver.find_element(By.CSS_SELECTOR, "div.card-body")
        assert elem is not None


    def test_VS_GUI_07_charts_enabled(self):

        btn = self.driver.find_element(By.CSS_SELECTOR, "button.btn-brand[disabled]")
        assert btn is not None


    def test_VS_GUI_08_theme_switch(self):
        theme_btn = self.driver.find_element(By.CSS_SELECTOR, "button[aria-label='Switch to light mode']")
        theme_btn.click()

        # Walidacja minimalna: przycisk zmienia tekst
        assert theme_btn.text in ["Jasny", "Ciemny"]


    def test_VS_GUI_09_language_switch_ui(self):
        lang_select = self.driver.find_element(By.CSS_SELECTOR, "select")
        lang_select.click()

        option_en = self.driver.find_element(By.CSS_SELECTOR, "option[value='en']")
        option_en.click()

        assert option_en.is_selected()


    def test_VS_GUI_10_reset_after_refresh(self):
        self.fill_form("https://youtube.com/test", "Device X")
        self.driver.refresh()

        url_val = self.driver.find_element(By.ID, "url").get_attribute("value")
        device_val = self.driver.find_element(By.ID, "device").get_attribute("value")

        assert url_val == ""
        assert device_val == ""


    def test_VS_GUI_11_responsiveness(self):
        self.driver.set_window_size(375, 812)

        header = self.driver.find_element(By.TAG_NAME, "h1").is_displayed()
        assert header is True


    def test_VS_GUI_12_placeholders(self):
        url_ph = self.driver.find_element(By.ID, "url").get_attribute("placeholder")
        device_ph = self.driver.find_element(By.ID, "device").get_attribute("placeholder")

        assert url_ph == "Wklej URL YouTube lub TikTok…"
        assert device_ph == "Wpisz tutaj nazwę urządzenia"