# Copyright (C) 2015 Google Inc., authors, and contributors <see AUTHORS file>
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
# Created By: jernej@reciprocitylabs.com
# Maintained By: jernej@reciprocitylabs.com

from lib import decorator, exception, constants


class DecoratePublicMethods(type):
    # todo: this should be refactored to DecorateMethods and used with a factory
    """
    Decorates all test methods with a decorator that makes a screenshot on
    any exception.
    """
    def __new__(mcs, name, bases, dct):
        for attr_name, value in dct.items():
            if all([name in attr_name for name in [
                constants.test_runner.TEST_METHOD_PREFIX,
                constants.test_runner.TEST_METHOD_POSTFIX]
                    ]) \
                    and callable(value):
                dct[attr_name] = decorator.take_screenshot_on_error(value)

        return super(DecoratePublicMethods, mcs).__new__(mcs, name, bases, dct)


class RequireDocs(type):
    """
    Requires from all methods to include docstrings.
    """
    def __new__(mcs, name, bases, dct):
        for attr_name, value in dct.items():
            if callable(value) and not hasattr(value, "__doc__"):
                raise exception.DocstringsMissing(attr_name)

        return super(RequireDocs, mcs).__new__(mcs, name, bases, dct)
