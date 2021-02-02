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

"""
This class contains fixtures and common helper function to keep the test files shorter
"""
import json
from pathlib import Path

import pytest
from qgis.core import QgsVectorLayer, QgsProject

from ..model.map_config import MapConfig
from ..qgis_plugin_tools.testing.utilities import get_qgis_app
from ..qgis_plugin_tools.tools.resources import plugin_test_data_path

QGIS_APP, CANVAS, IFACE, PARENT = get_qgis_app()

# noinspection PyArgumentList
QGIS_INSTANCE = QgsProject.instance()


@pytest.fixture(scope='function')
def new_project() -> None:
    """Initializes new QGIS project by removing layers and relations etc."""
    yield IFACE.newProject()


@pytest.fixture(scope='session')
def test_gpkg():
    return plugin_test_data_path('test_data.gpkg')


@pytest.fixture
def harbour_points(test_gpkg):
    return get_layer('harbours', test_gpkg)


@pytest.fixture
def lines(test_gpkg):
    lines = get_layer('lines', test_gpkg)
    add_layer(lines)
    set_styles(lines, 'lines.qml')
    return lines


@pytest.fixture
def lines_3067(test_gpkg):
    return get_layer('lines_3067', test_gpkg)


@pytest.fixture
def polygons(test_gpkg):
    layer = get_layer('Polygons', test_gpkg)
    add_layer(layer)
    set_styles(layer, 'polygons.qml')
    return layer


@pytest.fixture
def polygons_3067(test_gpkg):
    return get_layer('polygons_3067', test_gpkg)


@pytest.fixture
def harbour_points_3067(test_gpkg):
    return get_layer('harbours_3067', test_gpkg)


@pytest.fixture
def simple_harbour_points(harbour_points):
    add_layer(harbour_points)
    set_styles(harbour_points, 'harbour_simple.qml')
    return harbour_points


@pytest.fixture
def simple_harbour_points_invalid_size_units(harbour_points):
    add_layer(harbour_points)
    set_styles(harbour_points, 'harbour_simple_invalid_size_unit.qml')
    return harbour_points


@pytest.fixture
def simple_harbour_points_3067(harbour_points_3067):
    add_layer(harbour_points_3067)
    set_styles(harbour_points_3067, 'harbour_simple.qml')
    return harbour_points_3067


@pytest.fixture
def lines_invalid_size_units(lines):
    set_styles(lines, 'lines_invalid_size_unit.qml')
    return lines


@pytest.fixture
def polygons_invalid_size_units(polygons):
    set_styles(polygons, 'polygons_invalid_size_unit.qml')
    return polygons


@pytest.fixture
def tmpdir_pth(tmpdir) -> Path:
    return Path(tmpdir)


def get_layer(name: str, gpkg):
    layer = QgsVectorLayer(f'{gpkg}|layername={name}', name, 'ogr')
    assert layer.isValid()
    return layer


def set_styles(layer_simple_poly, style_file):
    style_file = plugin_test_data_path('style', style_file)
    msg, succeeded = layer_simple_poly.loadNamedStyle(style_file)
    assert succeeded, msg


def add_layer(layer: QgsVectorLayer) -> None:
    initial_layers = QGIS_INSTANCE.mapLayers()
    QGIS_INSTANCE.addMapLayer(layer, False)
    assert len(QGIS_INSTANCE.mapLayers()) > len(initial_layers)


def get_map_config(config_name: str):
    """ Get map config from test data directory """
    with open(plugin_test_data_path('config', config_name)) as f:
        map_config_dict = json.load(f)
    return MapConfig.from_dict(map_config_dict)


def get_loaded_map_config(conf_path: Path):
    """ Get map config from path """
    assert conf_path.exists()
    with open(conf_path) as f:
        map_config_dict = json.load(f)
    return MapConfig.from_dict(map_config_dict)
