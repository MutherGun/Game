import builtins
import pytest
from rooms.start_room import StartRoom
from rooms.hallway import Hallway

@pytest.fixture
def mock_print(monkeypatch):
    printed = []
    monkeypatch.setattr(builtins, "print", lambda msg: printed.append(msg))
    return printed

def test_get_description_contains_expected_text():
    room = StartRoom()
    description = room.get_description()
    assert "Nacházíš se v temné cele" in description["text"]

def test_handle_command_vyjdi_ven_returns_hallway(mock_print):
    room = StartRoom()
    result = room.handle_command("vyjdi ven")
    assert isinstance(result, Hallway)
    assert any("otevíráš dveře" in line for line in mock_print)

def test_handle_command_porozhlednout_prints_description_and_returns_none(mock_print):
    room = StartRoom()
    result = room.handle_command("porozhlednout")
    assert result is None
    assert any("zrezivělý zámek" in line for line in mock_print)

def test_handle_command_unknown_returns_none_and_prints_error(mock_print):
    room = StartRoom()
    result = room.handle_command("neexistujici prikaz")
    assert result is None
    assert any("Nerozumím tomuto příkazu" in line for line in mock_print)
