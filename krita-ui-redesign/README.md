# Krita UI Redesign — Pulvergate Fork (Krita 6.x / PyQt6)

A community UI redesign plugin for Krita, originally by **Kapyia** and **Pedro Reis**.  
This **Pulvergate** fork is a Krita 6.x / Qt 6 / PyQt6 port with live theme following and robustness fixes merged from the Kaledosium fork.

---

## Installation

1. Copy the `krita-ui-redesign` folder **and** the `krita-ui-redesign.desktop` file into Krita’s `pykrita` directory:
   - **Linux:** `~/.local/share/krita/pykrita/`
   - **Windows:** `C:\Users\USERNAME\AppData\Roaming\krita\pykrita`
2. The `.desktop` file must sit **next to** the folder (not inside it).
3. In Krita: **Settings → Configure Krita → Python Plugin Manager** → enable **Krita UI Redesign**.
4. Restart Krita.

You can also open the resource folder from **Settings → Manage Resources → Open Resource Folder… → pykrita**.

Features appear under the **Redesign** menu in the menu bar.

---

## Features (user-facing)

| Feature | Description |
|--------|-------------|
| **Flat Theme** | Flat chrome for dockers, toolbars, menus, tabs, buttons, status bar, tree views, overview docker, and welcome page. Colors always come from the **active Krita color scheme**. |
| **Thin Document Tabs** | Slimmer document tab bar height. |
| **Borderless Toolbars** | Independent toggle to remove toolbar borders/white lines. Also applied automatically when Flat Theme is on. |
| **NuToolbox** | Floating, collapsible toolbox pad on the left of the canvas (borrowed from Krita’s Toolbox docker). |
| **NuToolOptions** | Floating, collapsible tool options pad on the right (requires Tool Options Location = *In Docker*). |
| **Live theme refresh** | Switching themes in **Settings → Themes** rebuilds and reapplies all styles without restarting Krita. |

Menu items (all checkable, settings persisted under the `Redesign` config group):

- Borderless Toolbars  
- Thin Document Tabs  
- Use flat theme  
- NuToolbox  
- NuToolOptions  

---

## Changes in this fork

### 1. Krita 6.x / PyQt6 port

- All `PyQt5` imports → `PyQt6`
- `qApp.palette()` → `QApplication.instance().palette()` (with safe helpers)
- Qt 6 enum style throughout, for example:
  - `QEvent.Move` → `QEvent.Type.Move`
  - `QFrame.NoFrame` → `QFrame.Shape.NoFrame`
  - `Qt.WA_DeleteOnClose` → `Qt.WidgetAttribute.WA_DeleteOnClose`
  - `Qt.WindowStaysOnTopHint` → `Qt.WindowType.WindowStaysOnTopHint`
  - `QSizePolicy.Expanding` → `QSizePolicy.Policy.Expanding`
  - `QPalette.Highlight` → `QPalette.ColorRole.Highlight`
- `msg.exec_()` → `msg.exec()`
- Null-checks for widgets that may not exist (welcome page, overview docker, recent docs, news frame, etc.)

### 2. Live theme following (Pulvergate core work)

Previous versions often captured palette colors once at import and never refreshed them.

This fork:

- **`refreshPaletteColors()`** — re-reads Highlight, Window, AlternateBase, text, button, base, mid, light, dark, etc. from the current `QPalette`
- **`rebuildNuStyles()`** — rebuilds NuTools stylesheets from those colors
- **`buildFlatTheme()`** — always calls the above before applying flat chrome
- **`rebuildStyleSheet()`** — calls `buildFlatTheme()` every time styles are applied
- **`_PaletteChangeFilter`** — application event filter for `QEvent.Type.ApplicationPaletteChange`; when the user changes themes in Settings → Themes, styles rebuild and reapply automatically

Flat theme styles also cover:

- Welcome page  
- Overview docker  
- Recent Documents / News frame removal (no border frames)  
- Combo boxes, status bar text, tree views  
- Spin box arrow icons where applicable  

### 3. Merged from the Kaledosium fork

#### NuTools docker hardening

When NuToolbox / NuToolOptions “borrow” the real docker widgets, the original dockers can sometimes reappear as empty shells.

Hardening in `nttoolbox.py` and `nttooloptions.py`:

- Track `sourceDocker`
- Connect to `visibilityChanged`
- `_isSourceDockerEffectivelyEmpty()` — true when the docker’s widget was moved out
- `_ensureDockerHidden()` — force-hide the empty shell and uncheck its toggle action via `QSignalBlocker`
- Disconnect the signal cleanly on `close()`

#### Tool Options pad container

In `ntwidgetpad.py`, when the pad is `toolOptionsPad`:

- Borrowed widget is placed inside a `toolOptionsPadContainer` wrapper
- Container uses `WA_StyledBackground` and is targeted by stylesheet for rounded flat chrome
- Container is cleaned up in `returnDocker()`

`variables.nu_tool_options_style` styles the pad, container, buttons, combos, spin boxes, and checkboxes from the active palette on every rebuild.

#### Borderless Toolbars restored

- Independent **Borderless Toolbars** menu action again
- Setting: `Redesign/usesBorderlessToolbar`
- Still applied automatically when Flat Theme is enabled (`usesFlatTheme or usesBorderlessToolbar`)

#### Pad polish

- `WA_StyledBackground` on pads  
- Tighter layout margins (2px)  
- Ruler-aware left offset when canvas rulers are shown  
- Safer hide-button connection: `clicked` emits a bool; the handler ignores it so presses always toggle  
- More robust `toggleWidgetVisible` for both widget and optional container  

### 4. Packaging / docs

- `PORT_NOTES.md` — technical port and merge notes  
- `krita_ui_redesign_manual.html` — optional in-app manual reference (linked from the `.desktop` file)  
- This README — user features + full change outline  

---

## Requirements

- **Krita 6.x** (Qt 6 / PyQt6)
- For NuToolOptions: **Settings → Configure Krita → General → Tools → Tool Options Location** set to **In Docker**, then restart Krita once after changing that setting

---

## File layout

```
krita-ui-redesign.desktop          # Plugin descriptor (place next to folder)
krita-ui-redesign/
  __init__.py
  redesign.py                      # Extension entry, menu, stylesheet orchestration
  variables.py                     # Palette refresh + flat / NuTools stylesheets
  nutools.action
  krita_ui_redesign_manual.html
  PORT_NOTES.md
  README.md
  nuTools/
    nttoolbox.py                   # Floating toolbox pad + docker hardening
    nttooloptions.py               # Floating tool options pad + docker hardening
    ntwidgetpad.py                 # Shared pad, borrow/return, container
    ntadjusttosubwindowfilter.py
    ntscrollareacontainer.py
    nttogglevisiblebutton.py
```

---

## Credits

- Original plugin: **Kapyia**, **Pedro Reis**
- Toolbar white-line removal: **Kapyia**
- Krita 6 / PyQt6 port, live theme following, and packaging: **Pulvergate** fork
- Docker hardening, tool-options container, borderless toggle restore, pad polish: merged from the **Kaledosium** fork

Licensed under the **GNU General Public License v3** (or later), same as the original plugin.
