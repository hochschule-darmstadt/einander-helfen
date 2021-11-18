from data_enhancement.enhancement_tags import enhancement_tags as e_tags
from data_enhancement.enhancement_translation.enhancement_translation import translate_english_countries

"""
link function containing domain specific enhancement to said domain here
'domain' : self._enhance_domain_function_name
make sure to enter 'self._enhance_domain_function_name' and not
'self._enhance_domain_function_name()' as brackets would make this
a function call instead of a reference to the function
"""
def function_map():
    return {
        'ehrenamt_hessen': _enhance_ehrenamt_hessen,
        'weltwaerts': _enhance_weltwaerts,
        'gutetat_berlin': _enhance_gute_tat,
        'gutetat_hamburg': _enhance_gute_tat,
        'gutetat_munich': _enhance_gute_tat,
        'ein_jahr_freiwillig': _enhance_ein_jahr_freiwillig,
        'bundesfreiwilligendienst': _enhance_bundesfreiwilligendienst,
        'european_youth_portal': _enhance_european_youth_portal,
        'betterplace': _enhance_betterplace,
        'ehrenamt_sachsen': _enhance_ehrenamt_sachsen,
        'dksb_kinderschutzbund': _enhance_dksb_kinderschutzbund,
        'sozialeinsatz': _enhance_sozialeinsatz
    }


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
