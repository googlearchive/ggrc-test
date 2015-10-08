from lib import constants
from lib.page import widget_bar, header


class DashboardPage(widget_bar.WidgetBarPage, header.HeaderPage):
    def navigate_to(self):
        self._driver.get(constants.uri.BASE + constants.uri.DASHBOARD)
