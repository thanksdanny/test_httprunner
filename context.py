# encoding: utf-8

import copy
import os
import re
import sys

from httprunner import exception, testcase, utils
from httprunner.compat import OrderedDict

class Context(object):
    """ Manages context functions and variables.
        context has two levels, testset and testcase.
    """
    def __init__(self):
        self.testcase_shared_valiables_mapping = OrderedDict()
        self.testcase_variable_mapping = OrderedDict()
        self.testcase_parser = testcase.TestcaseParser()
        self.init_context()

    def init_context(self, level='testcase'):
        """
        testset level context initializes when a file is loaded,
        testcase level context initializes when each testcase starts.
        """
        if level == "testcase":
            self.testcase_functions_config = {}
            self.testcase_request_config = {}
            self.testcase_shared_valiables_mapping = OrderedDict()
        # testcase config shall inherit from testset configs,
        # but can not change testset configs, that's why we use copy.deepcopy here.
        self.testcase_functions_config = copy.deepcopy(self.testcase_functions_config)
        self.testcase_variable_mapping = copy.deepcopy(self.testcase_shared_valiables_mapping)

        self.testcase_parser.bind_functions(self.testcase_functions_config)
        self.testcase_parser.update_binded_variables(self.testcase_variable_mapping)

        if level == "testset":
            self.import_module_items(["httprunner.built_in"], "testset")
