# BlueNode Interview Task

The code presented in this repository accomplishes the task objective: parsing an input file using a standard definition and generate analyses. Please read the file `INSTRUCTIONS.md` for a more detailed break-down of the requirements involved for
the given project.

## Project Structure

While Python projects leave some room for flexibility in the project structure, I have tried to organize my work in line with existing Python conventions.

* The `classes` directory contains all of the classes defined for the project. This includes an abstract base class called `Processor`, two derived classes (a `TokenProcessor` class and a `LineProcessor` class), a `Generator` class for generating analyses and the custom errors `LineTokenizationError` and `StandardDefinitionParseError` defined when the business logic is deemed to have been violated in a way that the user may wish to investigate before proceeding further.

* The `tests` directory contains all files required for running tests with the `pytest` framework. Please read the section below on **Testing and Code Coverage** for more details.

Within the root path, we have all of the files that the project began with:

* `sample/report.csv` - a sample generated report - see `INSTRUCTIONS.md` for details on how it was derived.
* `sample/summary.txt` - a sample generated summary - see `INSTRUCTIONS.md` for details on how it was derived.
* `error_codes.json` - the error codes relevant to summaries and reports
* `input_file.txt` - a sample input file for parsing
* `INSTRUCTIONS.md` - documents the instructions for the project.
* `standard_definition.json` - a standard definition file used to guide parsing.

Within the root path, we also have some files that I have added:

* `solution.py` - a file that can be used to run the analyses
* `utils.py` - a utilities file containing useful enums and helper file/OS-related functions
* `pytest.ini` - a file to configure the `pytest` testing framework
* `.gitignore` - to tell Git to ignore committing certain files
* `.pre-commit-config.yaml` - for pre-commit hooks to ensure code quality.


## Installation

Begin by creating a new virtual environment associated with the project. If you haven't already installed `virtualenv`,
please use the package manager [pip](https://pip.pypa.io/en/stable/) to do so:

```bash
pip install virtualenv
```

To create and activate a virtual environment called `env`, run the following commands in the same directory as this `README.md`:

```bash
python -m virtualenv env
source env/bin/activate
```

Next, you will want to install the Python dependencies required for running this project. Conveniently, these are all stored in a file called `requirements.txt` and can be installed in one-go using `pip`:

```bash
pip install -r requirements.txt
```

Some notable dependencies include:
* [pytest](https://docs.pytest.org/en/7.1.x/index.html) - a framework for writing small readable tests for Python projects;
* [coverage](https://coverage.readthedocs.io/en/6.3.3/) - a tool for measuring code coverage for Python programs;

Finally, you will want to run the code and generate some analyses based on an input file and standard definition file.
The file `solution.py` in this repository contains the code that actually parses the input file line-by-line and
generates any analytical files (including a summary text file and a report csv file). While the output formats of those
two analyses are fixed at the present time (.csv, .txt), this file also offers some customization that could be handy
to some users:

* The directory for output analyses can be modified by altering the `OUTPUT_DIR` global variable.
* The file names for the summary and report can be modified by altering the `SUMMARY_FILE` and `REPORT_FILE` global variables.
* The location and file names for the input file and the standard definition file can be altered using the `BASE_DIR`,
`INPUT_FILE` and `STANDARD_DEFINITION_FILE` global variables. 
* By default, the project is configured to allow the summary and the report to get generated together at runtime.
To toggle the summary and report on and off, please use the `GENERATE_REPORT` and `GENERATE_SUMMARY` Booleans provided.

By default, the code has been configured to create the report in the location `parsed/report.csv` and to create the summary in the location `parsed/summary.txt`. This decision was motivated by the instructions in the `INSTRUCTIONS.md` file.

## Basic Usage

To run the application, please configure the global variables listed above in `solution.py` to your liking and then run:

```bash
python solution.py
```

This will create any analytical files in the desired location.

## Pre-Commit Hooks

The `.pre-commit-config.yaml` file configures the git hooks designed to be run before committing to the project. My coding quality standards for this repo include `flake8` and `black`.

To begin, install the pre-commit hooks:
```bash
pre-commit install
```

One command for running the hooks on the files is:
```bash
pre-commit run --all-files
```

This will prevent any Python files from exhibiting poor code quality standards in the repo.

## Testing and Code Coverage

All tests have been written using the `pytest` framework, which is optimally designed to allow programmers to write small and readable tests. `pytest` configuration is governed by the `pytest.ini` file - specifically in this case, it determines the path to ensure that `pytest` can find all of the tests within the project.

All files related to tests are conveniently stored in a directory called `tests`. There are a few notable files:

* `conftest.py`: Provides fixtures for the entire directory.
* `test_line_processor.py`: Tests functionality in the
concrete class `LineProcessor`.
* `test_token_processor.py`: Tests functionality in the
concrete class `TokenProcessor`.
* `test_processor.py`: Tests functionality in the abstract base class `Processor` (required for the `coverage` tool and arguably unimportant).

To run `coverage` and `pytest` in combination, the following commands may be useful to you: 

```bash
coverage run -m pytest
coverage report -m
```

The latter command will display code coverage (statements, misses, coverage percent, and what statements are not exercised by tests). It goes without saying that code coverage can be a deceptive metric, so please approach with hesitation.

## Design Decisions

In completing this project, I made a few implementation decisions that are worthy of being discussed transparently. There are aspects that may be suboptimal upon further discussion, but it is worthwhile understanding the rationale behind the decisions I made.

* Good code acknowledges the potential for situational changes and remains flexible, within reason. While the sample input file `input_file.txt` is small in size and can be loaded into memory without issue prior to parsing,
a streaming approach would scale to larger files better in the long run. **As a result, I decided to focus on parsing line-by-line as the input file is read in.**

* **The code has been designed to make it easy to add a new analytical report, should the need arise.** One can simply modify the data contract (returned in the `TokenProcessor`) and add new global variables in `solution.py` to accommodate new analyses.

* It is important to understand the business logic governing the problem you intend to solve. While the error codes could be loaded from the JSON file (`error_codes.json`), the templating itself wasn't quite correct in several spots and it plays a pivotal role in determining what error message to generate for a summary. **As a result, I elected to make an enum representing the error codes (`ErrorCodes` in `utils.py`) so the business logic is codified.** I made the same decision with the idea of datatypes, a central concept that governs how a report is generated. **By creating an enum to represent the datatypes (`DataTypes` in `utils.py`), the business logic is codified.** Should the user require another error or datatype supported within the analytical process, they will have to modify a small number of private validation functions. This point has been noted as a comment on the enums. 

* I can envision this code could still remain applicable even if a brand new standard definition file is presented, provided it is structured similarly to the file given to us (`standard_definition.json`). **Hence, I elected not to codify the standard definition file and have it imported in from memory using `json.load`.**

* **Finally, there is the difficult matter of handling unexpected behaviour (a problem that surely emerges in parsing problems fairly frequently).** The following represents my opinion - the issue itself is thought-provoking and I am open to other views on the matter. 
* **(1) From my perspective, there are some situations where one should handle issues gracefully and continue processing.** For example, there is a situation where a line with a given section `LX` has more tokens than there are sub-sections within the standard definition file (`LXYs`). While there is no error code associated with that, a warning can be logged for transparency and a graceful workaround can be imagined (e.g. scaling the number of tokens back so it matches the number of sub-sections). This behaviour is also easy to modify, should the user desire it. I was also strongly motivated to think this way simply because the `input_file.txt` provided exhibited this very issue.

* **(2) Still, there are situations where parsing should be stopped altogether** (where the business logic assumptions are stretched to the absolute limit and the user should be prompted to reflect on exactly what has been given to them). For example, if a line doesn't have subsections `LXY` from the standard definition file indicating how it should be parsed, it really doesn't make sense to continue with the report. Perhaps the standard definition file can be adjusted slightly by the user, resulting in a far higher quality analytical result than if we just skipped that `LX` section and moved on. It's a fine balance and I don't have all of the answers - I am simply trying to be transparent about how I addressed an open-ended problem.

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.

## Author

Will Musgrave
