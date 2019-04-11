import logging
import argparse
from edireader import EDIReader


if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument("-f", "--file", required=True, help="path to the edi file")
    ap.add_argument("-d", "--debug", action="store_true")
    args = vars(ap.parse_args())

    # set up logging
    logger = logging.getLogger('pyedi')
    formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
    stdout_hdlr = logging.StreamHandler()
    stdout_hdlr.setFormatter(formatter)
    logger.addHandler(stdout_hdlr)
    logger.setLevel(logging.INFO)

    if args['debug']:
        logger.setLevel(logging.DEBUG)

    try:
        edi = EDIReader(args['file'])
    except Exception as e:
        logger.error(e.args)
        exit()

    print(edi.validate())
