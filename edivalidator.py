import xml.dom.minidom
from xml.dom.minidom import getDOMImplementation


class EDIValidator:
    def __init__(self, file_name):
        self.file_name = file_name
        self.spec = xml.dom.minidom.parse(file_name)
        self.remove_whitespace_nodes(self.spec, True)

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

if __name__ == '__main__':
    pass
