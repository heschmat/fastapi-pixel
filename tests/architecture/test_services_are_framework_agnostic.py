""" 
Test to ensure that services are framework-agnostic.
Services should not depend on FastAPI or any specific web framework.
"""

import pathlib

SERVICE_PATH = pathlib.Path("app/services")

FORBIDDEN_IMPORTS = (
    "fastapi",
    "Depends",
)


def test_services_do_not_depend_on_fastapi():
    """ Services must not import FastAPI or Depends. services stay business-focused. """
    for file in SERVICE_PATH.rglob("*.py"):
        content = file.read_text()

        for forbidden in FORBIDDEN_IMPORTS:
            assert forbidden not in content, (
                f"{file} depends on FastAPI ({forbidden})"
            )
