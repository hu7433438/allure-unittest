import allure_commons
from allure_commons.model2 import TestResult, TestStepResult, Label, Parameter, TestAfterResult
from allure_commons.reporter import AllureReporter
from allure_commons.types import AttachmentType, ParameterMode
from allure_commons.utils import now, uuid4, represent

from .utils import get_status, get_status_details


class Listener:
    def __init__(self):
        self.allure_reporter = AllureReporter()

    @allure_commons.hookimpl(tryfirst=True)
    def start_step(self, uuid, title, params):
        parameters = [Parameter(name=name, value=value) for name, value in params.items()]
        step = TestStepResult(name=title, start=now(), parameters=parameters)
        self.allure_reporter.start_step(None, uuid, step)

    @allure_commons.hookimpl
    def stop_step(self, uuid, exc_type, exc_val, exc_tb):
        self.allure_reporter.stop_step(uuid,
                                       stop=now(),
                                       status=get_status(exc_val),
                                       statusDetails=get_status_details(exc_type, exc_val, exc_tb))

    @allure_commons.hookimpl
    def start_fixture(self, parent_uuid, uuid, name):
        after_fixture = TestAfterResult(name=name, start=now())
        self.allure_reporter.start_after_fixture(parent_uuid, uuid, after_fixture)

    @allure_commons.hookimpl
    def stop_fixture(self, parent_uuid, uuid, name, exc_type, exc_val, exc_tb):
        self.allure_reporter.stop_after_fixture(uuid,
                                                stop=now(),
                                                status=get_status(exc_val),
                                                statusDetails=get_status_details(exc_type, exc_val, exc_tb))

    @allure_commons.hookimpl
    def attach_data(self, body, name='log', attachment_type=AttachmentType.TEXT, extension=None):
        self.allure_reporter.attach_data(uuid4(), body, name=name, attachment_type=attachment_type, extension=extension)

    @allure_commons.hookimpl
    def attach_file(self, source, name='log', attachment_type=AttachmentType.TEXT, extension=None):
        self.allure_reporter.attach_file(uuid4(), source, name=name, attachment_type=attachment_type, extension=extension)

    @allure_commons.hookimpl
    def add_title(self, test_title):
        test_result = self.allure_reporter.get_test(None)
        if test_result:
            test_result.name = test_title

    @allure_commons.hookimpl
    def add_description(self, test_description):
        test_result = self.allure_reporter.get_test(None)
        if test_result:
            test_result.description = test_description

    @allure_commons.hookimpl
    def add_description_html(self, test_description_html):
        test_result = self.allure_reporter.get_test(None)
        if test_result:
            test_result.descriptionHtml = test_description_html

    @allure_commons.hookimpl
    def add_label(self, label_type, labels):
        test_result = self.allure_reporter.get_test(None)
        for label in labels if test_result else ():
            test_result.labels.append(Label(label_type, label))

    @allure_commons.hookimpl
    def add_parameter(self, name, value, excluded, mode: ParameterMode):
        test_result: TestResult = self.allure_reporter.get_test(None)
        existing_param = next(filter(lambda x: x.name == name, test_result.parameters), None)
        if existing_param:
            existing_param.value = represent(value)
        else:
            test_result.parameters.append(
                Parameter(
                    name=name,
                    value=represent(value),
                    excluded=excluded or None,
                    mode=mode.value if mode else None
                )
            )
