from selenium.webdriver.common.by import By


class QciUiTools():
    '''
    Provide tools to make working with QCI UI easier, and the process
    of doing so consistent.

    Expects to be passed an instance of Page.
    '''
    def __init__(self, page):
        self.page = page

    def build_qci_spinner_xpath(self, text=None):
        # QCI spinners are done via a div tag with a class of spinner-md
        qci_spinner_xpath_str = "div[contains(@class, 'spinner-md')]"

        # If they want to to catch a spinner with specific text
        # build the xpath string to include that.   At the time of
        # writing this, the spinner div and the text span tag are peer
        # nodes in the HTML tree.
        if text is not None:
            qci_spinner_text_xpath_str = "//span[@class = 'spinner-text' and contains(., '{}')]".format(text)
            qci_spinner_xpath_str = "{}/../{}".format(
                qci_spinner_text_xpath_str,
                qci_spinner_xpath_str,
            )

        # Otherwise we need to prepend the // so we can find the
        # spinner anywhere in the document tree:
        else:
            qci_spinner_xpath_str = "//{}".format(qci_spinner_xpath_str)

        return qci_spinner_xpath_str

    def wait_for_spinner(self, text=None, timeout=None):
        qci_spinner_xpath_str = self.build_qci_spinner_xpath(text)

        qci_spinner_loc = (By.XPATH, qci_spinner_xpath_str)

        self.page.wait_until_element_is_not_visible(
            qci_spinner_loc,
            timeout
        )
