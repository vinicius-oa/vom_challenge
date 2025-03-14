from domain.config_backend.controllers.schemas.request.config_backend import (
    ConfigBackendCreatePolicyRequestPolicyFlow
)

list_valid_policy_flow = [
    {
        "policy_flow": {
            "block_type": "start",
            "block_targets": [
                {
                    "block_type": "condition",
                    "variable_operator": ">",
                    "variable_name": "age",
                    "variable_value": 18,
                    "block_targets": [
                        {
                            "block_type": "end",
                            "flow": False,
                            "output": 0
                        },
                        {
                            "block_type": "condition",
                            "variable_operator": ">",
                            "variable_name": "income",
                            "variable_value": 1000,
                            "flow": True,
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
            ]
        }
    },
    {
        "policy_flow": {
            "block_type": "start",
            "block_targets": [
                {
                    "block_type": "condition",
                    "variable_operator": ">",
                    "variable_name": "age",
                    "variable_value": 18,
                    "block_targets": [
                        {
                            "block_type": "condition",
                            "variable_operator": ">",
                            "variable_name": "parent_years",
                            "variable_value": "50",
                            "flow": False,
                            "block_targets": [
                                {
                                    "block_type": "condition",
                                    "variable_operator": ">",
                                    "variable_name": "cousin_years",
                                    "variable_value": "50",
                                    "flow": False,
                                    "block_targets": [
                                        {
                                            "block_type": "end",
                                            "flow": False,
                                            "output": 1
                                        },
                                        {
                                            "block_type": "end",
                                            "flow": True,
                                            "output": 2
                                        }
                                    ]
                                },
                                {
                                    "block_type": "condition",
                                    "variable_operator": ">",
                                    "variable_name": "grandparent_years",
                                    "variable_value": "50",
                                    "flow": True,
                                    "block_targets": [
                                        {
                                            "block_type": "end",
                                            "flow": False,
                                            "output": 5
                                        },
                                        {
                                            "block_type": "end",
                                            "flow": True,
                                            "output": 6
                                        }
                                    ]
                                }
                            ]
                        },
                        {
                            "block_type": "condition",
                            "variable_operator": ">",
                            "variable_name": "income",
                            "variable_value": 1000,
                            "flow": True,
                            "block_targets": [
                                {
                                    "block_type": "end",
                                    "flow": False,
                                    "output": 3
                                },
                                {
                                    "block_type": "end",
                                    "flow": True,
                                    "output": 4
                                }
                            ]
                        }
                    ]
                }
            ]
        }
    },
    {
        "policy_flow": {
            "block_type": "start",
            "block_targets": [
                {
                    "block_type": "condition",
                    "variable_operator": ">",
                    "variable_name": "age",
                    "variable_value": 18,
                    "block_targets": [
                        {
                            "block_type": "condition",
                            "variable_operator": ">",
                            "variable_name": "parent_years",
                            "variable_value": 50,
                            "block_targets": [
                                {
                                    "block_type": "end",
                                    "flow": False,
                                    "output": 1
                                },
                                {
                                    "block_type": "end",
                                    "flow": True,
                                    "output": 2
                                }
                            ],
                            "flow": False
                        },
                        {
                            "block_type": "condition",
                            "variable_operator": ">",
                            "variable_name": "income",
                            "variable_value": 1000,
                            "block_targets": [
                                {
                                    "block_type": "end",
                                    "flow": False,
                                    "output": 3
                                },
                                {
                                    "block_type": "end",
                                    "flow": True,
                                    "output": 4
                                }
                            ],
                            "flow": True
                        }
                    ]
                }
            ]
        }
    },
    {
        "policy_flow": {
            "block_type": "start",
            "block_targets": [
                {
                    "block_type": "condition",
                    "variable_operator": ">",
                    "variable_name": "age",
                    "variable_value": 18,
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
]
list_valid_policy_flow_parsed = [
    ConfigBackendCreatePolicyRequestPolicyFlow(**x["policy_flow"])
    for x in list_valid_policy_flow
]

list_invalid_policy_flow = [
    {
        "expected_exception": "start_block_1",
        "policy_flow": {
            "block_type": "end",
            "block_targets": [
                {
                    "block_type": "condition",
                    "variable_operator": ">",
                    "variable_name": "age",
                    "variable_value": 18,
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
    },
    {
        "expected_exception": "start_block_2",
        "policy_flow": {
            "block_type": "start",
            "block_targets": [
                {
                    "block_type": "condition",
                    "variable_operator": ">",
                    "variable_name": "age",
                    "variable_value": 18,
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
                },
                {
                    "block_type": "condition",
                    "variable_operator": ">",
                    "variable_name": "age",
                    "variable_value": 18,
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
    },
    {
        "expected_exception": "start_block_3",
        "policy_flow": {
            "block_type": "start",
            "block_targets": [
                {
                    "block_type": "end",
                    "variable_operator": ">",
                    "variable_name": "age",
                    "variable_value": 18,
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
    },
    {
        "expected_exception": "block_targets_property",
        "policy_flow": {
            "block_type": "start",
            "block_targets": [
                {
                    "block_type": "condition",
                    "variable_operator": ">",
                    "variable_name": "age",
                    "variable_value": 18,
                    "block_targets": [
                        {
                            "block_type": "start",
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
    },
    {
        "expected_exception": "variable_name_property",
        "policy_flow": {
            "block_type": "start",
            "block_targets": [
                {
                    "block_type": "condition",
                    "variable_operator": ">",
                    "variable_name": "age",
                    "variable_value": 18,
                    "block_targets": [
                        {
                            "block_type": "end",
                            "flow": False,
                            "output": 0
                        },
                        {
                            "block_type": "condition",
                            "variable_operator": ">",
                            "variable_name": "age",
                            "variable_value": 1000,
                            "flow": True,
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
            ]
        }
    },
    {
        "expected_exception": "condition_block_required_properties",
        "policy_flow": {
            "block_type": "start",
            "block_targets": [
                {
                    "block_type": "condition",
                    "variable_operator": ">",
                    "variable_value": 18,
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
    },
    {
        "expected_exception": "condition_block_blocks_target_property",
        "policy_flow": {
            "block_type": "start",
            "block_targets": [
                {
                    "block_type": "condition",
                    "variable_operator": ">",
                    "variable_name": "age",
                    "variable_value": 18,
                    "block_targets": [
                        {
                            "block_type": "end",
                            "flow": False,
                            "output": 0
                        }
                    ]
                }
            ]
        }
    },
    {
        "expected_exception": "condition_block_flow_property",
        "policy_flow": {
            "block_type": "start",
            "block_targets": [
                {
                    "flow": True,
                    "block_type": "condition",
                    "variable_operator": ">",
                    "variable_name": "age",
                    "variable_value": 18,
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
    },
    {
        "expected_exception": "condition_block_flow_property_value",
        "policy_flow": {
            "block_type": "start",
            "block_targets": [
                {
                    "block_type": "condition",
                    "variable_operator": ">",
                    "variable_name": "age",
                    "variable_value": 18,
                    "block_targets": [
                        {
                            "block_type": "end",
                            "flow": False,
                            "output": 0
                        },
                        {
                            "block_type": "end",
                            "flow": False,
                            "output": 1000
                        }
                    ]
                }
            ]
        }
    },
    {
        "expected_exception": "end_block_required_properties",
        "policy_flow": {
            "block_type": "start",
            "block_targets": [
                {
                    "block_type": "condition",
                    "variable_operator": ">",
                    "variable_name": "age",
                    "variable_value": 18,
                    "block_targets": [
                        {
                            "block_type": "end",
                            "flow": False,
                            "output": 0
                        },
                        {
                            "block_type": "end",
                            "flow": True,
                        }
                    ]
                }
            ]
        }
    },
]
