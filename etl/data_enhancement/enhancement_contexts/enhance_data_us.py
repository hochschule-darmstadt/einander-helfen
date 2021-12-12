from data_enhancement.enhancement_tags import enhancement_tags as e_tags


"""
link function containing domain specific enhancement to said domain here
'domain' : self._enhance_domain_function_name
make sure to enter 'self._enhance_domain_function_name' and not
'self._enhance_domain_function_name()' as brackets would make this
a function call instead of a reference to the function
"""
def function_map():
    return {
        'volunteermatch': _enhance_volunteermatch,
    }


def _enhance_volunteermatch(self):
    """ domain specific enhancement for volunteermatch """
    self.logger.debug('_enhance_volunteermatch()')

    e_tags.run(self._data, self._domain_name, self._context)
