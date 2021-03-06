from .edivalidator import EDIValidator
from .edisegment import EDISegment
from .edimaps import EDIMap
from .ediexceptions import EDIFileNotFoundError, InterchangeControlError


class EDIReader:
    """
    Read edi file and validate it against xml based map file
    """

    ISA_LEN = 106
    BUF_SIZE = 8 * 1024

    def __init__(self, file_name):
        """
        Initialize the edi reader

        @param file_name: path to edi file
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
            self.envelope_validator = EDIValidator(
                'envelope/{}.xml'.format(self.icvn)
            )
            self.transaction_validator = None
            self.maps = EDIMap()

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
        valid = False
        for segment in self:
            segment_id = segment.get_segment_id()
            if segment_id not in ['ISA', 'GS', 'GE', 'IEA']:
                valid = self.transaction_validator.match_segment(segment)

            else:
                valid = self.envelope_validator.match_segment(segment)

            if segment_id == 'GS':
                fic = segment.get_element_by_ref('GS01')
                vriic = segment.get_element_by_ref('GS08')
                self.maps.get_file_name(self.icvn, fic, vriic)

            if not valid:
                break

        return valid
