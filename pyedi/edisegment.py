
class EDISegment:
    """
    EDISegment
    """

    elements = []
    delimiter = '*'

    def __init__(self, seg_str, delimiter):
        self.delimiter = delimiter
        self.elements = seg_str.split(delimiter)

    def get_element_by_index(self, index):
        try:
            return self.elements[index]
        except:
            return None

    def to_string(self):
        return self.delimiter.join(self.elements)

    def get_segment_id(self):
        return self.get_element_by_index(0)
