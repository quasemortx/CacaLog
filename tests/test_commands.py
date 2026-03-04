import pytest
from unittest.mock import MagicMock, patch
from app.commands import handle_command


@pytest.fixture
def mock_sheets():
    sheets = MagicMock()
    sheets.get_all_records.return_value = []
    return sheets


class TestDeletarCommand:
    def test_deletar_valido_encontrado(self, mock_sheets):
        mock_sheets.delete_inventory_item.return_value = True
        resp = handle_command("/deletar", ["S-712"], mock_sheets)
        assert "removido" in resp.lower()
        mock_sheets.delete_inventory_item.assert_called_once_with("S-712")

    def test_deletar_lab_encontrado(self, mock_sheets):
        mock_sheets.delete_inventory_item.return_value = True
        resp = handle_command("/deletar", ["L-03"], mock_sheets)
        assert "removido" in resp.lower()
        mock_sheets.delete_inventory_item.assert_called_once_with("L-03")

    def test_deletar_nao_encontrado(self, mock_sheets):
        mock_sheets.delete_inventory_item.return_value = False
        resp = handle_command("/deletar", ["S-999"], mock_sheets)
        assert "não encontrado" in resp.lower()
        mock_sheets.delete_inventory_item.assert_called_once_with("S-999")

    def test_deletar_id_sem_prefixo(self, mock_sheets):
        resp = handle_command("/deletar", ["712"], mock_sheets)
        assert "inválido" in resp.lower()
        mock_sheets.delete_inventory_item.assert_not_called()

    def test_deletar_sem_args(self, mock_sheets):
        resp = handle_command("/deletar", [], mock_sheets)
        assert "uso:" in resp.lower()
        mock_sheets.delete_inventory_item.assert_not_called()

    def test_deletar_erro_no_sheets(self, mock_sheets):
        mock_sheets.delete_inventory_item.side_effect = Exception("API Error")
        resp = handle_command("/deletar", ["S-712"], mock_sheets)
        assert "erro" in resp.lower()

    def test_deletar_normaliza_lowercase(self, mock_sheets):
        """ID passado em minúsculas deve ser normalizado para maiúsculas."""
        mock_sheets.delete_inventory_item.return_value = True
        resp = handle_command("/deletar", ["s-712"], mock_sheets)
        mock_sheets.delete_inventory_item.assert_called_once_with("S-712")
        assert "removido" in resp.lower()
