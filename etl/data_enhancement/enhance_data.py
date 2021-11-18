from data_enhancement.enhancement_duplicates import enhancement_exact_duplicates as e_exact_duplicates
from data_enhancement.enhancement_location.lat_lon_enhancer import add_lat_lon
from data_enhancement.enhancement_contexts.enhance_data_de import function_map as de_map
from data_enhancement.enhancement_contexts.enhance_data_us import function_map as us_map
from shared.logger_factory import LoggerFactory


class Enhancer:
    """ Class handling the enhancement steps for crawled data based on its origin """

    _context = "de"

    def __init__(self, data, domain_name, context):
        """Constructor of Enhancer."""
        self._data = data
        self._domain_name = domain_name
        self._context = context
        self.logger = LoggerFactory.get_enhancement_logger()

        if context == 'de':
            self._function_map = de_map()
        elif context == 'us':
            self._function_map = us_map()

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
            self._function_map[domain](self)
        else:
            self.logger.error(f'No function set for \'{domain}\'')
