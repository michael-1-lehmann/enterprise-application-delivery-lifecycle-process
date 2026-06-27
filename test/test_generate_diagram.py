#!/usr/bin/env python3

import unittest
from pathlib import Path
from drawio.generate_process_diagram import generate_drawio

class TestDrawio(unittest.TestCase):
    def tearDown(self):
        test_dir = Path(__file__).resolve().parent
        for drawio_file in test_dir.glob("test_output*.drawio"):
            if drawio_file.is_file():
                drawio_file.unlink()

    def test_meta_information_only_without_name(self):
        repo_root = Path(__file__).resolve().parents[1]
        input_path = repo_root / "test" / "test_meta_information_only_without_name.yaml"
        output_path = repo_root / "test" / "test_output_meta_information_only_without_name.drawio"

        generate_drawio(input_path, output_path)

    def test_meta_information_only_wrong_elements(self):
        repo_root = Path(__file__).resolve().parents[1]
        input_path = repo_root / "test" / "test_meta_information_only_wrong_elements.yaml"
        output_path = repo_root / "test" / "test_output_meta_information_only_wrong_elements.drawio"

        generate_drawio(input_path, output_path)

    def test_meta_information_only_unknown_meta_element(self):
        repo_root = Path(__file__).resolve().parents[1]
        input_path = repo_root / "test" / "test_meta_information_only_unknown_meta_element.yaml"
        output_path = repo_root / "test" / "test_output_meta_information_only_unknown_meta_element.drawio"

        generate_drawio(input_path, output_path)

    def test_meta_information_only_only_name(self):
        repo_root = Path(__file__).resolve().parents[1]
        input_path = repo_root / "test" / "test_meta_information_only_only_name.yaml"
        output_path = repo_root / "test" / "test_output_meta_information_only_name.drawio"

        generate_drawio(input_path, output_path)

    def test_meta_information_empty_process_groups(self):
        repo_root = Path(__file__).resolve().parents[1]
        input_path = repo_root / "test" / "test_meta_information_empty_process_groups.yaml"
        output_path = repo_root / "test" / "test_output_meta_information_empty_process_groups.drawio"

        generate_drawio(input_path, output_path)

    def test_meta_information_and_process_groups_only(self):
        repo_root = Path(__file__).resolve().parents[1]
        input_path = repo_root / "test" / "test_meta_information_process_group_only.yaml"
        output_path = repo_root / "test" / "test_output_meta_information_process_group_only.drawio"

        generate_drawio(input_path, output_path)

    def test_meta_information_process_group_wrong_element(self):
        repo_root = Path(__file__).resolve().parents[1]
        input_path = repo_root / "test" / "test_meta_information_process_group_wrong_element.yaml"
        output_path = repo_root / "test" / "test_output_meta_information_process_group_wrong_element.drawio"

        generate_drawio(input_path, output_path)

    def test_meta_information_phases_only(self):
        repo_root = Path(__file__).resolve().parents[1]
        input_path = repo_root / "test" / "test_meta_information_phases_only.yaml"
        output_path = repo_root / "test" / "test_output_meta_information_phases_only.drawio"

        generate_drawio(input_path, output_path)

    def test_meta_information_phases_wrong_element(self):
        repo_root = Path(__file__).resolve().parents[1]
        input_path = repo_root / "test" / "test_meta_information_phases_wrong_element.yaml"
        output_path = repo_root / "test" / "test_output_meta_information_phases_wrong_element.drawio"

        generate_drawio(input_path, output_path)

    def test_meta_information_and_process_groups_empty_activities(self):
        repo_root = Path(__file__).resolve().parents[1]
        input_path = repo_root / "test" / "test_meta_information_process_group_empty_activities.yaml"
        output_path = repo_root / "test" / "test_output_meta_information_process_group_empty_activities.drawio"

        generate_drawio(input_path, output_path)

    def test_meta_information_and_process_groups_activities_wrong_elements(self):
        repo_root = Path(__file__).resolve().parents[1]
        input_path = repo_root / "test" / "test_meta_information_process_group_activities_wrong_elements.yaml"
        output_path = repo_root / "test" / "test_output_meta_information_process_group_activities_wrong_elements.drawio"

        generate_drawio(input_path, output_path)

    def test_meta_information_and_process_groups_activities_activity_connections_wrong_elements(self):
        repo_root = Path(__file__).resolve().parents[1]
        input_path = repo_root / "test" / "test_meta_information_process_group_activities_activity_connections_wrong_elements.yaml"
        output_path = repo_root / "test" / "test_output_meta_information_process_group_activities_activity_connections_wrong_elements.drawio"

        generate_drawio(input_path, output_path)

if __name__ == '__main__':
    unittest.main()

