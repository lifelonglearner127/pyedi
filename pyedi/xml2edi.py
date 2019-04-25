import logging
from xml.dom.minidom import parse
from pyedi.edisegment import EDISegment
from pyedi.edivalidator import EDIValidator


logger = logging.getLogger('pyedi')


class XML2EDI:
    SEGMENT_DELIMITER = '~'
    ELEMENT_DELIMITER = '*'
    SUBELEMENT_DELIMITER = '>'

    def __init__(self, input_file, output_file, transaction, version):
        """
        Initialize the edi reader

        @param input_file: path to edi file
        @type input_file: string
        @param output_file: path to output xml file
        @type output_file: string
        @param transaction: edi transaction
        @type transaction: string
        @param version: edi transaction version
        @type version: string
        """
        self.output_file = output_file
        xml_edi = parse(input_file)
        self.remove_whitespace_nodes(xml_edi, True)
        self.segments = []
        self.build_segments(xml_edi.getElementsByTagName("segment"))
        self.validator = EDIValidator(
            'transaction/{}.{}.xml'.format(transaction, version)
        )

    def remove_whitespace_nodes(self,  node, unlink=False):
        """
        remove whitespace nodes
        """

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

    def build_segments(self, segment_nodes):
        for segment_node in segment_nodes:
            elements = []
            elements.append(segment_node.getAttribute('ref'))
            for child in segment_node.childNodes:
                elements.append(child.getAttribute('value'))

            self.segments.append(
                EDISegment(
                    XML2EDI.ELEMENT_DELIMITER.join(elements),
                    XML2EDI.ELEMENT_DELIMITER
                )
            )

    def convert(self):
        edi_string = ''
        for segment in self.segments:
            logger.info('Parsing segment: {}'.format(
                segment.to_string()
            ))

            (valid, err_str) = self.validator.match_segment(segment)

            if not valid:
                return (None, err_str)

            edi_string += segment.to_string()
            edi_string += XML2EDI.SEGMENT_DELIMITER + '\n'

        # check if edi document has segment pairs
        close_tags = self.validator.get_close_tags()
        for ((start_tag, close_tag)) in close_tags:
            err_str = '{} should end with {} trailer tag, ' \
                'but not found'.format(start_tag, close_tag)
            return (None, err_str)

        edi_file = open(self.output_file, "w")
        edi_file.write(edi_string)
        edi_file.close()
        return (edi_string, None)
