"""
Test to ensure that services do not handle IntegrityError directly.
Services should use a translator utility to convert database errors
into application-specific exceptions.
"""
import pathlib

SERVICE_PATH = pathlib.Path("app/services")


def test_services_do_not_catch_integrity_error_directly():
    for file in SERVICE_PATH.rglob("*.py"):
        content = file.read_text()

        assert "IntegrityError" not in content, (
            f"{file} handles IntegrityError directly — use translator"
        )
