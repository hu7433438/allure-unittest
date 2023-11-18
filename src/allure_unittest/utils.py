from allure_commons.model2 import Status
from allure_commons.model2 import StatusDetails
from allure_commons.utils import format_exception, format_traceback


def get_outcome_status(outcome):
    if isinstance(outcome, str):
        return Status.SKIPPED
    _, exception, _ = outcome or (None, None, None)
    return get_status(exception)


def get_outcome_status_details(outcome):
    if isinstance(outcome, str):
        return StatusDetails(message=outcome)
    exception_type, exception, exception_traceback = outcome or (None, None, None)
    return get_status_details(exception_type, exception, exception_traceback)


def get_status(exception):
    if exception:
        if isinstance(exception, AssertionError):
            return Status.FAILED
        return Status.BROKEN
    else:
        return Status.PASSED


def get_status_details(exception_type, exception, exception_traceback):
    message = format_exception(exception_type, exception)
    trace = format_traceback(exception_traceback)
    return StatusDetails(message=message, trace=trace) if message or trace else None
