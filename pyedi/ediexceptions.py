class EDIError(Exception):
    """Class for EDI"""
    pass


class EDIFileNotFoundError(EDIError):
    """Class for EDI Validator errors"""
    pass


# Envelope Error Classess
class EnvelopeError(EDIError):
    """Class for Envelope"""
    pass


class InterchangeControlError(EnvelopeError):
    """Class for interchange control errors"""
    pass


class FunctionalGroupError(EnvelopeError):
    """Class for functional group errors"""
    pass


# Transaction Error Classess
class TransactionError(EDIError):
    """Class for Transaction"""
    pass


class EDISegmentError(TransactionError):
    """Class for EDISegment"""
    pass


class EDIElementValueError(EDISegmentError):
    """Class for EDIElementValue"""
    pass


class EDIElementLengthError(EDISegmentError):
    """Class for EDIElementLength"""
    pass


class EDIElementTypeError(EDISegmentError):
    """Class for EDIElementType"""
    pass

class EDIElementNotExist(EDISegmentError):
    """Class for EDIElementNotExist"""
    pass
