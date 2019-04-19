import logging
from xml.dom.minidom import parse
from .ediexceptions import EDIFileNotFoundError
from .edixmlparser import EDIXMLParser
from pkg_resources import resource_stream


class EDIValidator(EDIXMLParser):
    """
    EDI Validator validates edi segment against xml based map file
    """

    def __init__(self, map_file):
        """
        Initialize the edi reader
        """
        self.dataele = {}

        try:
            # Load data elements from xml files
            fd = resource_stream(__name__, 'map/data_ele.xml')
            element_spec = parse(fd)
            self.remove_whitespace_nodes(element_spec, True)

            for element in element_spec.documentElement.childNodes:
                self.dataele[element.getAttribute('id')] = {
                    'type': element.getAttribute('type'),
                    'min_length': element.getAttribute('min_length'),
                    'max_length': element.getAttribute('max_length')
                }
            fd.close()

        except OSError:
            logger = logging.getLogger('pyedi')
            logger.error('Element file or map file is missing in the package')
            raise EDIFileNotFoundError(
                'Element file or map file is missing in the package'
            )

        super().__init__(map_file)
