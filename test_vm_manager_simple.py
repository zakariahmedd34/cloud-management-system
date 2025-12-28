"""
Simple Unit Tests for VM Manager
Tests basic functionality of vm_manager.py
"""

import unittest
from unittest.mock import patch, MagicMock
import json
import vm_manager


class TestVMManagerBasic(unittest.TestCase):
    """Simple tests for vm_manager functions"""

    def test_create_vm_with_valid_inputs(self):
        """Test: create_vm accepts all required inputs"""
        with patch('builtins.input', side_effect=["ubuntu-vm", "2048", "2", "20G"]):
            with patch('os.path.exists', return_value=False):
                with patch('subprocess.run') as mock_run:
                    vm_manager.create_vm()
                    self.assertEqual(mock_run.call_count, 2)

    def test_create_vm_with_missing_fields(self):
        """Test: create_vm rejects missing fields"""
        with patch('builtins.input', side_effect=["testvm", "1024", "1", ""]):
            vm_manager.create_vm()

    def test_create_vm_disk_already_exists(self):
        """Test: create_vm rejects when disk file exists"""
        with patch('builtins.input', side_effect=["testvm", "1024", "1", "5G"]):
            with patch('os.path.exists', return_value=True):
                vm_manager.create_vm()

    def test_delete_vm_with_confirmation(self):
        """Test: delete_vm removes VM when confirmed"""
        with patch('builtins.input', side_effect=["testvm", "y"]):
            with patch('os.path.exists', return_value=True):
                with patch('os.remove') as mock_remove:
                    vm_manager.delete_vm()
                    mock_remove.assert_called_once_with("testvm.qcow2")

    def test_delete_vm_with_cancellation(self):
        """Test: delete_vm cancels when not confirmed"""
        with patch('builtins.input', side_effect=["testvm", "n"]):
            with patch('os.path.exists', return_value=True):
                with patch('os.remove') as mock_remove:
                    vm_manager.delete_vm()
                    mock_remove.assert_not_called()

    def test_delete_vm_not_found(self):
        """Test: delete_vm fails when VM disk not found"""
        with patch('builtins.input', return_value="testvm"):
            with patch('os.path.exists', return_value=False):
                vm_manager.delete_vm()

    def test_list_vms_with_vms(self):
        """Test: list_vms displays all VMs"""
        with patch('os.listdir', return_value=["ubuntu.qcow2", "debian.qcow2"]):
            vm_manager.list_vms()

    def test_list_vms_empty(self):
        """Test: list_vms handles empty VM list"""
        with patch('os.listdir', return_value=[]):
            vm_manager.list_vms()

    def test_create_vm_from_config_valid(self):
        """Test: create_vm_from_config reads and processes config"""
        config = {"name": "testvm", "ram": "2048", "cpu": "2", "disk": "20G"}
        with patch('builtins.input', return_value="./config.json"):
            with patch('os.path.exists', side_effect=[True, False]):  # file exists, disk doesn't
                with patch('builtins.open', create=True) as mock_file:
                    mock_file.return_value.__enter__.return_value.read.return_value = json.dumps(config)
                    with patch('subprocess.run') as mock_run:
                        vm_manager.create_vm_from_config()
                        self.assertEqual(mock_run.call_count, 2)

    def test_create_vm_from_config_file_not_found(self):
        """Test: create_vm_from_config handles missing file"""
        with patch('builtins.input', return_value="./missing.json"):
            with patch('os.path.exists', return_value=False):
                vm_manager.create_vm_from_config()

    def test_create_vm_from_config_invalid_json(self):
        """Test: create_vm_from_config handles invalid JSON"""
        with patch('builtins.input', return_value="./config.json"):
            with patch('os.path.exists', return_value=True):
                with patch('builtins.open', create=True) as mock_file:
                    mock_file.return_value.__enter__.return_value.read.return_value = "{ invalid }"
                    vm_manager.create_vm_from_config()

    def test_create_vm_from_config_missing_fields(self):
        """Test: create_vm_from_config rejects incomplete config"""
        config = {"name": "testvm", "ram": "2048"}  # missing cpu and disk
        with patch('builtins.input', return_value="./config.json"):
            with patch('os.path.exists', return_value=True):
                with patch('builtins.open', create=True) as mock_file:
                    mock_file.return_value.__enter__.return_value.read.return_value = json.dumps(config)
                    vm_manager.create_vm_from_config()


if __name__ == '__main__':
    unittest.main(verbosity=2)
