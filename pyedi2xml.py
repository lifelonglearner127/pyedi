import argparse
from pyedi.edireader import EDIReader


if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('-f', '--file', required=True, help="Path to edi file")
    ap.add_argument('-d', '--debug', action='store_false',
                    help='Set debug mode')

    args = vars(ap.parse_args())

    try:
        edi_reader = EDIReader(args['file'])
    except Exception as err:
        print('{}'.format(err))
