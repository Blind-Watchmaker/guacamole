import os
import pytest

from utils import (
    load_json_from_path,
    make_dir_if_absent,
    remove_file_if_exists,
)


def test_load_json_from_file(valid_path_to_json, error_message):
    data = load_json_from_path(valid_path_to_json, error_message)
    expected_data = [{"in": "here", "random": "data"}]
    assert data == expected_data


def test_load_json_from_non_existent_file(invalid_path_to_json, error_message):
    with pytest.raises(FileNotFoundError):
        load_json_from_path(invalid_path_to_json, error_message)


def test_make_dir_if_absent(non_existent_dir):
    make_dir_if_absent(non_existent_dir)
    assert os.path.exists(non_existent_dir)
    os.rmdir(non_existent_dir)
    assert not os.path.exists(non_existent_dir)


def test_remove_file_if_exists(path_to_file_to_delete):
    assert os.path.exists(path_to_file_to_delete)
    remove_file_if_exists(path_to_file_to_delete)
    assert not os.path.exists(path_to_file_to_delete)
    open(path_to_file_to_delete, "a").close()
    assert os.path.exists(path_to_file_to_delete)
