from xml.dom.minidom import parse
from .ediexceptions import EDIFileNotFoundError


class EDIValidator:
    """
    EDI Validator validates edi segment against xml based map file
    """
    
    def __init__(self, map_file, element_file):
        """
        Initialize the edi reader

        @param map_file: path to map file
        @type map_file: string
        @param element_file: path to element file
        @type element_file: string
        """
        try:
            fd = open(map_file, 'r')
            self.spec = parse(fd)
        except OSError:
            raise EDIFileNotFoundError('{}'.format(map_file))

        try:
            fd = open(element_file, 'r')
            self.element_spec = parse(fd)
        except OSError:
            raise EDIFileNotFoundError('{}'.format(element_file))