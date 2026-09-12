# Copyright 2026 XMOS LIMITED.
# This Software is subject to the terms of the XMOS Public Licence: Version 1.

import subprocess
from pathlib import Path


def test_lib_logging_from_xc():
    test_dir = Path(__file__).parent
    binary = test_dir / "debug_printf_xc_test" / "bin" / "debug_printf_xc_test.xe"
    expected = (test_dir / "test_xc.expect").read_text()

    result = subprocess.run(["xsim", str(binary)], capture_output=True, text=True)

    assert result.returncode == 0
    assert result.stdout == expected
