class ProjectLocators:

    ALL_UNITS_BUTTON = "//button[.//span[text()='All units']]"
    AVIALABLE_APART_CARD  = "(//h3[contains(text(), 'APT. 104')])[2]"
    AVIALABLE_APART = "//span[@class='ant-menu-title-content' and text()='APARTMENT 104']"

    class AgentPage:
        SALES_OFFER_BUTTON = "//button[.//span[text() = 'Sales Offer']]"
        DOWNLOAD_PDF_BUTTON = "//button[.//span[text() = 'Download PDF']]"

    # Элементы для клиентской страницы
    class ClientPage:
        CALLBACK_FORM_BUTTON = "//button[.//*[@aria-label='phone']]"
        CALLBACK_FORM_MODAL = "//div[@class='ant-modal-content']"
