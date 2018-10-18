from qgis.PyQt.QtGui import QIcon
from qgis.PyQt.QtWidgets import QAction
from qgis.PyQt.QtCore import QObject
from qgis.core import QgsMessageLog, Qgis
from qgis.utils import qgsfunction, plugins

from comptages.core.settings import ComptagesSettings
from comptages.core.layers import Layers
from comptages.core.filter_dialog import FilterDialog
from comptages.ui.resources import *


class Comptages(QObject):

    def __init__(self, iface):
        QgsMessageLog.logMessage('__init__', 'Comptages', Qgis.Info)
        QObject.__init__(self)

        self.iface = iface
        self.settings = ComptagesSettings()
        self.layers = Layers(self.iface)

    def initGui(self):
        QgsMessageLog.logMessage('initGui', 'Comptages', Qgis.Info)

        self.connect_db_action = QAction(
            QIcon(':/plugins/Comptages/images/power.png'),
            'Connect DB',
            self.iface.mainWindow()
        )

        self.create_new_action = QAction(
            QIcon(':/plugins/Comptages/images/measure.png'),
            'Create new measure',
            None
        )

        self.select_edit_action = QAction(
            QIcon(':/plugins/Comptages/images/select_edit.png'),
            'Edit measure',
            None
        )

        self.filter_action = QAction(
            QIcon(':/plugins/Comptages/images/filter.png'),
            'Filter',
            None
        )

        self.settings_action = QAction(
            QIcon(':/plugins/Comptages/images/settings.png'),
            'Settings',
            None
        )

        self.connect_db_action.triggered.connect(
            self.do_connect_db_action)

        self.create_new_action.triggered.connect(
            self.do_create_new_action)

        self.select_edit_action.triggered.connect(
            self.do_select_edit_action)

        self.filter_action.triggered.connect(
            self.do_filter_action)

        self.settings_action.triggered.connect(
            self.do_settings_action)

        self.iface.addPluginToMenu('Comptages', self.connect_db_action)
        self.iface.addPluginToMenu('Comptages', self.create_new_action)
        self.iface.addPluginToMenu('Comptages', self.select_edit_action)
        self.iface.addPluginToMenu('Comptages', self.filter_action)
        self.iface.addPluginToMenu('Comptages', self.settings_action)

        self.toolbar = self.iface.addToolBar('Comptages')
        self.toolbar.setObjectName('Comptages')
        self.toolbar.setToolTip('Comptages toolbar')

        self.toolbar.addAction(self.connect_db_action)
        self.toolbar.addAction(self.create_new_action)
        self.toolbar.addAction(self.select_edit_action)
        self.toolbar.addAction(self.filter_action)
        self.toolbar.addAction(self.settings_action)

    def unload(self):
        self.iface.removePluginMenu('Comptages', self.connect_db_action)
        self.iface.removePluginMenu('Comptages', self.create_new_action)
        self.iface.removePluginMenu('Comptages', self.select_edit_action)
        self.iface.removePluginMenu('Comptages', self.filter_action)
        self.iface.removePluginMenu('Comptages', self.settings_action)

        del self.connect_db_action
        del self.create_new_action
        del self.select_edit_action
        del self.filter_action
        del self.settings_action

        del self.toolbar

    def do_connect_db_action(self):
        QgsMessageLog.logMessage(
            'do_connect_db_action', 'Comptages', Qgis.Info)
        self.layers.load_layers()

    def do_create_new_action(self):
        QgsMessageLog.logMessage(
            'do_create_new_action', 'Comptages', Qgis.Info)

    def do_select_edit_action(self):
        QgsMessageLog.logMessage(
            'do_select_edit_action', 'Comptages', Qgis.Info)
        self.layers.edit_count()

    def do_filter_action(self):
        QgsMessageLog.logMessage(
            'do_filter_action', 'Comptages', Qgis.Info)
        dlg = FilterDialog(self.iface)
        if dlg.exec_():
            self.layers.apply_filter(
                dlg.start_date.dateTime().toString('yyyy-MM-dd'),
                dlg.end_date.dateTime().toString('yyyy-MM-dd'),
                dlg.installation.currentIndex(),
                dlg.sensor.currentIndex())

    def do_settings_action(self):
        QgsMessageLog.logMessage(
            'do_settings_action', 'Comptages', Qgis.Info)

    def do_export_configuration_action(self, count_id):
        QgsMessageLog.logMessage(
            f'do_export_configuration_action {count_id}',
            'Comptages', Qgis.Info)

    def do_import_data_action(self, count_id):
        QgsMessageLog.logMessage(
            f'do_import_data_action {count_id}',
            'Comptages', Qgis.Info)

    def do_generate_report_action(self, count_id):
        QgsMessageLog.logMessage(
            f'do_generate_report_action {count_id}',
            'Comptages', Qgis.Info)

    def do_export_plan_action(self, count_id):
        QgsMessageLog.logMessage(
            f'do_export_plan_action {count_id}',
            'Comptages', Qgis.Info)

    def do_generate_chart_action(self, count_id):
        QgsMessageLog.logMessage(
            f'do_generate_chart_action {count_id}',
            'Comptages', Qgis.Info)

    def enable_actions_if_needed(self):
        """Enable actions if the plugin is connected to the db
        otherwise disable them"""
        pass

    def is_connected(self):
        """Return if the plugin is connected to the database"""
        pass

    def is_section_highlighted(self, section_id):
        return self.layers.is_section_highlighted(section_id)

    @qgsfunction(args="auto", group="Comptages")
    def is_highlighted(feature, parent):
        """Used by section layer to apply a style to the sections related to a
        count"""

        # Call the class method of the current instance of the plugin
        return plugins['comptages'].is_section_highlighted(
            feature.attribute('id'))
