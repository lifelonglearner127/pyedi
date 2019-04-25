import argparse
import logging
from pyedi.xml2edi import XML2EDI


if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('-i', '--input', required=True,
                    help="Path to xml file")
    ap.add_argument('-o', '--output', default="856_edi.txt",
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
        xml_to_edi = XML2EDI(
            args['input'], args['output'],
            args['transaction'], args['version']
        )
        (result, err_log) = xml_to_edi.convert()
        if result is not None:
            logger.info("Successfully Parsed")
        else:
            logger.info(err_log)
    except Exception as err:
        logger.error(err)
