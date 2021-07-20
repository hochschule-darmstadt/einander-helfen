from data_enhancement.enhancement_duplicates import enhancement_exact_duplicates as e_exact_duplicates
from data_enhancement.enhancement_tags import enhancement_tags as e_tags
from data_enhancement.enhancement_location.lat_lon_enhancer import add_lat_lon
from data_enhancement.enhancement_translation.enhancement_translation import translate_english_countries
from shared.logger_factory import LoggerFactory


class Enhancer:
    """ Class handling the enhancement steps for crawled data based on its origin """

    def __init__(self, data, domain_name):
        """Constructor of Enhancer."""
        self._data = data
        self._domain_name = domain_name
        self.logger = LoggerFactory.get_enhancement_logger()

        # link function containing domain specific enhancement to said domain here
        # 'domain' : self._enhance_domain_function_name
        # make sure to enter 'self._enhance_domain_function_name' and not
        # 'self._enhance_domain_function_name()' as brackets would make this
        # a function call instead of a reference to the function
        self._function_map = {
            'ehrenamt_hessen': self._enhance_ehrenamt_hessen,
            'weltwaerts': self._enhance_weltwaerts,
            'gutetat_berlin': self._enhance_gute_tat,
            'gutetat_hamburg': self._enhance_gute_tat,
            'gutetat_munich': self._enhance_gute_tat,
            'ein_jahr_freiwillig': self._enhance_ein_jahr_freiwillig,
            'bundesfreiwilligendienst': self._enhance_bundesfreiwilligendienst,
            'european_youth_portal': self._enhance_european_youth_portal,
            'betterplace': self._enhance_betterplace,
            'ehrenamt_sachsen': self._enhance_ehrenamt_sachsen,
            'dksb_kinderschutzbund': self._enhance_dksb_kinderschutzbund,
            'sozialeinsatz': self._enhance_sozialeinsatz
        }

    def run(self):
        """ run general enhancements and load domainspecific enhancement. """
        self.logger.info(f'Run general enhancement for {self._domain_name}')

        e_exact_duplicates.remove_duplicates(self._data, self._domain_name)
        add_lat_lon(self._data, self._domain_name)
        self._run_for_domain(self._domain_name)
        return self._data

    def _run_for_domain(self, domain):
        """ run domainspecific enhancement. """
        self.logger.info(f'Run domain specific enhancement enhancement for {domain}')

        if domain in self._function_map:
            self._function_map[domain]()
        else:
            self.logger.error(f'No function set for \'{domain}\'')

    def _enhance_ehrenamt_hessen(self):
        """ domain specific enhancement for ehrenamtsuche hessen """
        self.logger.debug('_enhance_ehrenamt_hessen()')

        e_tags.run(self._data, self._domain_name)

    def _enhance_weltwaerts(self):
        """ domain specific enhancement for weltwaerst """
        self.logger.debug('_enhance_weltwaerts()')

        self.logger.info('no specific enhancement for weltwaerts required')

    def _enhance_gute_tat(self):
        """ domain specific enhancement for gute-tat website group"""
        self.logger.debug('_enhance_gute_tat()')

        self.logger.info('no specific enhancement for gute-tat required')

    def _enhance_ein_jahr_freiwillig(self):
        """ domain specific enhancement for ein-jahr-freiwillig """
        self.logger.debug('_enhance_ein_jahr_freiwillig()')

        e_tags.run(self._data, self._domain_name)

    def _enhance_bundesfreiwilligendienst(self):
        """ domain specific enhancement for bundesfreiwilligendienst """
        self.logger.debug('_enhance_bundesfreiwilligendienst()')

        e_tags.run(self._data, self._domain_name)

    def _enhance_european_youth_portal(self):
        """ domain specific enhancement for european_youth_portal """
        self.logger.debug('_enhance_european_youth_portal()')

        e_tags.run(self._data, self._domain_name)

        translate_english_countries(self._data)

    def _enhance_betterplace(self):
        """ domain specific enhancement for betterplace """
        self.logger.debug('_enhance_betterplace()')

        e_tags.run(self._data, self._domain_name)

    def _enhance_ehrenamt_sachsen(self):
        """ domain specific enhancement for ehrenamt_sachsen """
        self.logger.debug('_enhance_ehrenamt_sachsen()')

        e_tags.run(self._data, self._domain_name)

    def _enhance_dksb_kinderschutzbund(self):
        """ domain specific enhancement for dksb_kinderschutzbund """
        self.logger.debug('_enhance_dksb_kinderschutzbund()')

        e_tags.run(self._data, self._domain_name)

    def _enhance_sozialeinsatz(self):
        """ domain specific enhancement for sozialeinsatz """
        self.logger.debug('_enhance_sozialeinsatz()')

        e_tags.run(self._data, self._domain_name)
