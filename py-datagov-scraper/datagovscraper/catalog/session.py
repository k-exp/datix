import BeautifulSoup as bs
import urllib2
import os
import re

class CatalogSession(object):
    """scraper session for catalog.data.gov"""
    def __init__(self,
                 current_page=1,
                 filter_url='/dataset',
                 page_range=None):
        """
        initialize scraper session
        """
        self.configure(current_page=current_page,
                       filter_url=filter_url,
                       page_range=page_range)

    def configure(self,
                  current_page=1,
                  filter_url='/dataset',
                  page_range=None):
        """
        this method feels like a hack. it only exists because i can't import
        this module from the shell module without getting relative path errors
        """
        self.filter_url = filter_url
        self.start_page = 1
        self.end_page = None
        self.current_page = current_page
        self._base_catalog_url = 'https://catalog.data.gov'
        self._has_page_range = False
        self._page_range_ubound = None
        self._page_range_lbound = None
        if isinstance(page_range, tuple) and len(page_range) == 2:
            self._has_page_range = True
            # TODO: check ints
            self._page_range_lbound = page_range[0]
            self._page_range_ubound = page_range[1]
            # set current page to lbound of range
            # note: this might lead to issues in the future. would be better
            # to first extract page info from the first page, check that both
            # ubound and lbound are within range, then proceed normally
            self.current_page = self._page_range_lbound
        self._current_page_raw_cache = None
        self._current_page_soup_cache = None
        self._current_page_scrape_results = None

    def start(self):
        """
        start scrape session for given filter url
        """
        self.load_current()
        self.extract_pagination_info()

    def build_url(self):
        """
        build url string for current page
        """
        query_string = self.filter_url
        # the provided filter might not contain query parameters
        if len(query_string.split('?')) <= 1:
            query_string += '?'
        # added page query parameter
        query_string = (query_string + 'page={0}').format(self.current_page)
        return self._base_catalog_url + query_string

    def load_current(self):
        """
        make http GET to current page
        """
        url = self.build_url()
        # load and cache current page
        self._current_page_raw_cache = urllib2.urlopen(url).read()
        self._current_page_soup_cache = bs.BeautifulSoup(\
            self._current_page_raw_cache)

    def extract_pagination_info(self):
        """
        get max page number from the currently loaded page
        """
        if self._current_page_soup_cache is None:
            raise Exception('page html not initialized')
        # get pagination markup. this should return a div containing
        # a single ul tag. each child li contains page links
        pagercontent = self._current_page_soup_cache.find('div', {
            'class':'pagination pagination-centered' })
        # extract hrefs
        links = map(lambda x: x['href'], pagercontent.findAll('a'))
        # sort hrefs ascending. last item of sorted list should be
        # href corresponding to max page
        links.sort()
        # split last href querystring and cast
        self.end_page = int(links[-1].split('=')[1])

    def extract_page_ds_descriptions(self):
        """
        get descriptions of datasets on current page
        """
        objects = []
        resclass = re.compile('^dataset-resources')
        dscontent = self._current_page_soup_cache.findAll('div', {
            'class':'dataset-content' })
        for c in dscontent:
            obj = {}
            # org name of dataset provider
            orgtype = c.find('span', { 'class':'organization-type' })
            orgtype = orgtype['data-organization-type']
            obj['organization'] = orgtype
            # dataset title
            heading = c.find('h3', { 'class':'dataset-heading' })
            heading = heading.find('a')
            heading_title = heading.contents[0]
            heading_link = heading['href']
            obj['heading'] = {
                'title': heading_title,
                'link': heading_link
            }
            # dataset description
            notes = c.find('div', { 'class':'notes' })
            notes_title = notes.find('p').contents[0].replace('&mdash;','')
            notes_body = notes.find('div').contents[0]
            obj['notes'] = {
                'title': notes_title,
                'body': notes_body
            }
            # available formats of dataset. this is empty occasionally
            resources = c.find('ul', { 'class':resclass })
            if resources is not None:
                resources = resources.findAll('a', { 'class':'label' })
                obj['resources'] = []
                for r in resources:
                    resource_format = r['data-format']
                    resource_org = r['data-organization']
                    resource_link = r['href']
                    obj['resources'].append({
                        'organization': resource_org,
                        'format': resource_format,
                        'link': resource_link
                    })
            else:
                obj['resources'] = []
            objects.append(obj)
        self._current_page_scrape_results = objects
        return objects

    def flush(self):
        """
        flush all cache objects
        """
        self._current_page_raw_cache = None
        self._current_page_soup_cache = None
        self._current_page_scrape_results = None

    def next(self):
        """
        fetch next page if available. next should only be called after the
        load_current method
        """
        if not self._has_page_range:
            if self.current_page >= self.end_page:
                return False

        if self._has_page_range:
            if self.current_page >= self._page_range_ubound:
                return False

        self.current_page += 1
        self.load_current()
        return True
