def test_run_core_stub():
    from src.core import function_1 as f
    res = f.run({"task":"test"})
    assert res["status"]=="ok"
