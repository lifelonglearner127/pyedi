import os
from pyedi.xml2edi import XML2EDI


class TestXML2EDI:
    def test_valid_856_edi(self):
        input_file = os.path.join(
            os.path.dirname(__file__),
            'documents/856/xml/valid.xml'
        )
        edi_to_xml = XML2EDI(
            input_file, 'output_valid.txt', 856, 5010
        )
        (result, err_log) = edi_to_xml.convert()
        assert result is not None and err_log is None

    def test_invalid_start_end_tag(self):
        input_file = os.path.join(
            os.path.dirname(__file__),
            'documents/856/xml/invalid_start_end_tag.xml'
        )
        edi_to_xml = XML2EDI(
            input_file, 'output_valid.txt', 856, 5010
        )
        (result, err_log) = edi_to_xml.convert()
        assert result is None and err_log is not None
        assert err_log == 'ISA should end with IEA trailer tag, but not found'

    def test_invalid_segment(self):
        input_file = os.path.join(
            os.path.dirname(__file__),
            'documents/856/xml/invalid_segment.xml'
        )
        edi_to_xml = XML2EDI(
            input_file, 'output_valid.txt', 856, 5010
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
            'documents/856/xml/invalid_element_length.xml'
        )
        edi_to_xml = XML2EDI(
            input_file, 'output_valid.txt', 856, 5010
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
            'documents/856/xml/invalid_element_value.xml'
        )
        edi_to_xml = XML2EDI(
            input_file, 'output_valid.txt', 856, 5010
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
            'documents/856/xml/invalid_element_value.xml'
        )
        edi_to_xml = XML2EDI(
            input_file, 'output_valid.txt', 856, 5010
        )
        (result, err_log) = edi_to_xml.convert()
        assert result is None and err_log is not None

        err_str = 'ST-Transaction Set Header, ' \
            'ST01 element value should be one of them - 856, ' \
            'but its value is 8856'
        assert err_log == err_str
