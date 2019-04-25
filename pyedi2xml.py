import argparse
import logging
from pyedi.edireader import EDIReader


if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('-f', '--file', required=True,
                    help="Path to edi file")
    ap.add_argument('-o', '--output', default="856_output.xml",
                    help="Path to output file")
    ap.add_argument('-t', '--transaction', required=True,
                    help="Specify EDI Transaction(eg, 856)")
    ap.add_argument('-v', '--version', required=True,
                    help="Specify EDI version(eg, 5010)")
    args = vars(ap.parse_args())

    # Configure Logging
    logger = logging.getLogger('pyedi')
    formatter = logging.Formatter('[%(levelname)s] %(message)s')
    stdout_hdlr = logging.StreamHandler()
    stdout_hdlr.setFormatter(formatter)
    logger.addHandler(stdout_hdlr)
    logger.setLevel(logging.INFO)

    logger.info('Started Parsing the EDI Standard')

    try:
        edi_reader = EDIReader(
            args['file'], args['transaction'], args['version']
        )
        if edi_reader.validate():
            logger.info("Successfully Parsed")
            xml_file = open(args['output'], "w", encoding="utf-8")
            edi_reader.validator.data_document.writexml(xml_file, "\n", "\t")
    except Exception as err:
        logger.error(err)
