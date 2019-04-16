import xml.dom.minidom
from xml.dom.minidom import getDOMImplementation


class EDIValidator:
    def __init__(self, file_name):
        self.file_name = file_name
        self.spec = xml.dom.minidom.parse(file_name)


if __name__ == '__main__':
    pass
