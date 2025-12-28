 # Simple Unit Tests for Docker Manager
 # Tests basic functionality of docker_manager.py

import unittest
from unittest.mock import patch, MagicMock
import docker_manager


class TestDockerManagerBasic(unittest.TestCase):


    def testCheckDockerRunningWhenAvailable(self):

        with patch('docker_manager.subprocess.run') as mock_run:
            mock_run.return_value = MagicMock(returncode=0)
            result = docker_manager.check_docker_running()
            self.assertTrue(result)

    def testCheckDockerRunningWhenUnavailable(self):

        with patch('docker_manager.subprocess.run') as mock_run:
            mock_run.side_effect = FileNotFoundError()
            result = docker_manager.check_docker_running()
            self.assertFalse(result)

    def testListImagesCallsDocker(self):

        with patch('docker_manager.subprocess.run') as mock_run:
            with patch.object(docker_manager, 'check_docker_running', return_value=True):
                docker_manager.list_images()
                mock_run.assert_called_once_with(["docker", "images"])

    def testListRunningContainersCallsDocker(self):

        with patch('docker_manager.subprocess.run') as mock_run:
            with patch.object(docker_manager, 'check_docker_running', return_value=True):
                docker_manager.list_running_containers()
                mock_run.assert_called_once_with(["docker", "ps"])

    def testListAllContainersCallsDocker(self):

        with patch('docker_manager.subprocess.run') as mock_run:
            with patch.object(docker_manager, 'check_docker_running', return_value=True):
                docker_manager.list_all_containers()
                mock_run.assert_called_once_with(["docker", "ps", "-a"])

    def testRunImageWithValidInput(self):
 
        with patch('builtins.input', side_effect=["nginx", ""]):
            with patch('docker_manager.subprocess.run') as mock_run:
                with patch.object(docker_manager, 'check_docker_running', return_value=True):
                    mock_run.return_value = MagicMock(returncode=0, stdout="container123", stderr="")
                    docker_manager.run_image()
                    self.assertTrue(mock_run.called)

    def testRunImageWithEmptyName(self):

        with patch('builtins.input', side_effect=[""]):
            with patch.object(docker_manager, 'check_docker_running', return_value=True):
                docker_manager.run_image()

    def testStopContainerWithValidInput(self):

        with patch('builtins.input', side_effect=["container123"]):
            with patch('docker_manager.subprocess.run') as mock_run:
                with patch.object(docker_manager, 'check_docker_running', return_value=True):
                    mock_run.return_value = MagicMock(returncode=0, stdout="Stopped", stderr="")
                    docker_manager.stop_container()
                    self.assertTrue(mock_run.called)

    def testSearchDockerhubWithValidInput(self):

        with patch('builtins.input', return_value="nginx"):
            with patch('docker_manager.subprocess.run') as mock_run:
                docker_manager.search_dockerhub()
                mock_run.assert_called_once()

    def testSearchDockerhubWithEmptyInput(self):

        with patch('builtins.input', return_value=""):
            with patch('docker_manager.subprocess.run') as mock_run:
                docker_manager.search_dockerhub()
                mock_run.assert_not_called()

    def testPullImageWithValidInput(self):

        with patch('builtins.input', return_value="nginx"):
            with patch('docker_manager.subprocess.run') as mock_run:
                with patch.object(docker_manager, 'check_docker_running', return_value=True):
                    mock_run.return_value = MagicMock(returncode=0, stdout="Pulling", stderr="")
                    docker_manager.pull_image()
                    self.assertTrue(mock_run.called)

    def testSearchLocalImagesWithValidInput(self):

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

    def testBuildImageWithValidInputs(self):

        with patch('builtins.input', side_effect=["Dockerfile", "myapp:1.0"]):
            with patch('os.path.exists', return_value=True):
                with patch('docker_manager.subprocess.run') as mock_run:
                    with patch.object(docker_manager, 'check_docker_running', return_value=True):
                        mock_run.return_value = MagicMock(returncode=0, stdout="Built", stderr="")
                        docker_manager.build_image()
                        self.assertTrue(mock_run.called)

    def testCreateDockerfileCreatesFile(self):

        with patch('builtins.input', side_effect=["./Dockerfile", "1", "python:3.9", "python app.py"]):
            with patch('os.path.exists', return_value=False):
                with patch('os.path.dirname', return_value=''):
                    with patch('builtins.open', create=True) as mock_file:
                        docker_manager.create_dockerfile()
                        mock_file.assert_called()

    def testStartContainerWithValidInput(self):

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
