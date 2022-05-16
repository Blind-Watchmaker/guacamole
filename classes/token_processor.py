from classes import Processor
from utils import DataTypes, ErrorCodes


class TokenProcessor(Processor):
    """The TokenProcessor class defines functionality to process tokens
    from a line streamed from an input file in accordance with a
    standard definition file.

    The TokenProcessor class defines all of the functionality required to
    process a token from a line streamed from the input file. The only publicly
    exposed method is the process() method, which performs validations on the
    token datatype and length to determine the correct error message and
    outputs a dictionary with data contracts for all analyses.
    Private helper methods determine the token datatype, validate the token
    datatype, validate the token length and return formatted error codes to
    be used in the data contract submitted through the process() method.

    Attributes:
        lx:
            The LX section of the line being processed.
        tokens:
            A sub-section token associated with the line
            (i.e. a token that occurs after an '&' symbol).
        token_constraints:
            A constraint from the "sub-sections" key in the standard definition
            file for the section LX.
            This is required to understand how tokens should be processed.
        missing:
            A Boolean indicating that the token should be
            marked as missing (greater number of constraints
            compared to tokens).
    """

    def __init__(self, lx, token, token_constraints, missing):
        """Inits TokenProcessor with lx, token, missing and token_constraints."""
        self.lx = lx
        self.token = token
        self.token_constraints = token_constraints
        self.missing = missing

    def _determine_token_datatype(self):
        """Determines the data type of the TokenProcessor's token.

        The token's datatype - restricted to a few values defined
        in the enum DataTypes - is determined using in-built Python
        str functionality wherever possible. A distinction is made
        between a missing token and a token that is neither a digit
        or a word character in order to match the report.csv in
        the sample directory.

        Args:

        Returns:
            A string representing the DataType

        Raises:

        """
        if (len(self.token) == 0) or (self.token is None):
            return DataTypes.MISSING.value
        if self.token.isdecimal():
            return DataTypes.DIGITS.value
        if self.token.isalpha():
            return DataTypes.WORD_CHARACTERS.value
        return DataTypes.OTHER.value

    def _validate_token_datatype(self):
        """Validates the data type of the TokenProcessor's token.

        The token's datatype - determined via the internal method
        determine_token_datatype() - is compared to the datatype
        extracted from the standard definition file (stored in
        self.token_constraints["data_type"]) and a Boolean is returned.

        Args:

        Returns:
            Boolean: True if the datatypes match, False if they don't.

        Raises:

        """
        token_dtype = self._determine_token_datatype()
        return token_dtype == self.token_constraints["data_type"]

    def _validate_token_length(self):
        """Validates the token is less than the maximum length of the constraint.

        The token's length is compared to the max_length
        extracted from the standard definition file (stored in
        self.token_constraints["max_length"]) and a Boolean is returned.

        Args:

        Returns:
            Boolean: True if the token is less than or equal, False if not.

        Raises:

        """
        if len(self.token) == 0:
            return False
        else:
            return len(self.token) <= self.token_constraints["max_length"]

    def _return_formatted_error_codes(self):
        """Retrieves the correct error code based on the token
        and token_constraints and returns a formatted error code.

        The token (if it exists) is evaluated against the token constraints
        to determine if it is a valid length and data-type. Depending upon
        the situation, the appropriate error code is retrieved and the error
        message is filled in with values from the standard definition file
        to fill in templated slots. This returns a dict with the error code
        and filled in message.

        Args:

        Returns:
            dict: An error code with two keys -
            (1) "code" representing the error code, and (2) "message"
            representing a formatted error code with sections, sub-sections,
            data types and max lengths from the standard definition file
            in templated slots.

        Raises:

        """
        len_isvalid = self._validate_token_length()
        datatype_isvalid = self._validate_token_datatype()

        if self.missing:
            error_codes = ErrorCodes.E05.value
            return {
                "code": error_codes["code"],
                "message": error_codes["message_template"].format(
                    lx=self.lx, lxy=self.token_constraints["key"]
                ),
            }
        elif len_isvalid and datatype_isvalid:
            error_codes = ErrorCodes.E01.value
            return {
                "code": error_codes["code"],
                "message": error_codes["message_template"].format(
                    lx=self.lx, lxy=self.token_constraints["key"]
                ),
            }
        elif len_isvalid and not datatype_isvalid:
            error_codes = ErrorCodes.E02.value
            return {
                "code": error_codes["code"],
                "message": error_codes["message_template"].format(
                    lx=self.lx,
                    lxy=self.token_constraints["key"],
                    data_type=self.token_constraints["data_type"],
                    max_length=self.token_constraints["max_length"],
                ),
            }
        elif not len_isvalid and datatype_isvalid:
            error_codes = ErrorCodes.E03.value
            return {
                "code": error_codes["code"],
                "message": error_codes["message_template"].format(
                    lx=self.lx,
                    lxy=self.token_constraints["key"],
                    data_type=self.token_constraints["data_type"],
                    max_length=self.token_constraints["max_length"],
                ),
            }
        elif not len_isvalid and not datatype_isvalid:
            error_codes = ErrorCodes.E04.value
            return {
                "code": error_codes["code"],
                "message": error_codes["message_template"].format(
                    lx=self.lx, lxy=self.token_constraints["key"]
                ),
            }

    def process(self):
        """Processes a token based on the token constraints and returns
        a dictionary of data (based on a data contract defined below) to
        satisfy all analyses desired by the user.

        The token and token constraints are used to generate formatted error
        dictionaries (with error code and error message) and the information is
        combined into a data contract to satisfy all analyses
        (including the report and the summary)

        Args:

        Returns:
            dict: A dictionary containing report_data and summary_data required
            to satisfy all analyses.

        Raises:

        """
        # At this point, we have established that token and token_constraints
        # are lists that contain one entry each. Hence, we get the first
        # element of each list to make the resulting analysis
        # easier.
        if self.token:
            self.token = self.token[0].strip()
        if self.token_constraints is not None:
            self.token_constraints = self.token_constraints[0]

        error_codes = self._return_formatted_error_codes()

        # Adjust token length to match expected data contract.
        if len(self.token) == 0:
            length = ""
        else:
            length = len(self.token)

        return {
            "report_data": {
                "Section": self.lx,
                "Sub-Section": self.token_constraints["key"],
                "Given DataType": self._determine_token_datatype(),
                "Expected DataType": self.token_constraints["data_type"],
                "Given Length": length,
                "Expected MaxLength": self.token_constraints["max_length"],
                "Error Code": error_codes["code"],
            },
            "summary_data": {"Error Message": error_codes["message"]},
        }
