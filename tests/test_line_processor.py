import logging
import pytest

from classes.custom_errors import LineTokenizationError, StandardDefinitionParseError

LOGGER = logging.getLogger(__name__)


def test_process(line_processor):
    data = line_processor.process()
    expected_result = [
        {
            "report_data": {
                "Section": "L1",
                "Sub-Section": "L11",
                "Given DataType": "digits",
                "Expected DataType": "digits",
                "Given Length": 2,
                "Expected MaxLength": 1,
                "Error Code": "E03",
            },
            "summary_data": {
                "Error Message": (
                    "L11 field under section L1 fails "
                    "the max length (expected: 1) validation, "
                    "however it passes the data type (digits) validation"
                )
            },
        },
        {
            "report_data": {
                "Section": "L1",
                "Sub-Section": "L12",
                "Given DataType": "",
                "Expected DataType": "word_characters",
                "Given Length": "",
                "Expected MaxLength": 3,
                "Error Code": "E04",
            },
            "summary_data": {
                "Error Message": (
                    "L12 field under section L1 fails " "all the validation criteria."
                )
            },
        },
        {
            "report_data": {
                "Section": "L1",
                "Sub-Section": "L13",
                "Given DataType": "word_characters",
                "Expected DataType": "word_characters",
                "Given Length": 1,
                "Expected MaxLength": 2,
                "Error Code": "E01",
            },
            "summary_data": {
                "Error Message": (
                    "L13 field under segment L1 passes " "all the validation criteria"
                )
            },
        },
    ]
    assert data == expected_result


def test_process_raises_line_tokenization_error(line_processor_with_invalid_line):
    with pytest.raises(LineTokenizationError):
        line_processor_with_invalid_line.process()


def test_process_with_bad_standard_definition(
    line_processor_with_invalid_standard_definition,
):
    with pytest.raises(StandardDefinitionParseError):
        line_processor_with_invalid_standard_definition.process()


def test_process_with_empty_standard_definition(
    line_processor_with_empty_standard_definition,
):
    with pytest.raises(StandardDefinitionParseError):
        line_processor_with_empty_standard_definition.process()


def test_process_with_long_line(caplog, line_processor_with_long_line):
    with caplog.at_level(logging.WARNING):
        data = line_processor_with_long_line.process()
        expected_data = [
            {
                "report_data": {
                    "Section": "L1",
                    "Sub-Section": "L11",
                    "Given DataType": "digits",
                    "Expected DataType": "digits",
                    "Given Length": 1,
                    "Expected MaxLength": 1,
                    "Error Code": "E01",
                },
                "summary_data": {
                    "Error Message": (
                        "L11 field under segment L1 "
                        "passes all the validation criteria"
                    )
                },
            },
            {
                "report_data": {
                    "Section": "L1",
                    "Sub-Section": "L12",
                    "Given DataType": "word_characters",
                    "Expected DataType": "word_characters",
                    "Given Length": 3,
                    "Expected MaxLength": 3,
                    "Error Code": "E01",
                },
                "summary_data": {
                    "Error Message": (
                        "L12 field under segment L1 "
                        "passes all the validation criteria"
                    )
                },
            },
            {
                "report_data": {
                    "Section": "L1",
                    "Sub-Section": "L13",
                    "Given DataType": "word_characters",
                    "Expected DataType": "word_characters",
                    "Given Length": 2,
                    "Expected MaxLength": 2,
                    "Error Code": "E01",
                },
                "summary_data": {
                    "Error Message": (
                        "L13 field under segment L1 passes "
                        "all the validation criteria"
                    )
                },
            },
        ]
        assert data == expected_data
        assert (
            "Scaling the number of tokens back to match the number of LXYs."
            in caplog.text
        )
