"""
Локаторы для модальных окон.
"""

from ..base import locator_registry


def register_modal_locators():
    """Регистрирует все локаторы для модальных окон."""

    # === ОБЩИЕ МОДАЛЬНЫЕ ОКНА ===

    locator_registry.add_locator(
        "MODAL_CONTENT",
        ".ant-modal-content",
        "Контент модального окна",
        component="modal",
    )

    locator_registry.add_locator(
        "MODAL_CLOSE_BUTTON",
        ".ant-modal-close",
        "Кнопка закрытия модального окна",
        component="modal",
    )

    locator_registry.add_locator(
        "MODAL_TITLE",
        ".ant-modal-title",
        "Заголовок модального окна",
        component="modal",
    )

    # === МОДАЛЬНЫЕ ОКНА 360 TOUR ===

    locator_registry.add_locator(
        "MODAL_360_CONTENT",
        '//img[contains(@class, "__react-image-turntable-img")] | //video | //canvas',
        "Контент модального окна 360 Area Tour",
        component="modal",
    )

    locator_registry.add_locator(
        "MODAL_360_CLOSE_BUTTON",
        '//button[contains(@class, "close") and @aria-label="close"]',
        "Кнопка закрытия модального окна 360 Area Tour",
        component="modal",
    )

    # === МОДАЛЬНЫЕ ОКНА AMENITIES ===

    locator_registry.add_locator(
        "MODAL_AMENITIES_SLIDER",
        ".ant-carousel",
        "Слайдер в модальном окне amenities",
        component="modal",
    )

    locator_registry.add_locator(
        "MODAL_AMENITIES_SLIDER_IMAGES",
        ".ant-carousel .ant-carousel-item img",
        "Изображения в слайдере amenities",
        component="modal",
    )

    locator_registry.add_locator(
        "MODAL_AMENITIES_SLIDER_INDICATORS",
        ".ant-carousel .ant-carousel-dots li",
        "Индикаторы слайдера amenities",
        component="modal",
    )

    locator_registry.add_locator(
        "MODAL_AMENITIES_PREV_BUTTON",
        ".ant-carousel .ant-carousel-prev",
        "Кнопка предыдущего слайда в amenities",
        component="modal",
    )

    locator_registry.add_locator(
        "MODAL_AMENITIES_NEXT_BUTTON",
        ".ant-carousel .ant-carousel-next",
        "Кнопка следующего слайда в amenities",
        component="modal",
    )

    # === МОДАЛЬНЫЕ ОКНА ФОРМ ===

    locator_registry.add_locator(
        "MODAL_CALLBACK_FORM",
        "//div[@class='ant-modal-content']",
        "Модальное окно callback формы",
        component="modal",
    )

    locator_registry.add_locator(
        "MODAL_SUCCESS_MESSAGE",
        'xpath=(//div[@class="ant-modal-content"])[1]',
        "Модальное окно с сообщением об успехе",
        component="modal",
    )

    locator_registry.add_locator(
        "MODAL_SUCCESS_TITLE",
        'xpath=.//div[contains(text(), "Thank you!")]',
        "Заголовок модального окна успеха",
        component="modal",
    )

    locator_registry.add_locator(
        "MODAL_SUCCESS_TEXT",
        'xpath=.//div[contains(text(), "Our specialist will contact you shortly.")]',
        "Текст модального окна успеха",
        component="modal",
    )


# Регистрируем локаторы при импорте
register_modal_locators()


class ModalLocators:
    """Удобный доступ к локаторам модальных окон."""

    def get(self, name: str, use_fallback: bool = False) -> str:
        """Получить локатор по имени."""
        return locator_registry.get_locator(name, use_fallback)

    def get_all_locators(self) -> dict:
        """Получить все локаторы модальных окон."""
        return locator_registry.get_component_locators("modal")

    def get_360_modal_locators(self) -> dict:
        """Получить локаторы модальных окон 360 Area Tour."""
        all_locators = self.get_all_locators()
        return {k: v for k, v in all_locators.items() if "360" in k}

    def get_amenities_modal_locators(self) -> dict:
        """Получить локаторы модальных окон amenities."""
        all_locators = self.get_all_locators()
        return {k: v for k, v in all_locators.items() if "AMENITIES" in k}

    def get_form_modal_locators(self) -> dict:
        """Получить локаторы модальных окон форм."""
        all_locators = self.get_all_locators()
        return {
            k: v
            for k, v in all_locators.items()
            if any(word in k for word in ["FORM", "SUCCESS", "CALLBACK"])
        }

    def get_common_modal_locators(self) -> dict:
        """Получить общие локаторы модальных окон."""
        all_locators = self.get_all_locators()
        return {
            k: v
            for k, v in all_locators.items()
            if k.startswith("MODAL_")
            and not any(
                word in k
                for word in ["360", "AMENITIES", "FORM", "SUCCESS", "CALLBACK"]
            )
        }


# Экспортируем объект
modal_locators = ModalLocators()
