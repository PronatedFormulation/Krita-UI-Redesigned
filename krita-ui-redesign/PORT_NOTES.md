# Krita 6.1.0 / PyQt6 Port

Changes made for Krita 6.x (Qt 6 / PyQt6):

- All `PyQt5` imports → `PyQt6`
- `qApp.palette()` → `QApplication.instance().palette()` (with safe helper)
- Enums updated to Qt 6 style:
  - `QEvent.Move` → `QEvent.Type.Move` (etc.)
  - `QFrame.NoFrame` → `QFrame.Shape.NoFrame`
  - `Qt.WA_DeleteOnClose` → `Qt.WidgetAttribute.WA_DeleteOnClose`
  - `Qt.WindowStaysOnTopHint` → `Qt.WindowType.WindowStaysOnTopHint`
  - `QSizePolicy.Expanding` → `QSizePolicy.Policy.Expanding`
  - `QPalette.Highlight` → `QPalette.ColorRole.Highlight`
- `msg.exec_()` → `msg.exec()`
- Added null-checks for widgets that may not exist (welcome page, overview docker, etc.)

Merged improvements from the Kaledosium fork:

- NuTools docker hardening: track `sourceDocker`, listen to `visibilityChanged`,
  force-hide empty docker shells with `QSignalBlocker` so Toolbox / Tool Options
  cannot reappear while borrowed.
- Tool Options pad uses a styled `toolOptionsPadContainer` wrapper for rounded
  flat chrome; richer `nu_tool_options_style` rebuilt from the active palette.
- Independent **Borderless Toolbars** menu toggle restored (still auto-on with flat theme).
- Pad polish: `WA_StyledBackground`, tighter margins, ruler-aware left offset,
  safer hide-button toggle (ignores QToolButton's checked bool).

Installation (same as before):
1. Copy `krita-ui-redesign` folder + `krita-ui-redesign.desktop` into Krita's `pykrita` folder.
2. Enable the plugin in Settings → Configure Krita → Python Plugin Manager.
3. Restart Krita.
