import argparse
import logging
from pyedi.edi2xml import EDI2XML


if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('-i', '--input', required=True,
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
        edi_to_xml = EDI2XML(
            args['input'], args['output'], 
            args['transaction'], args['version']
        )
        result = edi_to_xml.convert()
        if result is not None:
            logger.info("Successfully Parsed")
    except Exception as err:
        logger.error(err)
