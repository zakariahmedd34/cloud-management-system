"""
Simple Integration Tests for Main Menu
Tests basic functionality of menu and workflows
"""

import unittest
from unittest.mock import patch, MagicMock
import docker_manager
import vm_manager


class TestMainMenuBasic(unittest.TestCase):
    """Simple tests for menu workflows"""

    def test_docker_list_images(self):
        """Test: Docker list images option works"""
        with patch('docker_manager.subprocess.run') as mock_run:
            with patch.object(docker_manager, 'check_docker_running', return_value=True):
                docker_manager.list_images()
                mock_run.assert_called_once()

    def test_docker_search_dockerhub(self):
        """Test: Docker search DockerHub option works"""
        with patch('builtins.input', return_value="nginx"):
            with patch('docker_manager.subprocess.run') as mock_run:
                docker_manager.search_dockerhub()
                mock_run.assert_called_once()

    def test_docker_pull_image(self):
        """Test: Docker pull image option works"""
        with patch('builtins.input', return_value="nginx"):
            with patch('docker_manager.subprocess.run') as mock_run:
                with patch.object(docker_manager, 'check_docker_running', return_value=True):
                    mock_run.return_value = MagicMock(returncode=0, stdout="Pulled", stderr="")
                    docker_manager.pull_image()
                    self.assertTrue(mock_run.called)

    def test_docker_run_container(self):
        """Test: Docker run image option works"""
        with patch('builtins.input', side_effect=["nginx", "web"]):
            with patch('docker_manager.subprocess.run') as mock_run:
                with patch.object(docker_manager, 'check_docker_running', return_value=True):
                    mock_run.return_value = MagicMock(returncode=0, stdout="container123", stderr="")
                    docker_manager.run_image()
                    self.assertTrue(mock_run.called)

    def test_docker_list_running_containers(self):
        """Test: Docker list running containers option works"""
        with patch('docker_manager.subprocess.run') as mock_run:
            with patch.object(docker_manager, 'check_docker_running', return_value=True):
                docker_manager.list_running_containers()
                mock_run.assert_called_once()

    def test_docker_list_all_containers(self):
        """Test: Docker list all containers option works"""
        with patch('docker_manager.subprocess.run') as mock_run:
            with patch.object(docker_manager, 'check_docker_running', return_value=True):
                docker_manager.list_all_containers()
                mock_run.assert_called_once()

    def test_docker_create_dockerfile(self):
        """Test: Docker create Dockerfile option works"""
        with patch('builtins.input', side_effect=["Dockerfile", "1", "python:3.9", "python app.py"]):
            with patch('os.path.exists', return_value=False):
                with patch('os.path.dirname', return_value=''):
                    with patch('builtins.open', create=True):
                        docker_manager.create_dockerfile()

    def test_docker_build_image(self):
        """Test: Docker build image option works"""
        with patch('builtins.input', side_effect=["Dockerfile", "app:1.0"]):
            with patch('os.path.exists', return_value=True):
                with patch('docker_manager.subprocess.run') as mock_run:
                    with patch.object(docker_manager, 'check_docker_running', return_value=True):
                        mock_run.return_value = MagicMock(returncode=0, stdout="Built", stderr="")
                        docker_manager.build_image()
                        self.assertTrue(mock_run.called)

    def test_docker_stop_container(self):
        """Test: Docker stop container option works"""
        with patch('builtins.input', side_effect=["container123"]):
            with patch('docker_manager.subprocess.run') as mock_run:
                with patch.object(docker_manager, 'check_docker_running', return_value=True):
                    mock_run.return_value = MagicMock(returncode=0, stdout="Stopped", stderr="")
                    docker_manager.stop_container()
                    self.assertTrue(mock_run.called)

    def test_docker_start_container(self):
        """Test: Docker start container option works"""
        with patch('builtins.input', return_value="container123"):
            with patch('docker_manager.subprocess.run') as mock_run:
                with patch.object(docker_manager, 'check_docker_running', return_value=True):
                    mock_run.side_effect = [
                        MagicMock(returncode=0, stdout="container123\t", stderr=""),
                        MagicMock(returncode=0, stdout="Started", stderr="")
                    ]
                    docker_manager.start_container()
                    self.assertTrue(mock_run.called)

    def test_docker_search_local_images(self):
        """Test: Docker search local images option works"""
        with patch('builtins.input', return_value="nginx"):
            with patch('docker_manager.subprocess.run') as mock_run:
                with patch.object(docker_manager, 'check_docker_running', return_value=True):
                    mock_run.return_value = MagicMock(returncode=0, stdout="nginx:latest\timg123\t250MB", stderr="")
                    docker_manager.search_local_images()
                    self.assertTrue(mock_run.called)

    def test_vm_create_interactive(self):
        """Test: VM create interactive option works"""
        with patch('builtins.input', side_effect=["ubuntu-vm", "2048", "2", "20G"]):
            with patch('os.path.exists', return_value=False):
                with patch('subprocess.run') as mock_run:
                    vm_manager.create_vm()
                    self.assertEqual(mock_run.call_count, 2)

    def test_vm_create_from_config(self):
        """Test: VM create from config option works"""
        import json
        config = {"name": "testvm", "ram": "2048", "cpu": "2", "disk": "20G"}
        with patch('builtins.input', return_value="./config.json"):
            with patch('os.path.exists', side_effect=[True, False]):  # file exists, disk doesn't
                with patch('builtins.open', create=True) as mock_file:
                    mock_file.return_value.__enter__.return_value.read.return_value = json.dumps(config)
                    with patch('subprocess.run') as mock_run:
                        vm_manager.create_vm_from_config()
                        self.assertEqual(mock_run.call_count, 2)

    def test_vm_list(self):
        """Test: VM list option works"""
        with patch('os.listdir', return_value=["ubuntu.qcow2", "debian.qcow2"]):
            vm_manager.list_vms()

    def test_vm_delete(self):
        """Test: VM delete option works"""
        with patch('builtins.input', side_effect=["testvm", "y"]):
            with patch('os.path.exists', return_value=True):
                with patch('os.remove') as mock_remove:
                    vm_manager.delete_vm()
                    mock_remove.assert_called_once()

    def test_error_handling_no_docker_daemon(self):
        """Test: System handles Docker daemon not running"""
        with patch.object(docker_manager, 'check_docker_running', return_value=False):
            docker_manager.list_images()

    def test_error_handling_empty_input(self):
        """Test: System handles empty user input"""
        with patch('builtins.input', return_value=""):
            with patch('docker_manager.subprocess.run') as mock_run:
                docker_manager.search_dockerhub()
                mock_run.assert_not_called()


if __name__ == '__main__':
    unittest.main(verbosity=2)
