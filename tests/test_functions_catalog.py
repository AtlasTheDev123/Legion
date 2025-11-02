import json
import pathlib

def test_functions_count_matches_count_file():
    root = pathlib.Path(__file__).resolve().parents[1]
    functions_file = root / "schemas" / "functions.json"
    count_file = root / "schemas" / "functions_count.txt"

    assert functions_file.exists(), f"Missing {functions_file}"
    assert count_file.exists(), f"Missing {count_file}"

    # handle potential BOM with utf-8-sig
    funcs = json.loads(functions_file.read_text(encoding='utf-8-sig'))
    cnt = int(count_file.read_text(encoding='utf-8').strip())

    assert isinstance(funcs, list), "functions.json must be an array"
    assert len(funcs) == cnt, f"functions.json contains {len(funcs)} entries but {count_file} says {cnt}"
