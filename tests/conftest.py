# Copyright 2026 XMOS LIMITED.
# This Software is subject to the terms of the XMOS Public Licence: Version 1.
import pytest

@pytest.fixture
def level(request):
    return request.config.getoption("--level")

def pytest_addoption(parser):
    parser.addoption(
        "--level",
        action="store",
        default="smoke",
        choices=["smoke", "default", "extended"],
        help="Test coverage level",
    )
