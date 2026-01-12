# Copyright 2015-2026 XMOS LIMITED.
# This Software is subject to the terms of the XMOS Public Licence: Version 1.

import subprocess
from pathlib import Path

test_path = Path(__file__).parent
bin_path = test_path / "debug_printf_test/bin/debug_printf_test.xe"
expect_path = test_path / "test.expect"
out_path = test_path / "test.out"

assert bin_path.exists(), f"Test binary not found at {bin_path}"
assert expect_path.exists(), f"Expect file not found at {expect_path}"

def test_lib_logging():
    cmd_xsim = ["xsim", str(bin_path)]
    ret = subprocess.run(cmd_xsim, capture_output=True, text=True)
    expected_text = expect_path.read_text()
    out_path.write_bytes(ret.stdout.encode())
    assert ret.stdout == expected_text
