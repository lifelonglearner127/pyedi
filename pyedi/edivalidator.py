import logging
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
        self.dataele = {}
        fd = None
        try:
            # Load xml based map file
            with open(map_file, 'r') as fd:
                self.spec = parse(fd)
                self.remove_whitespace_nodes(self.spec, True)

            # Load data elements from xml files
            with open(element_file, 'r') as fd:
                self.element_spec = parse(fd)
                self.remove_whitespace_nodes(self.element_spec, True)

                for element in self.element_spec.documentElement.childNodes:
                    self.dataele[element.getAttribute('id')] = {
                        'type': element.getAttribute('type'),
                        'min_length': element.getAttribute('min_length'),
                        'max_length': element.getAttribute('max_length')
                    }

        except OSError:
            logger = logging.getLogger('pyedi')
            logger.error(
                'File Not Found: {} or {}'.format(map_file, element_file)
            )
            raise EDIFileNotFoundError(
                'Cannot find {} or {}'.format(map_file, element_file)
            )

    def remove_whitespace_nodes(self,  node, unlink=False):
        remove_list = []
        for child in node.childNodes:
            if child.nodeType == node.TEXT_NODE and \
               not child.data.strip():
                remove_list.append(child)
            elif child.hasChildNodes():
                self.remove_whitespace_nodes(child, unlink)
        for node in remove_list:
            node.parentNode.removeChild(node)
            if unlink:
                node.unlink()
