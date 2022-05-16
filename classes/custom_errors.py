class Error(Exception):
    """Base class for custom exceptions"""

    pass


class LineTokenizationError(Error):
    """Exception raised for errors in tokenizing a line.

    In accordance with the standard definition file, the
    tokenization process assumes that a line from an
    input file can be tokenized (with '&' as the delimiter)
    into:
    (a) a token called LX (the "key" attribute in a
    standard definition file);
    and
    (b) a set of tokens - one for each of the sub-sections
    LXY in the standard definition file.
    This exception is raised when a tokenized line is too
    short, indicating that there aren't enough tokens on
    the line to make the distinction between section and
    subsection. In other words, this gets raised when there
    is only one token.

    Attributes:
        line -- The offending line from the input file
        message -- Description of the error
    """

    def __init__(self, line):
        self.line = line
        self.message = (
            f"Not enough tokens yielded to parse line "
            f"{self.line} into LX sections and LXY subsections."
        )
        super().__init__(self.message)


class StandardDefinitionParseError(Error):
    """Exception raised for errors in parsing the standard definition file.

    The parsing logic for a standard definition file
    assumes that for every section LX, there are corresponding
    sub-sections LXY.
    This exception is raised when there are no subsections
    within a standard definition file.

    Attributes:
        lx -- The offending LX section from the standard definition file
        message -- Description of the error
    """

    def __init__(self, lx):
        self.lx = lx
        self.message = f"No standard definition sub-sections for {self.lx}"
        super().__init__(self.message)
