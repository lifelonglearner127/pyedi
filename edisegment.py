class EDISegment:

    def __init__(self, seg_str, delimiter):
        self.delimiter = delimiter
        self.elements = seg_str.split(delimiter)

    def getElementByIndex(self, idx):
        try:
            return self.elements[idx]
        except IndexError:
            return ''

    def getSegmentId(self):
        return self.getElementByIndex(0)

    def toString(self):
        return self.delimiter.join(self.elements)


if __name__ == '__main__':
    pass
