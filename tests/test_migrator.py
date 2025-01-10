import pytest
from migrator_tool.migrator_tool import DatabaseMigratorApp
import customtkinter as ctk

@pytest.fixture
def app():
    """Fixture to set up the DatabaseMigratorApp for tests."""
    root = ctk.CTk()
    app = DatabaseMigratorApp(root)
    yield app  # Provide the app to tests
    root.destroy()  # Clean up after tests

def test_initial_status(app):
    """Test that the initial status label text is correct."""
    assert app.status_label.cget("text") == "Status: Ready"

def test_update_status(app):
    """Test that the update_status method correctly updates the status label."""
    app.update_status("Testing status")
    assert app.status_label.cget("text") == "Status: Testing status"
