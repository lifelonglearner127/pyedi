import logging
from xml.dom.minidom import parse
from .ediexceptions import EDIFileNotFoundError
from pkg_resources import resource_stream


class EDIValidator:
    """
    EDI Validator validates edi segment against xml based map file
    """

    def __init__(self, map_file=None, element_file=None):
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
            if map_file is not None:
                fd = open(map_file, 'r')
            else:
                fd = resource_stream(__name__, 'map/856.5010.xml')

            self.spec = parse(fd)
            self.remove_whitespace_nodes(self.spec, True)
            fd.close()

            # Load data elements from xml files
            if element_file is not None:
                fd = open(element_file, 'r')
            else:
                fd = resource_stream(__name__, 'map/data_ele.xml')

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
            logger.error('Element file or map file are missing')
            raise EDIFileNotFoundError('Element file or map file are missing')
        
        finally:
            if fd is not None and not fd.closed:
                fd.close()

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
