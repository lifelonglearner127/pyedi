from edivalidator import EDIValidator
from edisegment import EDISegment


class EDIReader:
    buf_size = 8 * 1024
    isa_len = 106

    def __init__(self, file_name, map_file):
        """
        Initialize the EDIReader

        @param file_path: absolute path of source file
        @type file_path: string
        """
        self.file_name = file_name

        # read the edi file
        self.file = open(self.file_name, 'r')
        line = self.file.read(self.isa_len)

        # check if edi file has correct interchange envelope format
        if line[:3] != 'ISA':
            raise Exception(
                "First line does not begin with 'ISA': {}".format(line[:3])
            )

        icvn = line[84:89]
        if icvn not in ('00501'):
            raise Exception(
                'ISA Interchange Control Version Number is unknown:'
                '{} for {}'.format(icvn, line)
            )

        self.icvn = icvn
        self.ele_term = line[3]
        self.seg_term = line[-1]
        self.subele_term = line[-2]
        self.repetition_term = line[82]
        self.buffer = line
        self.buffer += self.file.read(self.buf_size)
        self.validator = EDIValidator(map_file)

    def __iter__(self):
        while True:
            if self.buffer.find(self.seg_term) == -1:
                self.buffer += self.file.read(self.buf_size)
            if self.buffer.find(self.seg_term) == -1:
                break

            (line, self.buffer) = self.buffer.split(self.seg_term, 1)
            line = line.lstrip('\n\r')

            if line == '':
                break

            yield(EDISegment(line, self.ele_term))

    def validate(self):
        for segement in self:
            print(segement.toString())
