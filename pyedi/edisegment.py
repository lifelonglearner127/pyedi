import re
from .ediexceptions import EDISegmentError


class EDISegment:
    """
    EDISegment
    """
    re_seg_id = '(?P<seg_id>[A-Z][A-Z0-9]{1,2})?'
    re_ele_idx = '(?P<ele_idx>[0-9]{2})?'
    re_str = '^%s%s$' % (re_seg_id, re_ele_idx)
    rec_path = re.compile(re_str, re.S)

    def __init__(self, segment_string, delimiter):
        """
        Initialize segment conf
        """
        self.segment_id = None
        self.delimiter = delimiter
        self.segment_string = segment_string
        self.elements = segment_string.split(delimiter)

        if self.elements:
            self.segment_id = self.elements.pop(0)

    def get_element_by_index(self, index):
        """
        Return element value by index
        """
        try:
            return self.elements[index]
        except IndexError:
            return None

    def get_element_by_ref(self, ref):
        """
        Return element (value, index) tuple by ref

        @param ref: reference to element for example, GS01
        @type ref: string
        """
        m = EDISegment.rec_path.search(ref)
        if m is not None:
            seg_id = m.group('seg_id')
            ele_idx = m.group('ele_idx')
            try:
                ele_idx = int(ele_idx)
            except ValueError:
                raise EDISegmentError('Failed to getting element value')

            if seg_id != self.segment_id:
                raise EDISegmentError('Failed to getting element value')
            return (seg_id, ele_idx)
        else:
            return None

    def to_string(self):
        return self.segment_string

    def get_segment_id(self):
        return self.segment_id
