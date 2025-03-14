import logging

logger = logging.getLogger("decision_policy_backend")


class CustomFormatter(logging.Formatter):
    def __init__(self, fmt, base_path):
        super().__init__(fmt)
        self.base_path = base_path

    def format(self, record):
        # if the log came from a .py module within `self.base_path`, then log the relative path. # noqa
        if self.base_path in record.pathname:
            record.pathname = (
                record.pathname[record.pathname.rindex(self.base_path):]
            )
        return super().format(record)
