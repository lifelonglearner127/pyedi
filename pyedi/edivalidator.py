from xml.dom.minidom import parse
from .ediexceptions import EDIFileNotFoundError, EDIElementLengthError, EDIElementTypeError, EDIElementValueError
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
            raise EDIFileNotFoundError(
                'Element file or map file is missing in the package'
            )

        super().__init__(map_file)
        self.next_node = self.spec.documentElement.firstChild
        self.build_segment_queue()

    def reset_has_occurred(self, node):
        nodes = node.getElementsByTagName('*')
        for element in nodes:
            element.setAttribute('has_occured', 0)

    def match_segment(self, edi_segment):
        match = False
        for spec_segment in self.segment_queue:
            if self.match_edi_segment(edi_segment, spec_segment):
                match = True
                break

        if match:
            self.next_node = spec_segment
            self.build_segment_queue()
            return True

        return False

    def match_edi_segment(self, edi_segment, spec_segment):
        if edi_segment.get_segment_id() != spec_segment.getAttribute('ref'):
            return False

        for (element, spec_element) in zip(edi_segment.elements, spec_segment.childNodes):
            spec_dataele = self.dataele[spec_element.getAttribute('id')]

            # Check Values
            possible_values = spec_element.getAttribute('values') if spec_element.hasAttribute('values') else None
            if possible_values is not None:
                if element not in possible_values.split(','):
                    raise EDIElementValueError(
                        '{} should be one of them - {}, but its value is {}'.format(
                            spec_element.getAttribute('ref'),
                            possible_values,
                            element
                        )
                    )

            # Check length 
            if (
                len(element) < int(spec_dataele['min_length']) or
                len(element) > int(spec_dataele['max_length'])
            ):
                raise EDIElementLengthError(
                    '{} should be between {} and {} in length, but it has {}'.format(
                        spec_element.getAttribute('ref'),
                        spec_dataele['min_length'],
                        spec_dataele['max_length'],
                        len(element)
                    )
                )
        
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
                raise EDIElementTypeError(
                    '{} should have {}-{} data type, but it has invalid type - {}'.format(
                        spec_element.getAttribute('ref'),
                        spec_dataele['type'],
                        type_str,
                        element
                    )
                )
        return True

    def build_segment_queue(self):
        self.segment_queue = []
        direction = "down"

        while True:
            if self.next_node.nodeType == self.next_node.TEXT_NODE:
                if self.next_node.nextSibling != None:
                    self.next_node = self.next_node.nextSibling
                else:
                    break

            if self.next_node.nodeName == "transaction":
                break

            elif self.next_node.nodeName == "loop":
                if direction == "down":
                    if (
                      not self.next_node.hasAttribute("has_occurred") or
                      int(self.nextNode.getAttribute("has_occurred")) < int(self.nextNode.getAttribute("repeat"))
                    ):
                        self.segment_queue.append(self.next_node.firstChild)
                        if (
                            self.next_node.firstChild.getAttribute("usage") == "M" and
                            (not self.next_node.firstChild.hasAttribute("has_occurred") or
                            self.next_node.firstChild.getAttribute("has_occurred") == 0)
                        ):
                            break
                            
                    if self.next_node.nextSibling != None:
                        direction = "down"
                        self.next_node = self.next_node.nextSibling
                    else:
                        direction = "up"
                        self.next_node = self.next_node.parentNode
                else:
                    if (self.next_node.childNodes.length > 1 and (self.next_node.getAttribute("repeat") == ">1" or int(self.next_node.getAttribute("has_occurred")) < int(self.next_node.getAttribute("repeat")))):
                        self.segment_queue.append(self.next_node.firstChild)
                        self.segment_queue[len(self.segment_queue) -  1].setAttribute("usage", "S")
                    if self.next_node.nextSibling != None:
                        direction = "down"
                        self.next_node = self.next_node.nextSibling
                    else:
                        direction = "up"
                        self.next_node = self.next_node.parentNode

            elif self.next_node.nodeName == "segment":
                if (
                      not self.next_node.hasAttribute("has_occurred") or
                      int(self.nextNode.getAttribute("has_occurred")) < int(self.nextNode.getAttribute("repeat"))
                    ):
                    self.segment_queue.append(self.next_node)

                if (
                    self.next_node.getAttribute("usage") == "M" and
                    (not self.next_node.hasAttribute("has_occurred") or
                    self.next_node.getAttribute("has_occurred") == 0)
                ):
                    break

                if self.next_node.nextSibling != None:
                    direction = "down"
                    self.next_node = self.next_node.nextSibling
                else:
                    direction = "up"
                    self.next_node = self.next_node.parentNode

                
