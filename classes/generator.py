import csv

from classes.line_processor import LineProcessor


class Generator:
    """The Generator class contains functions for generating any form of
    analysis from the input file.

    The Generator class defines all of the functionality required to
    generate a csv report file and a text summary file,
    as per the spec in `INSTRUCTIONS.md`. It also defines functionality
    to generate analyses specifically from a provided input file
    and standard definition file.

    Attributes:

    """

    def generate_report(self, output_path, line_data):
        """Generate a csv report (to be stored at output_path and
        to be written line-by-line).

        The data parsed from a line of the input file is used to write
        a csv report file line-by-line. If the header already exists for
        the file, it is skipped. Otherwise, we add the header at the
        beginning.

        Args:
            output_path: The path for the report file to be found.
            line_data: A list of dictionaries representing data
            from a single line.

        Returns:

        Raises:

        """
        report_line_data = [item["report_data"] for item in line_data]
        report_keys = report_line_data[0].keys()
        with open(output_path, "a+", newline="") as report_file:
            dict_writer = csv.DictWriter(report_file, report_keys)
            if report_file.tell() == 0:
                dict_writer.writeheader()
            for row in report_line_data:
                dict_writer.writerow(row)

    def generate_summary(self, output_path, line_data):
        """Generate a text summary (to be stored at output_path and
        to be written line-by-line).

        The data parsed from a line of the input file is used to write
        a text summary file line-by-line.

        Args:
            output_path: The path for the report file to be found.
            line_data: A list of dictionaries representing data
            from a single line.

        Returns:

        Raises:

        """
        summary_line_data = [item["summary_data"] for item in line_data]
        with open(output_path, "a+") as summary_writer:
            for row in summary_line_data:
                summary_writer.write(f"{row['Error Message']}\n")
            summary_writer.write("\n")

    def generate_analyses_from_input_file(
        self,
        input_path,
        summary_path,
        report_path,
        standard_definition,
        report=True,
        summary=True,
    ):
        """Generate analyses in output files based on parsing a line
        from an input file. Reading and writing is performed line-by-line.

        The data parsed from a line of the input file is used to write
        analyses into files.

        Args:
            input_path: Path to the input file (str)
            summary_path: Path to where the summary file should
            be written (str).
            report_path: Path to where the report file should
            be written (str).
            standard_definition: The loaded standard_definition
            (either a list of dicts or a dict).
            report: Boolean to determine if report should be generated.
            summary: Boolean to determine if summary should be generated.

        Returns:

        Raises:

        """
        with open(input_path) as reader:
            for line in reader:
                lp = LineProcessor(line, standard_definition)
                line_data = lp.process()
                if report:
                    self.generate_report(report_path, line_data)
                if summary:
                    self.generate_summary(summary_path, line_data)
