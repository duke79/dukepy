#!/usr/bin/env python
# Module     : SysTrayIcon.py
# Synopsis   : Windows System tray icon.
# Programmer : Simon Brunning - simon@brunningonline.net
# Date       : 11 April 2005
# Notes      : Based on (i.e. ripped off from) Mark Hammond's
#              win32gui_taskbar.py and win32gui_menu.py demos from PyWin32

# https://stackoverflow.com/questions/9494739/how-to-build-a-systemtray-app-for-windows

import os
import win32api  # https://github.com/michaelgundlach/pyspeech/issues/23#issuecomment-280915608
import win32ui

import win32con
import win32gui_struct
from enum import Enum
from past.types import basestring

try:
	import winxpgui as win32gui
except ImportError:
	import win32gui


class Style:
	"""
	ref: https://docs.microsoft.com/en-us/windows/desktop/api/winuser/ns-winuser-tagmenuiteminfoa
	"""
	DEFAULT = win32con.MFS_DEFAULT  # only one item allower per menu
	CHECKED = win32con.MFS_CHECKED
	UNCHECKED = win32con.MFS_UNCHECKED
	ENABLED = win32con.MFS_ENABLED
	DISABLED = win32con.MFS_DISABLED
	GRAYED = win32con.MFS_GRAYED
	HILITE = win32con.MFS_HILITE
	UNHILITE = win32con.MFS_UNHILITE


class Type():
	"""
		ref: https://docs.microsoft.com/en-us/windows/desktop/api/winuser/ns-winuser-tagmenuiteminfoa
	"""
	BITMAP = win32con.MFT_BITMAP
	MENUBARBREAK = win32con.MFT_MENUBARBREAK
	MENUBREAK = win32con.MFT_MENUBREAK
	OWNERDRAW = win32con.MFT_OWNERDRAW
	RADIOCHECK = win32con.MFT_RADIOCHECK
	RIGHTJUSTIFY = win32con.MFT_RIGHTJUSTIFY
	RIGHTORDER = win32con.MFT_RIGHTORDER
	SEPARATOR = win32con.MFT_SEPARATOR
	STRING = win32con.MFT_STRING


class TrayItem():
	def __init__(self):
		self.text = 'tray_item'
		self.icon = None
		self.action = None
		self.style = None
		self._next_action_id = None
		self.type = None


class TraySeparator(TrayItem):
	def __init__(self):
		TrayItem.__init__(self)
		self.type = Type.SEPARATOR


class TraySubmenu(TrayItem):
	def __init__(self):
		TrayItem.__init__(self)
		self.items = []


class Tray(object):
	QUIT = 'QUIT'
	SPECIAL_ACTIONS = [QUIT]

	FIRST_ID = 1023

	def __init__(self,
				 icon,
				 hover_text,
				 menu_options,
				 on_quit=None,
				 default_menu_index=None,
				 window_class_name=None, ):

		self.icon = icon
		self.hover_text = hover_text
		self.on_quit = on_quit

		item_quit = TrayItem()
		item_quit.text = 'Quit'
		item_quit.action = self.QUIT

		menu_options.append(item_quit)

		self._next_action_id = self.FIRST_ID
		self.menu_actions_by_id = set()
		self.menu_options = self._add_ids_to_menu_options(list(menu_options))
		self.menu_actions_by_id = dict(self.menu_actions_by_id)
		del self._next_action_id

		self.default_menu_index = (default_menu_index or 0)
		self.window_class_name = window_class_name or "SysTrayIconPy"

		message_map = {win32gui.RegisterWindowMessage("TaskbarCreated"): self.restart,
					   win32con.WM_DESTROY: self.destroy,
					   win32con.WM_COMMAND: self.command,
					   win32con.WM_USER + 20: self.notify, }
		# Register the Window class.
		window_class = win32gui.WNDCLASS()
		hinst = window_class.hInstance = win32gui.GetModuleHandle(None)
		window_class.lpszClassName = self.window_class_name
		window_class.style = win32con.CS_VREDRAW | win32con.CS_HREDRAW;
		window_class.hCursor = win32gui.LoadCursor(0, win32con.IDC_ARROW)
		window_class.hbrBackground = win32con.COLOR_WINDOW
		window_class.lpfnWndProc = message_map  # could also specify a wndproc.
		classAtom = win32gui.RegisterClass(window_class)
		# Create the Window.
		style = win32con.WS_OVERLAPPED | win32con.WS_SYSMENU
		self.hwnd = win32gui.CreateWindow(classAtom,
										  self.window_class_name,
										  style,
										  0,
										  0,
										  win32con.CW_USEDEFAULT,
										  win32con.CW_USEDEFAULT,
										  0,
										  0,
										  hinst,
										  None)
		win32gui.UpdateWindow(self.hwnd)
		self.notify_id = None
		self.refresh_icon()

		win32gui.PumpMessages()

	def _add_ids_to_menu_options(self, menu_options):
		result = []
		for menu_option in menu_options:
			if isinstance(menu_option, TrayItem):
				if callable(menu_option.action) or menu_option.action in self.SPECIAL_ACTIONS:
					self.menu_actions_by_id.add((self._next_action_id, menu_option.action))
					menu_option._next_action_id = self._next_action_id
				elif isinstance(menu_option, TraySubmenu):
					# menu_option._next_action_id = self._next_action_id
					menu_option.action = self._add_ids_to_menu_options(menu_option.items)
				result.append(menu_option)
			else:
				print('Unknown item', menu_option.text, menu_option.icon, menu_option.action)
			self._next_action_id += 1
		return result

	def refresh_icon(self):
		# Try and find a custom icon
		hinst = win32gui.GetModuleHandle(None)
		if os.path.isfile(self.icon):
			icon_flags = win32con.LR_LOADFROMFILE | win32con.LR_DEFAULTSIZE
			hicon = win32gui.LoadImage(hinst,
									   self.icon,
									   win32con.IMAGE_ICON,
									   0,
									   0,
									   icon_flags)
		else:
			print("Can't find icon file - using default.")
			hicon = win32gui.LoadIcon(0, win32con.IDI_APPLICATION)

		if self.notify_id:
			message = win32gui.NIM_MODIFY
		else:
			message = win32gui.NIM_ADD
		self.notify_id = (self.hwnd,
						  0,
						  win32gui.NIF_ICON | win32gui.NIF_MESSAGE | win32gui.NIF_TIP,
						  win32con.WM_USER + 20,
						  hicon,
						  self.hover_text)
		win32gui.Shell_NotifyIcon(message, self.notify_id)

	def restart(self, hwnd, msg, wparam, lparam):
		self.refresh_icon()

	def destroy(self, hwnd, msg, wparam, lparam):
		if self.on_quit: self.on_quit(self)
		nid = (self.hwnd, 0)
		win32gui.Shell_NotifyIcon(win32gui.NIM_DELETE, nid)
		win32gui.PostQuitMessage(0)  # Terminate the app.

	def notify(self, hwnd, msg, wparam, lparam):
		if lparam == win32con.WM_LBUTTONDBLCLK:
			self.execute_menu_option(self.default_menu_index + self.FIRST_ID)
		elif lparam == win32con.WM_RBUTTONUP:
			self.show_menu()
		elif lparam == win32con.WM_LBUTTONUP:
			pass
		return True

	def show_menu(self):
		menu = win32gui.CreatePopupMenu()
		self.create_menu(menu, self.menu_options)
		# win32gui.SetMenuDefaultItem(menu, 1000, 0)

		pos = win32gui.GetCursorPos()
		# See http://msdn.microsoft.com/library/default.asp?url=/library/en-us/winui/menus_0hdi.asp
		win32gui.SetForegroundWindow(self.hwnd)
		win32gui.TrackPopupMenu(menu,
								win32con.TPM_LEFTALIGN,
								pos[0],
								pos[1],
								0,
								self.hwnd,
								None)
		win32gui.PostMessage(self.hwnd, win32con.WM_NULL, 0, 0)

	def create_menu(self, menu, menu_options):
		for menu_option in menu_options[::-1]:
			if isinstance(menu_option.icon, str):
				menu_option.icon = self.prep_menu_icon(menu_option.icon)

			if isinstance(menu_option, TraySubmenu):
				submenu = win32gui.CreatePopupMenu()
				self.create_menu(submenu, menu_option.items)
				item, extras = win32gui_struct.PackMENUITEMINFO(text=menu_option.text,
																hbmpItem=menu_option.icon,
																hSubMenu=submenu,
																fState=menu_option.style)
				win32gui.InsertMenuItem(menu, 0, 1, item)
			elif isinstance(menu_option, TrayItem):
				item, extras = win32gui_struct.PackMENUITEMINFO(text=menu_option.text,
																hbmpItem=menu_option.icon,
																wID=menu_option._next_action_id,
																fState=menu_option.style,
																fType=menu_option.type)
				win32gui.InsertMenuItem(menu, 0, 1, item)

	def prep_menu_icon_old(self, icon):
		# First load the icon.
		ico_x = win32api.GetSystemMetrics(win32con.SM_CXSMICON)
		ico_y = win32api.GetSystemMetrics(win32con.SM_CYSMICON)
		hicon = win32gui.LoadImage(0, icon, win32con.IMAGE_ICON, ico_x, ico_y, win32con.LR_LOADFROMFILE)

		hdcBitmap = win32gui.CreateCompatibleDC(0)
		hdcScreen = win32gui.GetDC(0)
		hbm = win32gui.CreateCompatibleBitmap(hdcScreen, ico_x, ico_y)
		hbmOld = win32gui.SelectObject(hdcBitmap, hbm)
		# Fill the background.
		brush = win32gui.GetSysColorBrush(win32con.COLOR_MENU)
		win32gui.FillRect(hdcBitmap, (0, 0, 16, 16), brush)
		# unclear if brush needs to be feed.  Best clue I can find is:
		# "GetSysColorBrush returns a cached brush instead of allocating a new
		# one." - implies no DeleteObject
		# draw the icon
		win32gui.DrawIconEx(hdcBitmap, 0, 0, hicon, ico_x, ico_y, 0, 0, win32con.DI_NORMAL)
		win32gui.SelectObject(hdcBitmap, hbmOld)
		win32gui.DeleteDC(hdcBitmap)

		return hbm

	def prep_menu_icon(self, icon):
		"""
		Ref: https://stackoverflow.com/a/45890829/973425
		:param icon:
		:return:
		"""
		# First load the icon.
		ico_x = win32api.GetSystemMetrics(win32con.SM_CXSMICON)
		ico_y = win32api.GetSystemMetrics(win32con.SM_CYSMICON)
		hIcon = win32gui.LoadImage(0, icon, win32con.IMAGE_ICON, ico_x, ico_y, win32con.LR_LOADFROMFILE)

		hwndDC = win32gui.GetWindowDC(self.hwnd)
		dc = win32ui.CreateDCFromHandle(hwndDC)
		memDC = dc.CreateCompatibleDC()
		iconBitmap = win32ui.CreateBitmap()
		iconBitmap.CreateCompatibleBitmap(dc, ico_x, ico_y)
		oldBmp = memDC.SelectObject(iconBitmap)
		brush = win32gui.GetSysColorBrush(win32con.COLOR_MENU)

		win32gui.FillRect(memDC.GetSafeHdc(), (0, 0, ico_x, ico_y), brush)
		win32gui.DrawIconEx(memDC.GetSafeHdc(), 0, 0, hIcon, ico_x, ico_y, 0, 0, win32con.DI_NORMAL)

		memDC.SelectObject(oldBmp)
		memDC.DeleteDC()
		win32gui.ReleaseDC(self.hwnd, hwndDC)

		return iconBitmap.GetHandle()

	def command(self, hwnd, msg, wparam, lparam):
		id = win32gui.LOWORD(wparam)
		self.execute_menu_option(id)

	def execute_menu_option(self, id):
		menu_action = self.menu_actions_by_id[id]
		if menu_action == self.QUIT:
			win32gui.DestroyWindow(self.hwnd)
		else:
			menu_action(self)
		self.refresh_icon()

	@staticmethod
	def non_string_iterable(obj):
		try:
			iter(obj)
		except TypeError:
			return False
		else:
			return not isinstance(obj, basestring)


# Minimal self test. You'll need a bunch of ICO files in the current working
# directory in order for this to work...
if __name__ == '__main__':
	import fnmatch

	icons = []
	icons_directory = os.path.dirname(os.path.dirname(__file__))
	icons_directory = os.path.join(icons_directory, "app\\static\\images")
	for root, dirnames, filenames in os.walk(icons_directory):
		for filename in fnmatch.filter(filenames, '*.ico'):
			icons.append(os.path.join(root, filename))

	hover_text = "SysTrayIcon.py Demo"

	item_hello = TrayItem()
	item_hello_again = TrayItem()
	submenu = TraySubmenu()


	def hello(sysTrayIcon):
		print("hello")
		if ((item_hello.style & Style.CHECKED)):
			item_hello.style &= ~Style.CHECKED
			item_hello.text = "Unselected"
		# item_hello.style |= Style.UNCHECKED
		else:
			# item_hello.style &= ~Style.UNCHECKED
			item_hello.style |= Style.CHECKED
			item_hello.text = "Selected"


	def hello_again(sysTrayIcon):
		print("Hello Devas.")


	item_hello.text = 'Selected'
	item_hello.action = hello
	item_hello.style = Style.DEFAULT | Style.CHECKED
	item_hello.type = Type.RADIOCHECK

	item_hello_again.text = 'Hello again'
	item_hello_again.action = hello_again
	item_hello_again.style = Style.DEFAULT | Style.CHECKED

	submenu.text = 'A sub-menu'
	submenu.icon = icons[0]
	submenu.items = [item_hello_again]

	menu_options = [
		item_hello,
		TraySeparator(),
		submenu
	]


	def bye(sysTrayIcon):
		print('Bye, then.')


	Tray(icons[0], hover_text, menu_options, on_quit=bye, default_menu_index=1)
