# Copyright (C) 2015 Google Inc., authors, and contributors <see AUTHORS file>
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
# Created By: jernej@reciprocitylabs.com
# Maintained By: jernej@reciprocitylabs.com

"""
Utility classes for page objects used in tests.

Details:
Most of the tests require a sequence of primitive methods of the page
object. If the sequence repeats itself among tests, it should be shared in
this module.
"""

import uuid
from lib import base
from lib.constants.test import create_new_program


class LhnMenu(base.Test):
    @staticmethod
    def create_new_program():
        pass


class ModalNewProgramPage(base.Test):
    """Methods for simulating common user actions"""

    @staticmethod
    def enter_test_data(modal):
        """Fills out all fields in the modal

        Args:
            modal (lib.page.modal.new_program.NewProgramModal)
        """
        unique_id = str(uuid.uuid4())

        modal.enter_title(create_new_program.TITLE + unique_id)
        modal.enter_description(
            create_new_program.DESCRIPTION_SHORT)
        modal.enter_notes(
            create_new_program.NOTES_SHORT)
        modal.enter_code(create_new_program.CODE + unique_id)
        modal.filter_and_select_primary_contact("example")
        modal.filter_and_select_secondary_contact("example")
        modal.enter_program_url(
            create_new_program.PROGRAM_URL)
        modal.enter_reference_url(
            create_new_program.REFERENCE_URL)
        modal.enter_effective_date_start_month()
        modal.enter_stop_date_end_month()
