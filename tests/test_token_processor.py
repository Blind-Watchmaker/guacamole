from utils import DataTypes


# Unusually, testing a private method. I specifically
# wanted to make sure the OTHER datatype runs correctly.
def test_determine_token_datatype_other(token_processor):
    dtype = token_processor._determine_token_datatype()
    assert dtype == DataTypes.OTHER.value
