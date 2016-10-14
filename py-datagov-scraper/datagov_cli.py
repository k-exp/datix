#!/usr/bin/env python

if __name__ == '__main__':
    import datagovscraper.shell.catalog as catalog_sh
    from datagovscraper.catalog.filter import LocalFilter
    from datagovscraper.catalog.session import CatalogSession
    from datetime import datetime
    import sys
    import os
    import argparse

    parser = argparse.ArgumentParser(description=(
    '''
    data.gov shell client
    '''))

    parser.add_argument('routine', choices=[
                                        'catalog',
                                        'catalog_page',
                                        'api'
                                   ],
                                   help='cli routine to execute')

    parser.add_argument('-f', '--file', dest='filename',
                                        action='store',
                                        metavar='FILENAME',
                                        default=None,
                                        help='output file')

    parser.add_argument('-l', '--log', dest='logname',
                                        action='store',
                                        metavar='LOGNAME',
                                        default=None,
                                        help='log file')

    parser.add_argument('-t', '--filter', dest='filtername',
                                        action='store',
                                        metavar='FILTERNAME',
                                        default=None,
                                        help='name of filter key')

    parser.add_argument('-u', '--filterpath', dest='filterpath',
                                        action='store',
                                        metavar='FILTERPATH',
                                        default=None,
                                        help='path to filter yaml')

    parser.add_argument('-r', '--range', dest='rangestring',
                                        action='store',
                                        metavar='RANGE',
                                        default=None,
                                        help='range string M,N')

    parser.add_argument('-s', '--sleep', dest='throttle',
                                        action='store',
                                        type=float,
                                        metavar='SECONDS',
                                        default=None,
                                        help='sleep time per request')
    # args. see above
    args = parser.parse_args()

    # save cwd in order to write normalize results
    cwd = os.getcwd()

    # TODO: unique names
    # datetime.now().isoformat('-').split('.')[0]

    if args.routine == 'catalog':
        sess = CatalogSession()
        # TODO: load filter yaml if filter_path is provided,
        # lookup by given key. throw error if key dne.
        catalog_sh.run_catalog(sess, cwd,
            out_file=args.filename,
            log_file=args.logname,
            filter_url=None,
            range_string=args.rangestring,
            throttle=args.throttle)
    elif args.routine == 'catalog_page':
        pass
    elif args.routine == 'api':
        pass
    else:
        pass
