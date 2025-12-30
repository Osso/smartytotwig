import os
import sys
import tempfile

import pytest

from smartytotwig.main import main


class TestMain:
    def test_main_with_source_and_target(self, tmp_path):
        # Create a test Smarty file
        source_file = tmp_path / "test.tpl"
        source_file.write_text("{$foo}")

        target_file = tmp_path / "test.twig"

        # Mock sys.argv
        original_argv = sys.argv
        try:
            sys.argv = ["smartytotwig", "-s", str(source_file), "-t", str(target_file)]
            main()
        finally:
            sys.argv = original_argv

        # Check output file was created
        assert target_file.exists()
        assert "{{ foo }}" in target_file.read_text()

    def test_main_with_source_only(self, tmp_path):
        # Create a test Smarty file
        source_file = tmp_path / "template.tpl"
        source_file.write_text("{$bar}")

        # Mock sys.argv
        original_argv = sys.argv
        try:
            sys.argv = ["smartytotwig", "-s", str(source_file)]
            main()
        finally:
            sys.argv = original_argv

        # Check output file was created with auto-generated name
        target_file = tmp_path / "template.twig"
        assert target_file.exists()
        assert "{{ bar }}" in target_file.read_text()

    def test_main_without_source(self, capsys):
        # Mock sys.argv with no source
        original_argv = sys.argv
        try:
            sys.argv = ["smartytotwig"]
            main()
        finally:
            sys.argv = original_argv

        # No output should be produced
        captured = capsys.readouterr()
        assert captured.out == ""
