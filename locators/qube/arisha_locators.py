"""Локаторы для проекта Arisha."""

from ..base_locators import BaseLocators


class ArishaLocators(BaseLocators):
    """Локаторы для проекта Arisha."""

    # Основная информация о проекте
    PROJECT_NAME = "arisha"
    PROJECT_DISPLAY_NAME = "Arisha"
    MAP_LOCATOR = 'div[aria-label*="ARISHA TERACCES"], div[aria-label*="Arisha"], div[aria-label*="ARISHA"]'

    # Локаторы для виджета апартамента
    class ApartmentWidget:
        """Локаторы для виджета апартамента Arisha."""

        # Кнопки режимов просмотра
        VIEW_2D_BUTTON = 'button:has-text("2D")'
        VIEW_3D_BUTTON = 'button:has-text("3D")'

        # Кнопки навигации по сценам
        PREV_ARROW = ".widget-tab__isometry-arrow--prev"
        NEXT_ARROW = ".widget-tab__isometry-arrow--next"

        # Индикатор сцен
        SCENE_INDICATOR = '[class*="arrow"]:has-text("/")'

        # Кнопка скорости
        SPEED_BUTTON = 'button:has-text("0.5x")'

    # Локаторы для информации об апартаменте
    class ApartmentInfo:
        """Локаторы для информации об апартаменте Arisha."""

        # Основной контейнер с информацией
        INFO_CONTAINER = "._info_1k7zz_45, .ant-card"

        # Заголовок с номером апартамента
        APARTMENT_NUMBER = '.ant-card:has-text("APT. 104"), ._info_1k7zz_45:has-text("APT. 104")'

        # Информация о типе
        TYPE_INFO = '.ant-card:has-text("Type:"), ._info_1k7zz_45:has-text("Type:")'
        TYPE_VALUE = '.ant-card:has-text("2 Bedroom"), ._info_1k7zz_45:has-text("2 Bedroom")'

        # Информация о этаже
        FLOOR_INFO = '.ant-card:has-text("Floor:"), ._info_1k7zz_45:has-text("Floor:")'
        FLOOR_VALUE = '.ant-card:has-text("Floor: 1"), ._info_1k7zz_45:has-text("Floor: 1")'

        # Информация о здании
        BUILDING_INFO = '.ant-card:has-text("Building:"), ._info_1k7zz_45:has-text("Building:")'
        BUILDING_VALUE = '.ant-card:has-text("Building: 1"), ._info_1k7zz_45:has-text("Building: 1")'

        # Информация о площади
        AREA_INFO = '.ant-card:has-text("Total area:"), ._info_1k7zz_45:has-text("Total area:")'
        AREA_VALUE = '.ant-card:has-text("Total area:"), ._info_1k7zz_45:has-text("Total area:")'

        # Информация о виде
        VIEW_INFO = '.ant-card:has-text("View:"), ._info_1k7zz_45:has-text("View:")'
        VIEW_VALUE = '.ant-card:has-text("Green Community"), ._info_1k7zz_45:has-text("Green Community")'

        # Особенности
        MODERN_DESIGN = '.ant-card:has-text("Modern interior design"), ._info_1k7zz_45:has-text("Modern interior design")'
        HIGH_QUALITY = '.ant-card:has-text("High quality materials"), ._info_1k7zz_45:has-text("High quality materials")'
        BUILT_IN_APPLIANCES = '.ant-card:has-text("Built-in appliances"), ._info_1k7zz_45:has-text("Built-in appliances")'

        # Счетчик просмотров
        WATCHING_COUNT = '.ant-card:has-text("watching now"), ._info_1k7zz_45:has-text("watching now")'

