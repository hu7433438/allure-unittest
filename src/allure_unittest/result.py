from unittest import TestResult as _UnitTestResult

from allure_commons import plugin_manager
from allure_commons.logger import AllureFileLogger
from allure_commons.model2 import TestResult, Label
from allure_commons.reporter import AllureReporter
from allure_commons.types import LabelType
from allure_commons.utils import now, uuid4

from .listener import Listener
from .utils import get_outcome_status, get_outcome_status_details


class Result(_UnitTestResult):

    def __init__(self, report_source_path):
        super(Result, self).__init__()
        self.report_source_path = report_source_path
        self.listener = Listener()
        plugin_manager.register(self.listener)
        plugin_manager.register(AllureFileLogger(self.report_source_path))
        self.allure_reporter = AllureReporter()
        self.test_result = None
        self.allure_results = []

    def schedule_test(self, name, history=None) -> TestResult:
        uuid = uuid4()
        if history:
            test_result = TestResult(name=name, uuid=uuid, historyId=history, start=now())
        else:
            test_result = TestResult(name=name, uuid=uuid, start=now())
        self.allure_reporter.schedule_test(test_result.uuid, test_result)
        return test_result

    def add_test_result(self, test):
        if hasattr(test, '_testMethodName'):
            test_method = getattr(test, '_testMethodName')
            test_class = test.__class__.__qualname__
            test_module = test.__module__
        else:
            test_split_str = test.description.replace(' (', '.').replace(')', '').split('.', 1)
            test_method = test_split_str[0]
            test_class_str = test_split_str[1].rsplit('.', 1)
            test_class = test_class_str[1]
            test_module = test_class_str[0]

        self.test_result = self.schedule_test(f"{test_class}.{test_method}")
        self.allure_results.append(self.test_result.uuid)
        suites = test_module.split('.')[1:]
        suite_num = len(suites)
        for index, label_type in enumerate([LabelType.PARENT_SUITE, LabelType.SUITE, LabelType.SUB_SUITE]):
            if index + 1 > suite_num:
                break
            if index == 2 and suite_num > 3:
                self.test_result.labels.append(Label(label_type, '.'.join(suites[index:])))
                break
            self.test_result.labels.append(Label(label_type, suites[index]))

    def set_result_status(self, test, err):
        if not hasattr(test, '_testMethodName'):
            self.add_test_result(test)
        self.test_result.status = get_outcome_status(err)
        self.test_result.statusDetails = get_outcome_status_details(err)
        if not hasattr(test, '_testMethodName'):
            self.test_result.stop = now()
            self.allure_reporter.close_test(self.test_result.uuid)

    def startTest(self, test):
        super().startTest(test)
        self.add_test_result(test)
        # self.test_classes.append(f"{test_module}.{test_class}")

    def stopTest(self, test):
        """Called when the given test has been run"""
        if test_method_doc := getattr(test, '_testMethodDoc'):
            self.test_result.description = test_method_doc
        self.test_result.stop = now()
        self.allure_reporter.close_test(self.test_result.uuid)
        super().stopTest(test)

    def addError(self, test, err):
        """Called when an error has occurred. 'err' is a tuple of values as
        returned by sys.exc_info().
        """
        super().addError(test, err)
        self.set_result_status(test, err)

    def addFailure(self, test, err):
        """Called when an error has occurred. 'err' is a tuple of values as
        returned by sys.exc_info()."""
        self.set_result_status(test, err)
        super().addFailure(test, err)

    def addSubTest(self, test, subtest, err):
        """Called at the end of a subtest.
        'err' is None if the subtest ended successfully, otherwise it's a
        tuple of values as returned by sys.exc_info().
        """
        # By default, we don't do anything with successful subtests, but
        # more sophisticated test results might want to record them.
        self.set_result_status(test, err)
        super().addSubTest(test, subtest, err)

    def addSuccess(self, test):
        """Called when a test has completed successfully"""
        self.set_result_status(test, None)

    def addSkip(self, test, reason):
        """Called when a test is skipped."""
        self.set_result_status(test, reason)
        super().addSkip(test, reason)
