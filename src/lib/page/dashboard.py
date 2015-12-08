# Copyright (C) 2015 Google Inc., authors, and contributors <see AUTHORS file>
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
# Created By: jernej@reciprocitylabs.com
# Maintained By: jernej@reciprocitylabs.com

from lib import constants, environment
from lib.page import widget_bar, header


class DashboardPage(widget_bar.WidgetBarPage, header.HeaderPage):
    URL = environment.APP_URL + constants.url.DASHBOARD

    def __init__(self, driver):
        super(DashboardPage, self).__init__(driver)
