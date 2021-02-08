#  Gispo Ltd., hereby disclaims all copyright interest in the program Unfolded Studio QGIS plugin
#  Copyright (C) 2021 Gispo Ltd (https://www.gispo.fi/).
#
#
#  This file is part of Unfolded Studio QGIS plugin.
#
#  Unfolded Studio QGIS plugin is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 2 of the License, or
#  (at your option) any later version.
#
#  Unfolded Studio QGIS plugin is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with Unfolded Studio QGIS plugin.  If not, see <https://www.gnu.org/licenses/old-licenses/gpl-2.0.en.html>.
import enum
import json
from typing import Union, List

from ..qgis_plugin_tools.tools.exceptions import QgsPluginException
from ..qgis_plugin_tools.tools.i18n import tr
from ..qgis_plugin_tools.tools.resources import resources_path
from ..qgis_plugin_tools.tools.settings import get_setting, set_setting


@enum.unique
class Settings(enum.Enum):
    crs = 'EPSG:4326'
    project_crs = 'EPSG:3857'
    conf_output_dir = resources_path('configurations')
    layer_blending = 'normal'

    # size
    pixel_size_unit = 'Pixel'
    millimeter_size_unit = 'MM'
    millimeters_to_pixels = 0.28  # Taken from qgssymbollayerutils.cpp
    width_pixel_factor = 3.0  # Empirically determined factor

    # basemaps
    basemap = 'dark'
    mapbox_api_token = ''
    basemap_wmts_url = 'url=https://api.mapbox.com/styles/v1/{username}/{style_id}/wmts?access_token%3D{token}&contextualWMSLegend=0&crs={crs}&format=image/png&layers={style_id}&styles=default&tileMatrixSet=GoogleMapsCompatible'
    wmts_basemaps = {
        'uberdata': {
            'dark': 'cjoqbbf6l9k302sl96tyvka09',
            'light': 'cjoqb9j339k1f2sl9t5ic5bn4',
            'muted': 'cjfyl03kp1tul2smf5v2tbdd4',
            'muted_night': 'cjfxhlikmaj1b2soyzevnywgs',
        },
        'mapbox': {
            'satellite': 'satellite-v9'
        },
        'unfoldedinc': {
            'satellite-streets': 'ckcr4dmep0i511is9m4qj9az5',
            'streets': 'ckfzpk24r0thc1anudzpwnc9q',
        }
    }

    _options = {'layer_blending': ['normal', 'additive', 'substractive'],
                'basemap': ['dark', 'light', 'muted', 'muted_night', 'satellite', 'satellite-street', 'streets']}

    def get(self, typehint: type = str) -> any:
        """Gets the value of the setting"""
        if self in (Settings.millimeters_to_pixels, Settings.width_pixel_factor):
            typehint = float
        elif self in (Settings.wmts_basemaps,):
            return json.loads(get_setting(self.name, json.dumps(self.value), str))
        return get_setting(self.name, self.value, typehint)

    def set(self, value: Union[str, int, float, bool]) -> bool:
        """Sets the value of the setting"""
        options = self.get_options()
        if options and value not in options:
            raise QgsPluginException(tr('Invalid option. Choose something from values {}', options))
        if self in (Settings.wmts_basemaps,):
            value = json.dumps(value)
        return set_setting(self.name, value)

    def get_options(self) -> List[any]:
        """Get options for the setting"""
        return Settings._options.value.get(self.name, [])
