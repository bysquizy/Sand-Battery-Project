"""Stage 1 release contract: version, safe development and unchanged runtime stack."""
from __future__ import annotations

import json
from pathlib import Path
import tomllib

from project_version import APP_VERSION, APP_VERSION_LABEL

ROOT = Path(__file__).resolve().parents[1]


def test_project_version_metadata_agree():
    project = tomllib.loads((ROOT / "pyproject.toml").read_text(encoding="utf-8"))
    assert project["project"]["version"] == APP_VERSION
    assert project["project"]["requires-python"] == ">=3.13,<3.14"
    assert APP_VERSION_LABEL == "v2.1.0"
    assert APP_VERSION_LABEL.split(".")[0] in (ROOT / "README.md").read_text(encoding="utf-8")
    assert f'version: "{APP_VERSION}"' in (ROOT / "CITATION.cff").read_text(encoding="utf-8")


def test_devcontainer_never_disables_browser_security():
    source = (ROOT / ".devcontainer/devcontainer.json").read_text(encoding="utf-8")
    config = json.loads(source)
    assert "3.13" in config["image"]
    assert "requirements-dev.txt" in config["postCreateCommand"]
    for unsafe in ("enableCORS false", "enableXsrfProtection false", "apt upgrade", "pip3 install --user streamlit"):
        assert unsafe not in source


def test_current_security_and_verification_docs_are_not_alpha():
    security = (ROOT / ".github/SECURITY.md").read_text(encoding="utf-8")
    validation = (ROOT / "docs/MODEL_VALIDATION.md").read_text(encoding="utf-8")
    assert "2.1.x" in security
    assert "1.0 alpha" not in security
    assert "23 tests passed" not in validation
    assert "Numerical consistency is not experimental validation" in validation


def test_cloud_dependency_stack_is_unchanged():
    original = {
        "streamlit",
        "numpy",
        "scipy",
        "plotly",
        "pandas",
    }
    requirements = (ROOT / "requirements.txt").read_text(encoding="utf-8").strip().splitlines()
    assert len(requirements) == 5
    assert {line.split(">=")[0].strip() for line in requirements} == original


def test_uploaded_scenarios_record_single_source_version():
    home = (ROOT / "home_app.py").read_text(encoding="utf-8")
    assert "from project_version import APP_VERSION, APP_VERSION_LABEL" in home
    assert "payload={'version':APP_VERSION" in home
    assert "v1.2 Engineering Workspace" not in home
