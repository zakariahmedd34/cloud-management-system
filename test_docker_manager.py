"""
Simple Unit Tests for Docker Manager
Tests basic functionality of docker_manager.py
"""

import unittest
from unittest.mock import patch, MagicMock
import docker_manager


class TestDockerManagerBasic(unittest.TestCase):
    """Simple tests for docker_manager functions"""

    def test_check_docker_running_when_available(self):
        """Test: check_docker_running returns True when Docker is available"""
        with patch('docker_manager.subprocess.run') as mock_run:
            mock_run.return_value = MagicMock(returncode=0)
            result = docker_manager.check_docker_running()
            self.assertTrue(result)

    def test_check_docker_running_when_unavailable(self):
        """Test: check_docker_running returns False when Docker is unavailable"""
        with patch('docker_manager.subprocess.run') as mock_run:
            mock_run.side_effect = FileNotFoundError()
            result = docker_manager.check_docker_running()
            self.assertFalse(result)

    def test_list_images_calls_docker(self):
        """Test: list_images calls docker images command"""
        with patch('docker_manager.subprocess.run') as mock_run:
            with patch.object(docker_manager, 'check_docker_running', return_value=True):
                docker_manager.list_images()
                mock_run.assert_called_once_with(["docker", "images"])

    def test_list_running_containers_calls_docker(self):
        """Test: list_running_containers calls docker ps command"""
        with patch('docker_manager.subprocess.run') as mock_run:
            with patch.object(docker_manager, 'check_docker_running', return_value=True):
                docker_manager.list_running_containers()
                mock_run.assert_called_once_with(["docker", "ps"])

    def test_list_all_containers_calls_docker(self):
        """Test: list_all_containers calls docker ps -a command"""
        with patch('docker_manager.subprocess.run') as mock_run:
            with patch.object(docker_manager, 'check_docker_running', return_value=True):
                docker_manager.list_all_containers()
                mock_run.assert_called_once_with(["docker", "ps", "-a"])

    def test_run_image_with_valid_input(self):
        """Test: run_image accepts image name and creates container"""
        with patch('builtins.input', side_effect=["nginx", ""]):
            with patch('docker_manager.subprocess.run') as mock_run:
                with patch.object(docker_manager, 'check_docker_running', return_value=True):
                    mock_run.return_value = MagicMock(returncode=0, stdout="container123", stderr="")
                    docker_manager.run_image()
                    self.assertTrue(mock_run.called)

    def test_run_image_with_empty_name(self):
        """Test: run_image rejects empty image name"""
        with patch('builtins.input', side_effect=[""]):
            with patch.object(docker_manager, 'check_docker_running', return_value=True):
                docker_manager.run_image()

    def test_stop_container_with_valid_input(self):
        """Test: stop_container calls docker stop command"""
        with patch('builtins.input', side_effect=["container123"]):
            with patch('docker_manager.subprocess.run') as mock_run:
                with patch.object(docker_manager, 'check_docker_running', return_value=True):
                    mock_run.return_value = MagicMock(returncode=0, stdout="Stopped", stderr="")
                    docker_manager.stop_container()
                    self.assertTrue(mock_run.called)

    def test_search_dockerhub_with_valid_input(self):
        """Test: search_dockerhub calls docker search command"""
        with patch('builtins.input', return_value="nginx"):
            with patch('docker_manager.subprocess.run') as mock_run:
                docker_manager.search_dockerhub()
                mock_run.assert_called_once()

    def test_search_dockerhub_with_empty_input(self):
        """Test: search_dockerhub rejects empty search term"""
        with patch('builtins.input', return_value=""):
            with patch('docker_manager.subprocess.run') as mock_run:
                docker_manager.search_dockerhub()
                mock_run.assert_not_called()

    def test_pull_image_with_valid_input(self):
        """Test: pull_image calls docker pull command"""
        with patch('builtins.input', return_value="nginx"):
            with patch('docker_manager.subprocess.run') as mock_run:
                with patch.object(docker_manager, 'check_docker_running', return_value=True):
                    mock_run.return_value = MagicMock(returncode=0, stdout="Pulling", stderr="")
                    docker_manager.pull_image()
                    self.assertTrue(mock_run.called)

    def test_search_local_images_with_valid_input(self):
        """Test: search_local_images filters local images"""
        with patch('builtins.input', return_value="nginx"):
            with patch('docker_manager.subprocess.run') as mock_run:
                with patch.object(docker_manager, 'check_docker_running', return_value=True):
                    mock_run.return_value = MagicMock(
                        returncode=0,
                        stdout="nginx:latest\timgid\t250MB",
                        stderr=""
                    )
                    docker_manager.search_local_images()
                    self.assertTrue(mock_run.called)

    def test_build_image_with_valid_inputs(self):
        """Test: build_image calls docker build command"""
        with patch('builtins.input', side_effect=["Dockerfile", "myapp:1.0"]):
            with patch('os.path.exists', return_value=True):
                with patch('docker_manager.subprocess.run') as mock_run:
                    with patch.object(docker_manager, 'check_docker_running', return_value=True):
                        mock_run.return_value = MagicMock(returncode=0, stdout="Built", stderr="")
                        docker_manager.build_image()
                        self.assertTrue(mock_run.called)

    def test_create_dockerfile_creates_file(self):
        """Test: create_dockerfile creates a file"""
        with patch('builtins.input', side_effect=["./Dockerfile", "1", "python:3.9", "python app.py"]):
            with patch('os.path.exists', return_value=False):
                with patch('os.path.dirname', return_value=''):
                    with patch('builtins.open', create=True) as mock_file:
                        docker_manager.create_dockerfile()
                        mock_file.assert_called()

    def test_start_container_with_valid_input(self):
        """Test: start_container calls docker start command"""
        with patch('builtins.input', return_value="container123"):
            with patch('docker_manager.subprocess.run') as mock_run:
                with patch.object(docker_manager, 'check_docker_running', return_value=True):
                    mock_run.side_effect = [
                        MagicMock(returncode=0, stdout="container123\t", stderr=""),
                        MagicMock(returncode=0, stdout="Started", stderr="")
                    ]
                    docker_manager.start_container()
                    self.assertTrue(mock_run.called)


if __name__ == '__main__':
    unittest.main(verbosity=2)
