import logging
from .edivalidator import EDIValidator
from .edisegment import EDISegment
from .ediexceptions import EDIFileNotFoundError, InterchangeControlError


logger = logging.getLogger('pyedi')


class EDIReader:
    """
    Read edi file and validate it against xml based map file
    """

    ISA_LEN = 106
    BUF_SIZE = 8 * 1024

    def __init__(self, file_name, transaction, version):
        """
        Initialize the edi reader

        @param file_name: path to edi file
        @type file_name: string
        @param transaction: edi transaction
        @type transaction: string
        @param file_name: edi transaction version
        @type file_name: string
        """
        self.fd = None

        try:
            self.fd = open(file_name, 'r')
            line = self.fd.read(EDIReader.ISA_LEN)

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
            self.buffer += self.fd.read(EDIReader.BUF_SIZE)
            self.validator = EDIValidator(
                'transaction/{}.{}.xml'.format(transaction, version)
            )

        except OSError:
            raise EDIFileNotFoundError('File Not Found: {}'.format(file_name))

    def __del__(self):
        if self.fd is not None:
            self.fd.close()

    def __iter__(self):
        while True:
            if self.buffer.find(self.segment_delimiter) == -1:
                self.buffer += self.fd.read(EDIReader.BUF_SIZE)

            if self.buffer.find(self.segment_delimiter) == -1:
                break

            (line, self.buffer) = self.buffer.split(self.segment_delimiter, 1)
            line = line.lstrip('\n\r')

            if line == '':
                break

            yield(EDISegment(line, self.element_delimiter))

    def validate(self):
        """
        Validate transaction
        """

        valid = True
        # check if the segment has valid rule
        for segment in self:
            logger.info('Parsing segment: {}'.format(
                segment.to_string()
            ))

            (valid, segments) = self.validator.match_segment(segment)

            if not valid:
                logger.error(
                    'Found segment: {}. This segment might be incorrect'
                    ' or a mandatory segment is missing '.format(
                        segment.get_segment_id()
                    )
                )

                logger.error(
                    'Mandatory segments is {} - {}'.format(
                        segments[0].getAttribute('ref'),
                        segments[0].getAttribute('name')
                    )
                )
                err_str = 'Other possible segment are '

                for possible_seg in segments[1:]:
                    err_str += '{}-{}, '.format(
                        possible_seg.getAttribute('ref'),
                        possible_seg.getAttribute('name')
                    )
                logger.error(err_str)
                return False

        # check if edi document has segment pairs
        close_tags = self.validator.get_close_tags()
        for ((start_tag, close_tag)) in close_tags:
            logger.error(
                '{} should end with {} trailer tag, but not found'.
                format(start_tag, close_tag)
            )
            valid = False

        return valid
