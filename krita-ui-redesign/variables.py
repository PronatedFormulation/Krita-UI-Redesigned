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
from PyQt6.QtWidgets import QApplication
from PyQt6.QtGui import QPalette

# Cached palette-derived colors (hex without '#')
highlight = "000000"
background = "000000"
alternate = "000000"
inactive_text_color = "000000"
active_text_color = "000000"
button_color = "000000"
base_color = "000000"
mid_color = "000000"
light_color = "000000"
dark_color = "000000"
window_text = "000000"
bright_text = "000000"

small_tab_size = 20

# Style string holders (filled by buildFlatTheme / rebuildNuStyles)
no_borders_style = " QToolBar { border: none; } "
nu_toolbox_style = ""
nu_toggle_button_style = ""
nu_tool_options_style = ""
nu_scroll_area_style = ""

small_tab_style = f"QTabBar::tab {{ height: {small_tab_size}px; }}"
big_tab_style = "QTabBar::tab { }"

flat_tab_style = ""
flat_main_window_style = ""
flat_tool_button_style = ""
flat_push_button_style = ""
flat_dock_style = ""
flat_toolbar_style = ""
flat_menu_bar_style = ""
flat_combo_box_style = ""
flat_toolbox_style = ""
flat_status_bar_style = ""
flat_tree_view_style = ""
flat_overview_docker_style = ""
flat_welcome_page = ""
flat_button_style = ""


def _palette_color(role, group=QPalette.ColorGroup.Active):
    """Return the current theme color for a QPalette role as hex without '#'."""
    app = QApplication.instance()
    if app is None:
        return "000000"
    return app.palette().color(group, role).name().split("#")[1]


def refreshPaletteColors():
    """Re-read every color we care about from the active application palette."""
    global highlight, background, alternate, inactive_text_color, active_text_color
    global button_color, base_color, mid_color, light_color, dark_color
    global window_text, bright_text

    highlight = _palette_color(QPalette.ColorRole.Highlight)
    background = _palette_color(QPalette.ColorRole.Window)
    alternate = _palette_color(QPalette.ColorRole.AlternateBase)
    # ToolTipText is often a reasonable "secondary" text color in Krita themes
    inactive_text_color = _palette_color(QPalette.ColorRole.ToolTipText)
    active_text_color = _palette_color(QPalette.ColorRole.WindowText)
    button_color = _palette_color(QPalette.ColorRole.Button)
    base_color = _palette_color(QPalette.ColorRole.Base)
    mid_color = _palette_color(QPalette.ColorRole.Mid)
    light_color = _palette_color(QPalette.ColorRole.Light)
    dark_color = _palette_color(QPalette.ColorRole.Dark)
    window_text = _palette_color(QPalette.ColorRole.WindowText)
    bright_text = _palette_color(QPalette.ColorRole.BrightText)


def rebuildNuStyles():
    """Rebuild the NuTools stylesheets from the current palette."""
    global nu_toolbox_style, nu_toggle_button_style, nu_tool_options_style, nu_scroll_area_style

    nu_toolbox_style = f"""
            QWidget {{
                background-color: #01{alternate};
            }}

            .QScrollArea {{
                background-color: #00{background};
            }}

            QScrollArea * {{
                background-color: #00000000;
            }}

            QScrollArea QToolTip {{
                background-color: #{active_text_color};
            }}

            QAbstractButton {{
                background-color: #aa{background};
                border: none;
                border-radius: 4px;
            }}

            QAbstractButton:checked {{
                background-color: #cc{highlight};
            }}

            QAbstractButton:hover {{
                background-color: #{highlight};
            }}

            QAbstractButton:pressed {{
                background-color: #{alternate};
            }}
        """

    nu_toggle_button_style = f"""
        QToolButton {{
            background-color: #aa{background};
            border: none;
            border-radius: 4px;
        }}

        QToolButton:hover {{
            background-color: #{highlight};
        }}

        QToolButton:pressed {{
            background-color: #{alternate};
        }}
        """

    # Tool Options pad: use the styled container from ntwidgetpad and
    # palette() keywords where possible so controls track the theme
    # even between full rebuilds.
    nu_tool_options_style = f"""
        QWidget#toolOptionsPad {{
            background-color: transparent;
            color: #{active_text_color};
        }}

        QWidget#toolOptionsPadContainer {{
            background-color: #{background};
            border: none;
            border-radius: 8px;
        }}

        QWidget#toolOptionsPadContainer QWidget {{
            border: none;
        }}

        QWidget#toolOptionsPad QAbstractButton,
        QWidget#toolOptionsPad QComboBox,
        QWidget#toolOptionsPad QSpinBox,
        QWidget#toolOptionsPad QDoubleSpinBox {{
            background-color: #{base_color};
            color: #{active_text_color};
            border: none;
            border-radius: 4px;
        }}

        QWidget#toolOptionsPad QCheckBox::indicator {{
            width: 14px;
            height: 14px;
            border: 1px solid #{mid_color};
            border-radius: 2px;
            background-color: #{base_color};
        }}

        QWidget#toolOptionsPad QCheckBox::indicator:checked {{
            border-color: #{highlight};
            background-color: #{highlight};
        }}
    """

    nu_scroll_area_style = f"""
    QScrollArea {{
        background-color: #{background};
        color: #{active_text_color};
    }}
"""


def buildFlatTheme():
    """
    Rebuild every flat-theme stylesheet from the *current* application palette.
    Call this before applying styles so the redesign always follows the active theme.
    """
    global flat_tab_style
    global flat_main_window_style
    global flat_button_style
    global flat_dock_style
    global flat_toolbar_style
    global flat_menu_bar_style
    global flat_combo_box_style
    global flat_toolbox_style
    global flat_status_bar_style
    global flat_tree_view_style
    global flat_overview_docker_style
    global flat_welcome_page

    refreshPaletteColors()
    rebuildNuStyles()

    flat_menu_bar_style = """
        QMenuBar {
            border-bottom: 0px solid transparent;
        }
    """

    flat_overview_docker_style = f"""
        * {{
            background: #{background};
        }}

        * > QSpinBox {{
            border: none;
            background-color: #{alternate};
            border-radius: 4px;
        }}
    """

    flat_tab_style = f"""
        QTabBar::tab:!selected {{
            background: #{alternate};
            color: #{inactive_text_color};
        }}

        QMainWindow > QTabBar::tab {{
            margin-top: 5px;
            padding: 5px;
            background: #{background};
            qproperty-drawBase: 0;
            qproperty-expanding: 1;
            border-top-right-radius: 5px;
            border-top-left-radius: 5px;
        }}

        QMainWindow > QTabBar {{
            border: none;
            qproperty-drawBase: 0;
            qproperty-expanding: 1;
        }}

        QTabBar::tab:selected {{
            background: #{background};
        }}

        QTabBar::tab:hover {{
            color: #{active_text_color};
       }}
    """

    flat_main_window_style = f"""
        QStackedWidget, QStackedLayout {{
            background: #{background};
        }}
        QHeaderView {{
            background: transparent;
            background-color: #{background};
        }}

        QLineEdit {{
            background: #{alternate};
            selection-background-color: #{highlight};
            color: #{active_text_color};
        }}

        QStatusBar > * {{
            border: none;
        }}
    """

    flat_button_style = f"""
        QToolButton, QFrame {{
            background: #{background};
            border: none;
        }}

        QToolButton:checked {{
            background: #{alternate};
            border: none;
        }}

        QToolButton:hover {{
            background: #{alternate};
            border: none;
        }}

        QToolButton::menu-button {{
            background: #{background};
        }}

        QToolButton:hover {{
            background: #{alternate};
        }}

        QToolButton::menu-button:hover {{
            background: #{alternate};
        }}

        QToolButton[popupMode="1"] {{
            padding-right: 13px;
            border: none;
        }}

        QPushButton {{
            background: #{background};
            border: 1px solid #{alternate};
            padding: 5px;
            border-radius: 2px;
            color: #{active_text_color};
        }}

        QPushButton:hover {{
            background: #{alternate};
        }}

        QStatusBar QPushButton {{
            background: #{background};
            color: #{active_text_color};
        }}

        QStatusBar > QPushButton:hover {{
            background: #{alternate};
        }}

        QDoubleSpinBox {{
            border: 1px solid #{alternate};
            border-radius: 2px;
            background: #{background};
            color: #{active_text_color};
        }}

        QDoubleSpinBox::up-button,
        QDoubleSpinBox::up-arrow,
        QDoubleSpinBox::down-button,
        QDoubleSpinBox::down-arrow {{
            width: 10px;
            height: 10px;
            margin: 3px;
        }}

        QDoubleSpinBox::up-button,
        QDoubleSpinBox::up-arrow {{
            image: url(:24_light_draw-arrow-up.svg);
            margin-top: 1px;
         }}

        QDoubleSpinBox::down-button,
        QDoubleSpinBox::down-arrow {{
            image: url(:24_light_draw-arrow-down.svg);
            margin-bottom: 1px;
        }}
        """

    flat_dock_style = f"""
        QAbstractScrollArea {{
            background: #{background};
            border: none;
        }}

        QDockWidget {{
            titlebar-close-icon: url(:/light_deletelayer.svg);
            titlebar-normal-icon: url(:/light_duplicatelayer.svg);
            border-bottom-right-radius: 4px;
            border-bottom-left-radius: 4px;
        }}

        QDockWidget::close-button {{
            border: none;
            margin: -1px;
        }}

        QDockWidget::float-button {{
            border: none;
            margin: 1px;
        }}

        QDockWidget > * {{
            background-color: #{background};
            border: none;
            border-bottom-right-radius: 4px;
            border-bottom-left-radius: 4px;
            titlebar-close-icon: url(/:16_dark_tab-close.svg);
        }}

        QDockWidget::title {{
            background-color: #{background};
            border: none;
            padding: 5px;
            margin-top: 2px;
            color: #{active_text_color};
        }}"""

    flat_toolbar_style = f"""QToolBar {{
            background-color: #{background};
            border: none;
        }}
        """

    flat_combo_box_style = f"""QComboBox {{
            background: #{background};
            border-bottom: 2px solid #{inactive_text_color};
            border-radius: 4px;
            padding-left: 10px;
            padding-right: 10px;
            padding-bottom: 2px;
            padding-top: 2px;
            color: #{active_text_color};
        }}

        QComboBox:hover {{
            background: #{alternate};
        }}

        QComboBox::drop-down {{
            border: none;
            border-radius: 4px;
        }}

        QComboBox::down-arrow {{
            image: url(:16_light_draw-arrow-down.svg);
            width: 9px;
        }}"""

    flat_toolbox_style = "* > QToolButton {border: none;}"

    flat_status_bar_style = f"QStatusBar {{ background-color: #{background}; color: #{active_text_color}; }}"

    flat_tree_view_style = f"""QTreeView {{
        background-color: #{background};
        border: none;
        padding: 5px;
        color: #{active_text_color};
    }}"""

    flat_welcome_page = """
        QPushButton {
            border: none;
        }
    """
