import re
import logging
from .ediexceptions import EDISegmentError


class EDISegment:
    """
    EDISegment
    """
    re_seg_id = '(?P<seg_id>[A-Z][A-Z0-9]{1,2})?'
    re_ele_idx = '(?P<ele_idx>[0-9]{2})?'
    re_str = '^%s%s$' % (re_seg_id, re_ele_idx)
    rec_path = re.compile(re_str, re.S)

    def __init__(self, seg_str, delimiter):
        self.delimiter = delimiter
        self.elements = seg_str.split(delimiter)
        self.seg_id = None

        if self.elements:
            self.seg_id = self.elements[0]

    def get_element_by_index(self, index):
        try:
            return self.elements[index]
        except IndexError:
            return None

    def get_element_by_ref(self, ref):
        m = EDISegment.rec_path.search(ref)
        if m is not None:
            seg_id = m.group('seg_id')
            ele_idx = m.group('ele_idx')
            try:
                ele_idx = int(ele_idx)
            except ValueError:
                logger = logging.getLogger('pyedi')
                logger.error('Failed to getting element value')
                raise EDISegmentError('Failed to getting element value')

            if seg_id != self.seg_id:
                logger = logging.getLogger('pyedi')
                logger.error('Faile to getting element value')
                raise EDISegmentError('Failed to getting element value')
            return (seg_id, ele_idx)
        else:
            return None

    def to_string(self):
        return self.delimiter.join(self.elements)

    def get_segment_id(self):
        return self.seg_id
