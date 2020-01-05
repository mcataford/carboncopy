import pytest

def assert_captured_output_matches_snapshot(capsys, snapshot): 
    captured_out = capsys.readouterr()

    assert captured_out.out == snapshot
    assert captured_out.err == snapshot
