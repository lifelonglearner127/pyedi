from .edixmlparser import EDIXMLParser


class EDIMap(EDIXMLParser):

    def __init__(self):
        self.maps = []
        
        super().__init__('maps.xml')

        for version_element in self.spec.documentElement.childNodes:
            icvn = version_element.getAttribute('icvn')

            for map_element in version_element.childNodes:
                fic = map_element.getAttribute('fic')
                vriic = map_element.getAttribute('vriic')

                self.maps.append({
                    'icvn': icvn,
                    'fic': fic,
                    'vriic': vriic,
                    'map_file': map_element.firstChild.nodeValue
                })

    def get_file_name(self, icvn, fic, vriic):
        for a in self.maps:
            if a['icvn'] == icvn and a['fic'] == fic and a['vriic'] == vriic:
                return a['map_file']
