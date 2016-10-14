#!/usr/bin/env python

import sys
import os
import argparse
import pandas as pd



def csvSelect(filepath, selectlist=[]):
    '''
    select the fields contained in selectlist
    '''
    if len(selectlist) == 0:
        raise Exception('csvSelect: empty projection')

    df = pd.read_csv(filepath)

    return df[selectlist]

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=(
    '''
    project over selected columns of a csv file. if no file is given,
    read in filelist from standard in.
    '''))

    parser.add_argument('-s', '--select', dest='selectlist',
                                        action='store',
                                        metavar='SELECTLIST',
                                        default='',
                                        help='select list')

    parser.add_argument('-f', '--file', dest='filename',
                                        action='store',
                                        metavar='FILENAME',
                                        default=None,
                                        help='input file')

    parser.add_argument('-v', '--verbose', dest='isverbose',
                                        action='store_true',
                                        default=False,
                                        help='verbose stderr output')
    # args. see above
    args = parser.parse_args()

    # save cwd in order to write normalize results
    cwd = os.getcwd()

    # parse list of csv columns to select
    selectlist = map(lambda x: x.strip(), args.selectlist.split(','))

    def go(filepath):
        # extract the name of file from path
        filename_withext = filepath.split('/')[-1]

        try:
            result = csvSelect(filepath, selectlist=selectlist)
            resultpath = os.path.join(cwd, 'SELECTION-'+filename_withext)
            result.to_csv(resultpath, index=False)
            sys.stdout.write("%s\n" % (resultpath,))
        except KeyError as ke: # bad -s flag
            if args.isverbose:
                sys.stderr.write("csv_select:KeyError:{0}: {1}\n".format( \
                    filename_withext, ke.args[0]))
        except IOError as ioe:
            if args.isverbose:
                sys.stderr.write("csv_select:IOError:{0}: {1}\n".format( \
                    filename_withext, ioe.args[0]))
        except: # unknown error
            if args.isverbose:
                raise

    if args.filename is None:
        # iterate through csv files piped in
        for line in sys.stdin.readlines():
            go(line.strip())
    else:
        go(args.filename)
