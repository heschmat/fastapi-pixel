"""
Test to ensure that repositories do not manage transactions.
Repositories should only mutate the session; transaction finalization
should be handled at the service layer.
"""
import pathlib

REPO_PATH = pathlib.Path("app/repositories")


FORBIDDEN = (
    ".commit(",
    ".rollback(",
    ".refresh(",
)


def test_repositories_do_not_manage_transactions():
    """ Repositories must never manage transactions. """
    for file in REPO_PATH.rglob("*.py"):
        content = file.read_text()

        for token in FORBIDDEN:
            assert token not in content, (
                f"{file} contains forbidden transaction call: {token}"
            )
