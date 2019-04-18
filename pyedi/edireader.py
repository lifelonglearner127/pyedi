import logging
from .edivalidator import EDIValidator
from .ediexceptions import EDIFileNotFoundError


class EDIReader:
    """
    Read edi file and validate it against xml based map file
    """

    isa_len = 106
    buf_size = 8 * 1024

    def __init__(self, file_name, map_file, element_file):
        """
        Initialize the edi reader

        @param file_name: path to edi file
        @type file_name: string
        @param map_file: path to map file
        @type map_file: string
        @param element_file: path to element file
        @type element_file: string
        """
        
        try:
            self.fd = open(file_name, 'r')
            line = self.fd.read(self.isa_len)

            # TODO: ISA/FG Validation
            
            self.validator = EDIValidator(map_file, element_file)

        except OSError as err:
            logger = logging.getLogger('pyedi')
            logger.error('File Not Found: {}'.format(file_name))
        
        except EDIFileNotFoundError as err:
            logger = logging.getLogger('pyedi')
            logger.error('EDIFileNotFoundError: {}'.format(err))

    def __del__(self):
        self.fd.close

    def validate_transaction(self):
        """
        Validate transaction
        """
        pass

    def validate_envelope(self, envelop):
        """
        Validate Interchange Envelope and Functional Group
        """
        pass