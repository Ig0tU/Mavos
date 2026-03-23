import unittest
from unittest.mock import patch, MagicMock
import models
import agent
import commands
import os

class TestGPAutomator(unittest.TestCase):

    @patch('requests.get')
    def test_ollama_detection(self, mock_get):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"models": [{"name": "llama3"}]}
        mock_get.return_value = mock_response

        models_list = models.get_ollama_models()
        self.assertEqual(len(models_list), 1)
        self.assertEqual(models_list[0]['name'], "llama3")
        self.assertEqual(models_list[0]['provider'], "ollama")

    @patch('requests.get')
    def test_lm_studio_detection(self, mock_get):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"data": [{"id": "mistral-7b"}]}
        mock_get.return_value = mock_response

        models_list = models.get_lm_studio_models()
        self.assertEqual(len(models_list), 1)
        self.assertEqual(models_list[0]['name'], "mistral-7b")
        self.assertEqual(models_list[0]['provider'], "lm_studio")

    def test_file_tools(self):
        test_file = "test_file.txt"
        test_content = "hello world"

        # Test write
        result = commands.write_file.run(f"{test_file}|{test_content}")
        self.assertIn("successfully", result)

        # Test read
        result = commands.read_file.run(test_file)
        self.assertEqual(result, test_content)

        # Test list
        result = commands.list_directory.run(".")
        self.assertIn(test_file, result)

        # Cleanup
        if os.path.exists(test_file):
            os.remove(test_file)

    def test_shell_tool(self):
        result = commands.run_shell_command.run("echo 'hello shell'")
        self.assertEqual(result.strip(), "hello shell")

if __name__ == '__main__':
    unittest.main()
