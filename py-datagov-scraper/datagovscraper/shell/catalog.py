import os
import codecs
import json
import time

def _parseRange(rangestring):
    rnglist = map(lambda x: x.strip(), rangestring.split(','))
    if len(rnglist) != 2:
        raise Exception('invalid range string')
    lbound = int(rnglist[0])
    ubound = int(rnglist[1])
    if lbound == ubound:
        raise Exception('empty range')
    if lbound > ubound:
        raise Exception('invalid range M > N')
    return (lbound, ubound)

def _catalog_sess_loop(sess, outfile, logfile, throttle=0):
    while True:
        if(throttle != 0):
            time.sleep(throttle)

        iterSuccess = True
        hasMore = False
        try:
            sess.extract_page_ds_descriptions()
        except:
            iterSuccess = False

        if iterSuccess:
            res = sess._current_page_scrape_results
            outfile.write(json.dumps(res))
            outfile.write('\n')
            logfile.write("SUCCESS:PAGE-{0}\n".format(sess.current_page))
        else:
            logfile.write("FAIL:PAGE-{0}\n".format(sess.current_page))

        try:
            hasMore = sess.next()
        except:
            hasMore = False
            logfile.write("FAIL:NEXT\n")

        if not hasMore:
            logfile.write("DONE\n")
            break



def run_catalog_maxpage(sess_instance,
                        cwd,
                        out_file=None,
                        log_file=None,
                        filter_url=None):
    """
    return the max page of a scrape session
    TODO: filter object should be handled by caller

    Parameters
    ----------
    sess_instance : catalog.session.CatalogSession
        CatalogSession initialized by the caller
    cwd : str
        current working directory to save outfiles and logfiles to (if
        out and log are specified).
    out_file : str, optional
        name of output file. if omitted, pipe the result to stdout. if
        provided, each result is a single line appended to the utf-8
        encoded file
    log_file : str, optional
        name of log file. if omitted, result metadata is silent. if provided,
        metadata of result is a single line appended to the utf-8 encoded file
    filter_url : str, optional
        catalog filter url. loaded with yaml file by caller.
    """
    pass

def run_catalog(sess_instance,
                cwd,
                out_file=None,
                log_file=None,
                filter_url=None,
                range_string=None,
                throttle=None):
    """
    execute a catalog scraper session
    TODO: filter object should be handled by caller

    Parameters
    ----------
    sess_instance : catalog.session.CatalogSession
        CatalogSession initialized by the caller
    cwd : str
        current working directory to save outfiles and logfiles to (if
        out and log are specified).
    out_file : str, optional
        name of output file. if omitted, pipe the result of each request to
        stdout. if provided, each result of a page scrape is a single line
        appended to the utf-8 encoded file
    log_file : str, optional
        name of log file. if omitted, all scrape result metadata is silent. if
        provided, metadata of each result of a page scrape is a single line
        appended to the utf-8 encoded file
    filter_url : str, optional
        catalog filter url. loaded with yaml file by caller.
    range_string : str, optional
        pagination range to scrape. if ommited, scrape pages 1, MAX. if
        provided, format should be M,N where M,N : int and M < N
    throttle : int, optional
        sleep time between requests
    """

    isPipeStdout = out_file is None
    isSilent = log_file is None
    hasRange = range_string is not None
    hasThrottle = throttle is not None

    outFileFullPath = None
    if not isPipeStdout:
        outFileFullPath = os.path.join(cwd, out_file)

    logFileFullPath = None
    if not isSilent:
        logFileFullPath = os.path.join(cwd, log_file)

    rangeParam = None
    if hasRange:
        rangeParam = _parseRange(range_string)

    throttleParam = 0
    if hasThrottle:
        throttleParam = throttle

    if filter_url is None:
        sess_instance.configure(page_range=rangeParam)
    else:
        sess_instance.configure(filter_url=filter_url,
                                page_range=rangeParam)

    # for the time being, only continue if files are specified
    if isPipeStdout or isSilent:
        raise Exception('TODO: Stdout and Silent')


    sess_instance.start()

    with codecs.open(outFileFullPath, 'a', 'utf-8') as ofile:
        with codecs.open(logFileFullPath, 'a', 'utf-8') as log:
            _catalog_sess_loop(sess_instance, ofile, log)
