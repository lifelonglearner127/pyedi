import logging
from xml.dom.minidom import parse
from .ediexceptions import EDIFileNotFoundError
from pkg_resources import resource_stream


class EDIValidator:
    """
    EDI Validator validates edi segment against xml based map file
    """

    def __init__(self, map_file):
        """
        Initialize the edi reader
        """
        self.map_file = map_file
        self.dataele = {}

        try:
            # Load xml based map file
            fd = resource_stream(
                __name__, 'map/transaction/{}.xml'.format(map_file)
            )
            self.spec = parse(fd)
            self.remove_whitespace_nodes(self.spec, True)
            fd.close()

            # Load data elements from xml files
            fd = resource_stream(__name__, 'map/data_ele.xml')
            self.element_spec = parse(fd)
            self.remove_whitespace_nodes(self.element_spec, True)

            for element in self.element_spec.documentElement.childNodes:
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
