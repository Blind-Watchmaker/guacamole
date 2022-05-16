import filecmp
import os

from utils import remove_file_if_exists


def test_generate_analyses_from_input_file(
    generator,
    input_path,
    summary_path,
    report_path,
    standard_definition,
    expected_report_path,
    expected_summary_path,
):
    # Remove the summary and report if they exist.
    remove_file_if_exists(summary_path)
    remove_file_if_exists(report_path)

    # Assert the summary and report don't exist.
    assert not os.path.exists(summary_path)
    assert not os.path.exists(report_path)
    # Assert the input file exists already.
    assert os.path.exists(input_path)

    # Act
    generator.generate_analyses_from_input_file(
        input_path,
        summary_path,
        report_path,
        standard_definition,
        report=True,
        summary=True,
    )

    # Assert the summary and report now exist.
    assert os.path.exists(summary_path)
    assert os.path.exists(report_path)

    # Assert the summary and report are as expected.
    filecmp.cmp(summary_path, expected_summary_path)
    filecmp.cmp(report_path, expected_report_path)

    # Remove the summary and report.
    remove_file_if_exists(summary_path)
    remove_file_if_exists(report_path)

    # Assert the summary and report don't exist.
    assert not os.path.exists(summary_path)
    assert not os.path.exists(report_path)
    # Assert the input file still exists.
    assert os.path.exists(input_path)
