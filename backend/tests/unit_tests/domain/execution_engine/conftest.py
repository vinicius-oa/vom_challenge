import pytest

from config.di import DI


@pytest.fixture(scope="package")
def policy_json():
    yield {
        "id": 1,
        "name": "test",
        "policy_flow": {
            "block_type": "start",
            "block_targets": [
                {
                    "block_type": "condition",
                    "variable_operator": ">",
                    "variable_name": "age",
                    "variable_value": 15,
                    "block_targets": [
                        {
                            "block_type": "end",
                            "flow": False,
                            "output": 0
                        },
                        {
                            "block_type": "end",
                            "flow": True,
                            "output": 1000
                        }
                    ]
                }
            ]
        }
    }


@pytest.fixture(scope="package")
def execution_engine_service(policy_json):
    execution_engine_service = DI.execution_engine_service()
    yield execution_engine_service
