import logging
from .edivalidator import EDIValidator
from .edisegment import EDISegment
from .ediexceptions import EDIFileNotFoundError, InterchangeControlError


logger = logging.getLogger('pyedi')


class EDI2XML:
    """
    Convert edi document to xml
    """

    ISA_LEN = 106
    BUF_SIZE = 8 * 1024

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
        self.fd = None
        self.output_file = output_file

        try:
            self.fd = open(input_file, 'r')
            line = self.fd.read(EDI2XML.ISA_LEN)

            if line[:3] != 'ISA':
                raise InterchangeControlError(
                    "First line does not begin with 'ISA': %s" % line[:3]
                )

            self.icvn = line[84:89]
            if self.icvn not in ('00501'):
                raise InterchangeControlError(
                    'ISA Interchange Control Version Number is unknown:'
                    '%s for %s' % (self.icvn, line)
                )

            self.segment_delimiter = line[-1]
            self.element_delimiter = line[3]
            self.subelement_delimiter = line[-2]
            self.repetition_delimiter = (
                line[82] if self.icvn == '00501' else None
            )
            self.buffer = line
            self.buffer += self.fd.read(EDI2XML.BUF_SIZE)
            self.validator = EDIValidator(
                'transaction/{}.{}.xml'.format(transaction, version)
            )
        except OSError:
            raise EDIFileNotFoundError('File Not Found: {}'.format(input_file))

    def __del__(self):
        if self.fd is not None:
            self.fd.close()

    def __iter__(self):
        while True:
            if self.buffer.find(self.segment_delimiter) == -1:
                self.buffer += self.fd.read(EDI2XML.BUF_SIZE)

            if self.buffer.find(self.segment_delimiter) == -1:
                break

            (line, self.buffer) = self.buffer.split(self.segment_delimiter, 1)
            line = line.lstrip('\n\r')

            if line == '':
                break

            yield(EDISegment(line, self.element_delimiter))

    def convert(self):
        """
        convert transaction
        """

        # check if the segment has valid rule
        for segment in self:
            logger.info('Parsing segment: {}'.format(
                segment.to_string()
            ))

            try:
                (valid, segments) = self.validator.match_segment(segment)

                if not valid:
                    err_str = 'Found segment: {}. This segment might be ' \
                        'incorrect or a mandatory segment is missing '.format(
                            segment.get_segment_id()
                        )

                    err_str += '\nMandatory segments is {} - {}'.format(
                            segments[0].getAttribute('ref'),
                            segments[0].getAttribute('name')
                        )

                    if len(segments) > 1:
                        err_str += '\nOther possible segment are '

                    for possible_seg in segments[1:]:
                        err_str += '{}-{}, '.format(
                            possible_seg.getAttribute('ref'),
                            possible_seg.getAttribute('name')
                        )

                    return (None, err_str)
            except Exception as err:
                return (None, str(err))

        # check if edi document has segment pairs
        close_tags = self.validator.get_close_tags()
        for ((start_tag, close_tag)) in close_tags:
            err_str = '{} should end with {} trailer tag, ' \
                'but not found'.format(start_tag, close_tag)
            return (None, err_str)

        xml_file = open(self.output_file, "w", encoding="utf-8")
        self.validator.data_document.writexml(xml_file, "\n", "\t")
        xml_file.close()
        return (self.validator.data_document, None)
