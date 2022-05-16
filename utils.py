from enum import Enum
import json
import os


class DataTypes(Enum):
    # The data types supported by current business logic for analysis.
    DIGITS = "digits"
    WORD_CHARACTERS = "word_characters"
    OTHER = "other"
    MISSING = ""


class ErrorCodes(Enum):
    # The error codes supported by current business logic for analysis.

    # Because of the issue of string formatting for the report and how
    # pivotal the error codes are to the business logic happening in the code,
    # it doesn't really make sense to have a user import the error codes from
    # a file. If you need to change the error codes, you have to change the
    # business logic. Because of this, I can also make some liberties and
    # revise some of these error codes to better support string formatting.
    # (I could have changed the original error_codes.json file but it
    # strikes me as pertinent to keep it unchanged.)
    E01 = {
        "code": "E01",
        "message_template": (
            "{lxy} field under segment {lx} passes all the validation criteria"
        ),
    }
    E02 = {
        "code": "E02",
        "message_template": (
            "{lxy} field under section {lx} fails "
            "the data type (expected: {data_type}) "
            "validation, however it passes the max "
            "length ({max_length}) validation"
        ),
    }
    E03 = {
        "code": "E03",
        "message_template": (
            "{lxy} field under section {lx} fails "
            "the max length (expected: {max_length}) "
            "validation, however it passes the data "
            "type ({data_type}) validation"
        ),
    }
    E04 = {
        "code": "E04",
        "message_template": (
            "{lxy} field under section {lx} fails all the validation criteria."
        ),
    }
    E05 = {
        "code": "E05",
        "message_template": "{lxy} field under section {lx} is missing.",
    }


def load_json_from_path(path, error_message):
    """Loads a JSON file based on the path if it exists.

    A JSON file specified by the path is loaded and returned if it exists.
    Otherwise, a FileNotFoundError is returned with a custom error message.

    Args:
        path: The path to the JSON file.
        error_message: The custom error message to be displayed if the file
        is not found.

    Returns:
        json_output: The output of loading the JSON into memory (likely
        a dictionary or a list of dictionaries)

    Raises:
        FileNotFoundError with custom error message.
    """
    try:
        f = None
        with open(path, "r") as f:
            json_output = json.load(f)
            return json_output
    except FileNotFoundError as e:
        e.strerror = error_message
        raise e
    finally:
        if f is not None:
            f.close()


def make_dir_if_absent(output_dir):
    """Makes the directory specified by output_dir if it doesn't already exist.

    Args:
        output_dir: The desired path for the directory.

    Returns:

    Raises:
    """
    dir_exists = os.path.exists(output_dir)
    if not dir_exists:
        os.makedirs(output_dir)


def remove_file_if_exists(path):
    """Removes a file in the given path if it exists.

    Args:
        path: The path to the file.

    Returns:

    Raises:
    """
    if os.path.exists(path):
        os.remove(path)
