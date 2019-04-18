import os
import logging
from .edivalidator import EDIValidator
from .ediexceptions import EDIFileNotFoundError
from pkg_resources import resource_stream


class EDIReader:
    """
    Read edi file and validate it against xml based map file
    """

    isa_len = 106
    buf_size = 8 * 1024

    def __init__(self, file_name):
        """
        Initialize the edi reader

        @param file_name: path to edi file
        @type file_name: string
        """
        self.fd = None
        try:
            self.validator = EDIValidator('856.5010')
            
            self.fd = open(file_name, 'r')
            line = self.fd.read(self.isa_len)

            # TODO: ISA/FG Validation

        except OSError:
            logger = logging.getLogger('pyedi')
            logger.error('File Not Found: {}'.format(file_name))
            raise EDIFileNotFoundError(
                'Cannot find {}'.format(file_name)
            )

    def __del__(self):
        if self.fd is not None:
            self.fd.close()

    def validate(self):
        """
        Validate transaction
        """
        pass
