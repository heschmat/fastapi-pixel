import pathlib

CORE_PATH = pathlib.Path("app/core")


def test_core_has_no_upward_dependencies():
    for file in CORE_PATH.rglob("*.py"):
        content = file.read_text()

        assert "services" not in content
        assert "routers" not in content

