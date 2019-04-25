import os
from pyedi.edi2xml import EDI2XML


class TestEDI2XML:
    def test_valid_856_edi(self):
        input_file = os.path.join(
            os.path.dirname(__file__),
            'documents/856/edi/valid.txt'
        )
        edi_to_xml = EDI2XML(
            input_file, 'output_valid.xml', 856, 5010
        )
        (result, err_log) = edi_to_xml.convert()
        assert result is not None and err_log is None

    def test_invalid_start_end_tag(self):
        input_file = os.path.join(
            os.path.dirname(__file__),
            'documents/856/edi/invalid_start_end_tag.txt'
        )
        edi_to_xml = EDI2XML(
            input_file, 'output_valid.xml', 856, 5010
        )
        (result, err_log) = edi_to_xml.convert()
        assert result is None and err_log is not None
        assert err_log == 'ISA should end with IEA trailer tag, but not found'

    def test_invalid_segment(self):
        input_file = os.path.join(
            os.path.dirname(__file__),
            'documents/856/edi/invalid_segment.txt'
        )
        edi_to_xml = EDI2XML(
            input_file, 'output_valid.xml', 856, 5010
        )
        (result, err_log) = edi_to_xml.convert()
        assert result is None and err_log is not None

        err_str = 'Found segment: T. This segment might be ' \
            'incorrect or a mandatory segment is missing '
        err_str += '\nMandatory segments is ST - Transaction Set Header'

        assert err_log == err_str

    def test_invalid_element_length(self):
        input_file = os.path.join(
            os.path.dirname(__file__),
            'documents/856/edi/invalid_element_length.txt'
        )
        edi_to_xml = EDI2XML(
            input_file, 'output_valid.xml', 856, 5010
        )
        (result, err_log) = edi_to_xml.convert()
        assert result is None and err_log is not None

        err_str = 'ST-Transaction Set Header, ' \
            'ST02 element should be between 4 and 9 in length, ' \
            'but its length is 1'
        assert err_log == err_str

    def test_invalid_element_value(self):
        input_file = os.path.join(
            os.path.dirname(__file__),
            'documents/856/edi/invalid_element_value.txt'
        )
        edi_to_xml = EDI2XML(
            input_file, 'output_valid.xml', 856, 5010
        )
        (result, err_log) = edi_to_xml.convert()
        assert result is None and err_log is not None

        err_str = 'ST-Transaction Set Header, ' \
            'ST01 element value should be one of them - 856, ' \
            'but its value is 8856'
        assert err_log == err_str

    def test_invalid_element_type(self):
        input_file = os.path.join(
            os.path.dirname(__file__),
            'documents/856/edi/invalid_element_value.txt'
        )
        edi_to_xml = EDI2XML(
            input_file, 'output_valid.xml', 856, 5010
        )
        (result, err_log) = edi_to_xml.convert()
        assert result is None and err_log is not None

        err_str = 'ST-Transaction Set Header, ' \
            'ST01 element value should be one of them - 856, ' \
            'but its value is 8856'
        assert err_log == err_str
