"""
Test to ensure that routers do not import repositories directly.
Routers should interact with services, not repositories.
"""
import pathlib

ROUTER_PATH = pathlib.Path("app/api/routers")


def test_routers_do_not_import_repositories():
    """ Routers must go through services, always."""
    for file in ROUTER_PATH.rglob("*.py"):
        content = file.read_text()

        assert "repositories" not in content, (
            f"{file} imports repositories directly"
        )
