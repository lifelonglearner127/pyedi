class EDIReader:
    buf_size = 8 * 1024
    isa_len = 106

    def __init__(self, filename):
        """
        Initialize the EDIReader

        @param file_path: absolute path of source file
        @type file_path: string
        """
        self.filename = filename

        # read the edi file
        f = open(self.filename, 'r')
        line = f.read(self.isa_len)

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
        self.buffer += f.read(self.buf_size)

    def validate(self):
        return True
