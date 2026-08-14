"""
    Plugin for Krita UI Redesign, Copyright (C) 2020 Kapyia, Pedro Reis

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""

from krita import *
from .nuTools.nttoolbox import ntToolBox
from .nuTools.nttooloptions import ntToolOptions
from . import variables
from PyQt6.QtWidgets import QMessageBox, QWidget, QFrame, QApplication
from PyQt6.QtCore import QEvent, QObject, QTimer

class _PaletteChangeFilter(QObject):
    """Watches the application for palette changes (theme switches).

    Must NOT call setStyleSheet / resize synchronously here: ApplicationPaletteChange
    fires while Qt is still applying the new palette. Doing heavy UI work in the
    filter re-enters style/polish code and can crash Krita.
    """

    def __init__(self, redesign):
        super().__init__()
        self.redesign = redesign

    def eventFilter(self, obj, event):
        if event.type() == QEvent.Type.ApplicationPaletteChange:
            # Defer until the event has fully propagated.
            self.redesign.scheduleThemeRefresh()
        return False


class Redesign(Extension):

    usesFlatTheme = False
    usesBorderlessToolbar = False
    usesThinDocumentTabs = False
    usesNuToolbox = False
    usesNuToolOptions = False
    ntTB = None
    ntTO = None
    _paletteFilter = None
    _themeRefreshPending = False
    _rebuilding = False

    def __init__(self, parent):
        super().__init__(parent)

    def scheduleThemeRefresh(self):
        """Coalesce palette-change storms into a single deferred rebuild."""
        if self._themeRefreshPending:
            return
        self._themeRefreshPending = True
        # 0 = next event-loop tick (after palette propagation). A short delay
        # gives Krita's own theme code time to finish widget updates first.
        QTimer.singleShot(50, self._applyThemeRefresh)

    def _applyThemeRefresh(self):
        self._themeRefreshPending = False
        if self._rebuilding:
            return
        win = Application.activeWindow()
        if not win:
            return
        qwin = win.qwindow()
        if qwin is None:
            return
        self.rebuildStyleSheet(qwin)

    def setup(self):
        if Application.readSetting("Redesign", "usesFlatTheme", "true") == "true":
            self.usesFlatTheme = True

        if Application.readSetting("Redesign", "usesBorderlessToolbar", "true") == "true":
            self.usesBorderlessToolbar = True

        if Application.readSetting("Redesign", "usesThinDocumentTabs", "true") == "true":
            self.usesThinDocumentTabs = True

        if Application.readSetting("Redesign", "usesNuToolbox", "true") == "true":
            self.usesNuToolbox = True

        if Application.readSetting("Redesign", "usesNuToolOptions", "true") == "true":
            self.usesNuToolOptions = True

    def createActions(self, window):
        actions = []

        actions.append(window.createAction("toolbarBorder", "Borderless Toolbars", ""))
        actions[0].setCheckable(True)
        actions[0].setChecked(self.usesBorderlessToolbar)

        actions.append(window.createAction("tabHeight", "Thin Document Tabs", ""))
        actions[1].setCheckable(True)
        actions[1].setChecked(self.usesThinDocumentTabs)

        actions.append(window.createAction("flatTheme", "Use flat theme", ""))
        actions[2].setCheckable(True)
        actions[2].setChecked(self.usesFlatTheme)

        actions.append(window.createAction("nuToolbox", "NuToolbox", ""))
        actions[3].setCheckable(True)
        actions[3].setChecked(self.usesNuToolbox)

        actions.append(window.createAction("nuToolOptions", "NuToolOptions", ""))
        actions[4].setCheckable(True)

        if Application.readSetting("", "ToolOptionsInDocker", "false") == "true":
            actions[4].setChecked(self.usesNuToolOptions)

        menu = window.qwindow().menuBar().addMenu("Redesign")

        for a in actions:
            menu.addAction(a)

        actions[0].toggled.connect(self.toolbarBorderToggled)
        actions[1].toggled.connect(self.tabHeightToggled)
        actions[2].toggled.connect(self.flatThemeToggled)
        actions[3].toggled.connect(self.nuToolboxToggled)
        actions[4].toggled.connect(self.nuToolOptionsToggled)

        # Follow theme changes at runtime
        if self._paletteFilter is None:
            self._paletteFilter = _PaletteChangeFilter(self)
            app = QApplication.instance()
            if app:
                app.installEventFilter(self._paletteFilter)

        variables.buildFlatTheme()

        if (self.usesNuToolOptions and
            Application.readSetting("", "ToolOptionsInDocker", "false") == "true"):
                self.ntTO = ntToolOptions(window)
                self.ntTO.pad.show()
                self.ntTO.updateStyleSheet()

        if self.usesNuToolbox:
            self.ntTB = ntToolBox(window)
            self.ntTB.pad.show()
            self.ntTB.updateStyleSheet()

        self.rebuildStyleSheet(window.qwindow())

    def toolbarBorderToggled(self, toggled):
        Application.writeSetting("Redesign", "usesBorderlessToolbar", str(toggled).lower())
        self.usesBorderlessToolbar = toggled
        self.rebuildStyleSheet(Application.activeWindow().qwindow())

    def flatThemeToggled(self, toggled):
        Application.writeSetting("Redesign", "usesFlatTheme", str(toggled).lower())
        self.usesFlatTheme = toggled
        self.rebuildStyleSheet(Application.activeWindow().qwindow())

    def tabHeightToggled(self, toggled):
        Application.instance().writeSetting("Redesign", "usesThinDocumentTabs", str(toggled).lower())
        self.usesThinDocumentTabs = toggled
        self.rebuildStyleSheet(Application.activeWindow().qwindow())

    def nuToolboxToggled(self, toggled):
        Application.writeSetting("Redesign", "usesNuToolbox", str(toggled).lower())
        self.usesNuToolbox = toggled

        if toggled:
            self.ntTB = ntToolBox(Application.activeWindow())
            self.ntTB.pad.show()
            self.ntTB.updateStyleSheet()
        elif not toggled and self.ntTB:
            self.ntTB.close()
            self.ntTB = None

    def nuToolOptionsToggled(self, toggled):
        if Application.readSetting("", "ToolOptionsInDocker", "false") == "true":
            Application.writeSetting("Redesign", "usesNuToolOptions", str(toggled).lower())
            self.usesNuToolOptions = toggled

            if toggled:
                self.ntTO = ntToolOptions(Application.activeWindow())
                self.ntTO.pad.show()
                self.ntTO.updateStyleSheet()
            elif not toggled and self.ntTO:
                self.ntTO.close()
                self.ntTO = None
        else:
            msg = QMessageBox()
            msg.setText("nuTools requires the Tool Options Location to be set to 'In Docker'. \n\n" +
                        "This setting can be found at Settings -> Configure Krita... -> General -> Tools -> Tool Options Location." +
                        "Once the setting has been changed, please restart Krita.")
            msg.exec()

    def rebuildStyleSheet(self, window):
        # Guard against re-entrancy: setStyleSheet can itself trigger style/palette
        # polish events while we are still rebuilding.
        if self._rebuilding:
            return
        if window is None:
            return

        self._rebuilding = True
        try:
            # Always re-read the active theme palette so styles follow
            # whatever color scheme the user has selected in Settings → Themes.
            variables.buildFlatTheme()

            full_style_sheet = ""

            # Dockers / chrome
            if self.usesFlatTheme:
                full_style_sheet += f"\n {variables.flat_dock_style} \n"
                full_style_sheet += f"\n {variables.flat_button_style} \n"
                full_style_sheet += f"\n {variables.flat_main_window_style} \n"
                full_style_sheet += f"\n {variables.flat_combo_box_style} \n"
                full_style_sheet += f"\n {variables.flat_status_bar_style} \n"
                full_style_sheet += f"\n {variables.flat_tab_style} \n"
                full_style_sheet += f"\n {variables.flat_tree_view_style} \n"
                full_style_sheet += f"\n {variables.flat_menu_bar_style} \n"
                full_style_sheet += f"\n {variables.flat_toolbar_style} \n"

                welcomePage = window.findChild(QWidget, 'KisWelcomePage')
                if welcomePage:
                    welcomePage.setStyleSheet(variables.flat_welcome_page)

            # Borderless toolbars: independent toggle, also implied by flat theme
            if self.usesFlatTheme or self.usesBorderlessToolbar:
                full_style_sheet += f"\n {variables.no_borders_style} \n"

            window.setStyleSheet(full_style_sheet)

            # Overview
            overview = window.findChild(QWidget, 'OverviewDocker')
            overview_style = ""

            # No border for Recent Documents and News Frame
            recentDocuments = window.findChild(QWidget, 'recentDocsStackedWidget')
            newsFrame = window.findChild(QWidget, 'newsFrame')
            remove_frame_elems = [recentDocuments, newsFrame]

            for elem in remove_frame_elems:
                if elem is None:
                    continue
                if hasattr(elem, 'setFrameStyle'):
                    elem.setFrameStyle(QFrame.Shape.NoFrame)
                if hasattr(elem, 'setFrameShape'):
                    elem.setFrameShape(QFrame.Shape.NoFrame)
                if hasattr(elem, 'setLineWidth'):
                    elem.setLineWidth(0)
                elem.setStyleSheet("")

            if self.usesFlatTheme:
                overview_style += f"\n {variables.flat_overview_docker_style} \n"

            if overview:
                overview.setStyleSheet(overview_style)

            # Document tabs
            canvas_style_sheet = ""

            if self.usesThinDocumentTabs:
                canvas_style_sheet += f"\n {variables.small_tab_style} \n"
            else:
                canvas_style_sheet += f"\n {variables.big_tab_style} \n"

            canvas = window.centralWidget()
            if canvas:
                canvas.setStyleSheet(canvas_style_sheet)
                # Force a layout pass so tab height changes take effect
                canvas.resize(canvas.sizeHint())

            # NuTools pads — styles were refreshed above by buildFlatTheme()
            if self.usesNuToolOptions and self.ntTO:
                self.ntTO.updateStyleSheet()

            if self.usesNuToolbox and self.ntTB:
                self.ntTB.updateStyleSheet()
        finally:
            self._rebuilding = False

Krita.instance().addExtension(Redesign(Krita.instance()))
