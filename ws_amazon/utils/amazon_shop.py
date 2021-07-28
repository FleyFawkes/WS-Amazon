
class WebDriverContext:
    """context manager"""

    def __init__(self, driver):
        self.driver = driver

    def __enter__(self):
        return self.driver

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.driver.quit()


class AmazonShop:

    def __init__(self, driver):
        self.driver = driver
