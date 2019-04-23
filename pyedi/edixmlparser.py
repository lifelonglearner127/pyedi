from xml.dom.minidom import parse
from .ediexceptions import EDIFileNotFoundError
from pkg_resources import resource_stream


class EDIXMLParser:
    """
    EDIXMLParser
    """

    def __init__(self, xml_file):
        """
        Initialize the edi xml parser
        """
        try:
            # Load xml file
            fd = resource_stream(__name__, 'map/{}'.format(xml_file))
            self.spec = parse(fd)
            self.remove_whitespace_nodes(self.spec, True)
            fd.close()

        except OSError:
            raise EDIFileNotFoundError(
                '{} is missing in the package'.format(xml_file)
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
