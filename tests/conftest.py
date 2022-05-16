import pathlib
import pytest

from classes import LineProcessor, Generator, TokenProcessor


@pytest.fixture
def base_dir():
    return pathlib.Path(__file__).parent.resolve()


@pytest.fixture
def non_existent_dir(base_dir):
    return f"{base_dir}/non_existent_dir"


@pytest.fixture
def path_to_file_to_delete(base_dir):
    file = "dummy_data/random_file.txt"
    return f"{base_dir}/{file}"


@pytest.fixture
def valid_path_to_json(base_dir):
    file = "dummy_data/sample.json"
    return f"{base_dir}/{file}"


@pytest.fixture
def invalid_path_to_json():
    return "not_here/not_here.json"


@pytest.fixture
def input_path(base_dir):
    file = "dummy_data/input_file.txt"
    return f"{base_dir}/{file}"


@pytest.fixture
def summary_path(base_dir):
    file = "dummy_data/summary.txt"
    return f"{base_dir}/{file}"


@pytest.fixture
def report_path(base_dir):
    file = "dummy_data/report.csv"
    return f"{base_dir}/{file}"


@pytest.fixture
def expected_report_path(base_dir):
    file = "dummy_data/expected_report.csv"
    return f"{base_dir}/{file}"


@pytest.fixture
def expected_summary_path(base_dir):
    file = "dummy_data/expected_summary.txt"
    return f"{base_dir}/{file}"


@pytest.fixture
def error_message():
    return "Error Message!"


@pytest.fixture
def line():
    return "L1&99&&A"


@pytest.fixture
def short_line():
    return "L1"


@pytest.fixture
def long_line():
    return "L1&4&AbC&xY&garbage"


@pytest.fixture
def other_token():
    return "4.abc3jf3247@"


@pytest.fixture
def standard_definition():
    return [
        {
            "key": "L1",
            "sub_sections": [
                {"key": "L11", "data_type": "digits", "max_length": 1},
                {"key": "L12", "data_type": "word_characters", "max_length": 3},
                {"key": "L13", "data_type": "word_characters", "max_length": 2},
            ],
        },
        {
            "key": "L4",
            "sub_sections": [
                {"key": "L41", "data_type": "word_characters", "max_length": 1},
                {"key": "L42", "data_type": "digits", "max_length": 6},
            ],
        },
    ]


@pytest.fixture
def invalid_standard_definition():
    return [{"key": "L1", "sub-sections": "garbage"}]


@pytest.fixture
def empty_standard_definition():
    return []


@pytest.fixture
def line_processor(line, standard_definition):
    return LineProcessor(line, standard_definition)


@pytest.fixture
def line_processor_with_invalid_line(short_line, standard_definition):
    return LineProcessor(short_line, standard_definition)


@pytest.fixture
def line_processor_with_invalid_standard_definition(line, invalid_standard_definition):
    return LineProcessor(line, invalid_standard_definition)


@pytest.fixture
def line_processor_with_empty_standard_definition(line, empty_standard_definition):
    return LineProcessor(line, empty_standard_definition)


@pytest.fixture
def line_processor_with_long_line(long_line, standard_definition):
    return LineProcessor(long_line, standard_definition)


@pytest.fixture
def token_processor(short_line, other_token, standard_definition):
    return TokenProcessor(
        lx=short_line,
        token=other_token,
        token_constraints=standard_definition,
        missing=False,
    )


@pytest.fixture
def generator():
    return Generator()
