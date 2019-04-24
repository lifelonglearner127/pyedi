from xml.dom.minidom import parse
from pkg_resources import resource_stream
from .ediexceptions import (
    EDIFileNotFoundError, EDIElementLengthError,
    EDIElementTypeError, EDIElementValueError, EDIElementNotExist
)


class EDIValidator:
    """
    EDI Validator validates edi segment against xml based map file
    """

    def __init__(self, map_file):
        """
        Initialize the edi reader
        """
        self.dataele = {}

        try:
            # Load xml file
            fd = resource_stream(__name__, 'map/{}'.format(map_file))
            self.spec = parse(fd)
            self.remove_whitespace_nodes(self.spec, True)
            fd.close()

            # Load data elements from xml files
            fd = resource_stream(__name__, 'map/data_ele.xml')
            element_spec = parse(fd)
            self.remove_whitespace_nodes(element_spec, True)
            fd.close()

            for element in element_spec.documentElement.childNodes:
                self.dataele[element.getAttribute('id')] = {
                    'type': element.getAttribute('type'),
                    'min_length': element.getAttribute('min_length'),
                    'max_length': element.getAttribute('max_length')
                }

        except OSError:
            raise EDIFileNotFoundError(
                'Element file or map file is missing in the package'
            )

        self.next_node = self.spec.documentElement.firstChild
        self.build_segment_queue()

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

    def reset_has_occurred(self, node):
        nodes = node.getElementsByTagName('*')
        for element in nodes:
            element.setAttribute('has_occurred', 0)

    def match_segment(self, edi_segment):
        match = False
        for spec_segment in self.segment_queue:
            if self.match_edi_segment(edi_segment, spec_segment):
                match = True
                break

        if match:
            self.next_node = spec_segment

            parent_node = spec_segment.parentNode
            if (
                parent_node.nodeName == "loop" and
                parent_node.firstChild.isSameNode(spec_segment)
            ):
                self.reset_has_occurred(spec_segment.parentNode)
                if parent_node.hasAttribute("has_occurred"):
                    parent_node.setAttribute(
                        "has_occurred",
                        int(parent_node.getAttribute("has_occurred")) + 1
                    )
                else:
                    parent_node.setAttribute("has_occurred", 1)

            if spec_segment.hasAttribute('has_occurred'):
                spec_segment.setAttribute(
                    "has_occurred",
                    int(spec_segment.getAttribute("has_occurred")) + 1
                )
            else:
                spec_segment.setAttribute("has_occurred", 1)

            self.build_segment_queue()
            return True

        return False

    def match_edi_segment(self, edi_segment, spec_segment):
        if edi_segment.get_segment_id() != spec_segment.getAttribute('ref'):
            return False

        if edi_segment.get_segment_id() == 'HL':
            hl03_value = edi_segment.get_element_by_index(2)
            hl03_values = spec_segment.childNodes[2].getAttribute('values')
            if hl03_value not in hl03_values:
                return False

        for (element, spec_element)\
                in zip(edi_segment.elements, spec_segment.childNodes):

            if (
                spec_element.getAttribute('usage') != 'M' and
                element == ''
            ):
                continue
            err_str = 'Error occurred while parsing {}-{}\n'.format(
                edi_segment.get_segment_id(),
                spec_element.getAttribute('ref'),
            )

            try:
                spec_dataele = self.dataele[spec_element.getAttribute('id')]
            except KeyError:
                err_str += 'Element id should be {}, but it does not exist' \
                    ' in the package'.format(spec_element.getAttribute('id'))
                raise EDIElementNotExist(err_str)

            # Check Values
            possible_values = spec_element.getAttribute('values') \
                if spec_element.hasAttribute('values') else None
            if possible_values is not None:
                if element not in possible_values.split(','):
                    err_str += 'Element value should be one of them - {}, ' \
                        'but its value is {}'.format(
                            possible_values,
                            element
                        )
                    raise EDIElementValueError(err_str)

            # Check length
            if (
                len(element) < int(spec_dataele['min_length']) or
                len(element) > int(spec_dataele['max_length'])
            ):
                err_str += 'Element should be between {} and {} in length, ' \
                    'but its length is {}'.format(
                        spec_dataele['min_length'],
                        spec_dataele['max_length'],
                        len(element)
                    )
                raise EDIElementLengthError(err_str)

            # Check data type
            type_error = False
            type_str = ""
            if (
                spec_dataele['type'][0] == 'N'
            ):                                  # Numeric
                type_str = "Numeric"
            elif spec_dataele['type'] == 'R':   # Decimal number
                type_str = "Decimal number"
            elif spec_dataele['type'] == 'ID':  # Identifier data type
                type_str = "Identifier"
            elif spec_dataele['type'] == 'AN':  # String data type
                type_str = "String"
            elif spec_dataele['type'] == 'DT':  # Date data type
                type_str = "Date"
            elif spec_dataele['type'] == 'TM':  # Time data type
                type_str = "Time"

            if type_error:
                err_str += 'Element should have {} data type, ' \
                    'but its type is {}'.format(
                        type_str,
                        type_str
                    )
                raise EDIElementTypeError(err_str)
        return True

    def build_segment_queue(self):
        self.segment_queue = []
        direction = "down"

        while True:
            if self.next_node.nodeType == self.next_node.TEXT_NODE:
                if self.next_node.nextSibling is not None:
                    self.next_node = self.next_node.nextSibling
                else:
                    break

            if self.next_node.nodeName == "transaction":
                break

            else:
                if direction == "down":
                    segment = self.next_node.firstChild \
                        if self.next_node.nodeName == 'loop' \
                        else self.next_node

                    if (
                        self.next_node.getAttribute("repeat") == '>1' or
                        not self.next_node.getAttribute("has_occurred") or
                        int(self.next_node.getAttribute("has_occurred")) <
                        int(self.next_node.getAttribute("repeat"))
                    ):
                        self.segment_queue.append(segment)

                    if (
                        segment.getAttribute('usage') == 'M' and
                        (
                            not segment.getAttribute('has_occurred') or
                            segment.getAttribute('has_occurred') == 0
                        )
                    ):
                        break

                elif direction == "up" and self.next_node.nodeName == 'loop':
                    if (
                        self.next_node.getAttribute("repeat") == ">1" or
                        int(self.next_node.getAttribute('has_occurred')) <
                        int(self.next_node.getAttribute('repeat'))
                    ):
                        self.segment_queue.append(self.next_node.firstChild)

                if self.next_node.nextSibling is not None:
                    direction = "down"
                    self.next_node = self.next_node.nextSibling
                else:
                    direction = "up"
                    self.next_node = self.next_node.parentNode
