import pathlib

from classes.generator import Generator
from utils import (
    load_json_from_path,
    make_dir_if_absent,
    remove_file_if_exists,
)

# Global variables for defining the output directory and output files
# for all analyses. If you want to add a new analysis, create a global
# variable here.
OUTPUT_DIR = "parsed"
REPORT_FILE = "report.csv"
SUMMARY_FILE = "summary.txt"

# Global variables for defining where the input file and the standard
# definition file are coming from.
BASE_DIR = pathlib.Path(__file__).parent.resolve()
INPUT_FILE = "input_file.txt"
STANDARD_DEFINITION_FILE = "standard_definition.json"

# Boolean global variables for defining what analyses should be output.
# By default, both the report and summary are generated during runtime.
# If you want to add a new analysis, create another global variable here.
GENERATE_REPORT = True
GENERATE_SUMMARY = True

if __name__ == "__main__":

    # Get the standard definition file
    standard_definition = load_json_from_path(
        path=f"{BASE_DIR}/{STANDARD_DEFINITION_FILE}",
        error_message="Standard definition file not accessible",
    )

    # Determine whether the `OUTPUT_DIR` directory exists
    # and if it doesn't, create a new directory called `OUTPUT_DIR``
    make_dir_if_absent(output_dir=f"{OUTPUT_DIR}")

    # Remove analysis files if they already exists - we'll be generating them
    # with the final command below. If you have another analysis, add another
    # logical flow below with the new global variables you have defined above.
    if GENERATE_REPORT:
        remove_file_if_exists(f"{OUTPUT_DIR}/{REPORT_FILE}")
    if GENERATE_SUMMARY:
        remove_file_if_exists(f"{OUTPUT_DIR}/{SUMMARY_FILE}")

    # Generate the report and the summary in the directory called `OUTPUT_DIR`
    gen = Generator()
    gen.generate_analyses_from_input_file(
        input_path=f"{BASE_DIR}/{INPUT_FILE}",
        summary_path=f"{OUTPUT_DIR}/{SUMMARY_FILE}",
        report_path=f"{OUTPUT_DIR}/{REPORT_FILE}",
        standard_definition=standard_definition,
        report=GENERATE_REPORT,
        summary=GENERATE_SUMMARY,
    )
