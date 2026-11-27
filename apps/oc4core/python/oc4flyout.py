## The plot's menu (the engine's "flyout"): Shift and a left click on the map, as the original's.
## The game core lists its items (CvGame::startFlyoutMenu: the city's production, Move To, Select
## All, Fortify All, the units there) and does the one chosen (CvGame::applyFlyoutMenu, through
## oc4host.flyout_choose); this draws them over the main interface.
##
## Seen in Wine (backlog #113, testgames/shots/wine-stacksel/ss-m10.png, 1600x900): the list's
## top left corner at the mouse, 222 x 288, rows 28 apart starting 13 down, the text 35 in, ten
## rows shown and a scroll bar for more, on the dark blue panel of the main interface.

import CvPythonExtensions as _cpe
import oc4host

_W, _H, _ROWS = 222, 288, 10
_NAMES = ('OC4FlyoutPanel', 'OC4FlyoutList')
_shown = [False]


def _screen():
	import CvScreenEnums
	return _cpe.CyGInterfaceScreen('MainInterface', CvScreenEnums.MAIN_INTERFACE)


def show(items, x, y):
	"""items: the rows' texts in the game core's order; x, y: the mouse."""
	hide()
	if not items:
		return
	screen = _screen()
	xr, yr = screen.getXResolution(), screen.getYResolution()
	h = min(_H, 16 + 28 * len(items))
	# (OpenCiv4's: kept on the screen, left of or above the mouse at the right or bottom edge;
	# the original's at an edge is not seen yet)
	if x + _W > xr:
		x = max(0, x - _W)
	if y + h > yr:
		y = max(0, y - h)
	screen.addPanel(_NAMES[0], u'', u'', True, False, x, y, _W, h, _cpe.PanelStyles.PANEL_STYLE_MAIN)
	screen.addListBoxGFC(_NAMES[1], u'', x + 22, y + 8, _W - 30, h - 16, _cpe.TableStyles.TABLE_STYLE_EMPTY)  # (no stripes, as Wine's)
	box = screen._s.get(_NAMES[1])
	if box is not None:
		box.rowHeight = 28
	for k, text in enumerate(items):
		screen.appendListBoxString(_NAMES[1], text, _cpe.WidgetTypes.WIDGET_GENERAL, k, -1)
	_shown[0] = True


def hide():
	"""True if the menu was up."""
	if not _shown[0]:
		return False
	screen = _screen()
	for name in _NAMES:
		screen.deleteWidget(name)
	_shown[0] = False
	return True


def isShown():
	return _shown[0]


def handleInput(argsList):
	"""A row of the list chosen (oc4screens' input tuple: notify at 0, the row at 1)."""
	notify, data = argsList[0], argsList[1]
	if notify == 11:  # NOTIFY_LISTBOX_ITEM_SELECTED
		hide()
		oc4host.flyout_choose(int(data))
	return 1
