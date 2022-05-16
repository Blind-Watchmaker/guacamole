import logging

from classes import (
    LineTokenizationError,
    Processor,
    StandardDefinitionParseError,
    TokenProcessor,
)


class LineProcessor(Processor):
    """The LineProcessor class defines functionality to process lines
    as they are streamed from an input file.

    The LineProcessor class defines all of the functionality required to
    process a line as it is streamed from an input file. The only publicly
    exposed method is the process() method, which allows the initialized
    LineProcessor object to be broken into tokens and parsed tokenwise in
    accordance with the constraints from the standard definition file
    (LX section, LXY subsection). Private helper methods tokenize the line,
    return token constraints from the standard definition file and validate
    the token and token constraints prior to processing.

    Attributes:
        line:
            A string representing a line from an input file we are processing.
        standard_definition:
            A list of dictionaries representing a standard definition file.
        lx:
            A dynamic attribute representing a LX section of the line.
        tokens:
            A dynamic attribute representing a list of sub-section tokens
            associated with the line
            (i.e. any token that occurs after an '&' symbol).
        token_constraints:
            A dynamic attribute representing the "sub-sections" key in the
            standard definition file for the section LX.
            This is required to understand how tokens should be processed.
    """

    def __init__(self, line, standard_definition):
        """Inits LineProcessor with line and standard_definition."""
        self.line = line
        self.standard_definition = standard_definition

    def _tokenize_line(self):
        """Tokenizes the line from the input file being streamed in.

        The line is split based on the '&' character and stored as a
        list of tokens. If the list of tokens consists of less than two
        characters, our business logic (the separability of a line into an
        LX section and LXY sub-sections) breaks and we throw raise a custom
        error. Upon success, dynamic attributes self.lx stores the "LX" section
        and self.token stores a list of tokens from the line to be parsed
        by the standard_definition file.

        Args:

        Returns:

        Raises:
            LineTokenizationError:  Not enough tokens yielded to parse line
            {self.line} into LX sections and LXY subsections.
        """
        tokens = self.line.split("&")
        if len(tokens) < 2:
            raise LineTokenizationError(self.line)
        self.lx = tokens[0]
        self.tokens = tokens[1:]

    def _return_token_constraints(self):
        """Returns the token constraints from the standard definition,
        defined as the list of dict sub-sections associated with a section LX.

        Using a generator expression, self.standard_definition is searched
        for the entry that matches the section value (self.lx). If we find it,
        we return the "sub-sections" key of that dictionary
        (or None if that wasn't found).
        If we don't find it, we return None.

        Args:

        Returns:
            A dictionary containing the token constraints associated
            with line (with section LX) and tokens (expected to abide by LXY
            constraints from standard_definition file).

            None.

        Raises:

        """
        lx_dict = next(
            (item for item in self.standard_definition if item.get("key") == self.lx),
            None,
        )
        if not lx_dict:
            return None
        else:
            return lx_dict.get("sub_sections")

    def _validate_token_constraints(self):
        """Validate that the retrieval process was able to get a dictionary entry
        and set the dynamic attribute self.token_constraints.

        After using the private function self._return_token_constraints()
        to return the token constraints for the line, we set the dynamic attribute
        self.token_constraints to that value unless the token_constraints is None.
        If the latter is the case, our business logic (the assumption that each
        line of the standard definition file has parsing rules for tokens) breaks
        and we raise a custom error.

        Args:

        Returns:

        Raises:
            StandardDefinitionParseError:
            No standard definition sub-sections found for {self.lx}

        """
        token_constraints = self._return_token_constraints()
        if token_constraints is None:
            raise StandardDefinitionParseError(self.lx)
        self.token_constraints = token_constraints

    def _validate_tokens(self):
        """Validate that the number of token constraints LXY is greater than
        or equal to the number of tokens presented.

        We do not have an error code to handle the situation where the number of
        token_constraints (the number of LXY sub-sections in the standard definition
        file for a section LX) exceeds the number of tokens. Since this will break
        our existing business logic, we detect this case and log a warning to the user.
        We handle this situation gracefully (scaling the number of tokens in the
        dynamic attribute self.tokens to match the number of sub-sections)
        so processing can continue.

        Args:

        Returns:
            warning: Number of standard definition sub-sections (LXYs)
            less than the total number of tokens in line

        Raises:

        """
        if len(self.token_constraints) < len(self.tokens):
            logging.warning(
                "Number of LXYs less than the number of tokens in line %s for %s",
                self.line.strip(),
                self.lx,
            )
            logging.warning(
                "Scaling the number of tokens back to match the number of LXYs."
            )
            self.tokens = self.tokens[0 : len(self.token_constraints)]

    def process(self):
        """Processes the line streamed in from the input file.

        The input line (self.line) is tokenized and the token
        constraints are retrieved from the standard definition file
        (self.standard_definition). Upon validation, a list called
        data is populated with the output coming from processed
        TokenProcessors based upon the section LX, token to be
        parsed and the token constraint associated with the token.
        This data is returned.

        Args:

        Returns:
            data: A list of dictionaries required for all analyses,
            with each dictionary representing the validation properties
            and error codes associated with a single token.

        Raises:

        """
        self._tokenize_line()
        self._validate_token_constraints()
        self._validate_tokens()

        # Due to token validation, we now know
        # len(self.token_constraints) >= len(tokens).
        # So we loop over the number of token constraints
        # to take into account a situation where we have
        # strictly more token constraints than tokens
        # (i.e. a missing token). This situation is associated
        # with error code E05 (see the enum ErrorCodes in
        # token_processor.py).
        data = []
        for i in range(len(self.token_constraints)):
            # A Boolean to make a distinction between missing values
            # (when token_constraints > tokens) and values that simply
            # do not meet the validation criteria entirely.
            missing = len(self.token_constraints[0 : i + 1]) > len(
                self.tokens[0 : i + 1]
            )
            tp = TokenProcessor(
                lx=self.lx,
                token=self.tokens[i : i + 1],
                token_constraints=self.token_constraints[i : i + 1],
                missing=missing,
            )
            data.append(tp.process())
        return data
