class EDISegmentError(Exception):
    """Class for EDISegment"""
    pass


class EDIFileNotFoundError(Exception):
    """Class for EDI Validator errors"""
    pass


class InterchangeControlError(Exception):
    """Class for interchange control errors"""
    pass


class FunctionalGroupError(Exception):
    """Class for functional group errors"""
    pass
