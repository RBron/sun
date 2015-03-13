#!/usr/bin/python
# -*- coding: utf-8 -*-

# sun_gtk is a path of sun.

# Copyright 2015 Dimitris Zlatanidis <d.zlatanidis@gmail.com>
# All rights reserved.

# sun is a tray notification applet for informing about
# package updates in Slackware.

# https://github.com/dslackw/sun

# sun is free software: you can redistribute it and/or
# modify it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.

import gtk
import commands
import subprocess
from sun.__metadata__ import (
    __all__,
    icon_path
)
from sun.utils import fetch


class GtkStatusIcon(object):

    def __init__(self):
        self.sun_icon = "{0}{1}.png".format(icon_path, __all__)
        self.icon = gtk.status_icon_new_from_file(self.sun_icon)
        self.icon.connect('popup-menu', self.right_click)
        self.cmd = "/etc/rc.d/rc.sun"
        gtk.main()

    def icon_menu(self, event_button, event_time, data=None):
        menu = gtk.Menu()

        menu_item = gtk.ImageMenuItem("About")
        img = gtk.image_new_from_stock(gtk.STOCK_REFRESH, gtk.ICON_SIZE_MENU)
        img.show()
        menu_item.set_image(img)
        menu.append(menu_item)
        menu_item.show()

        about = gtk.MenuItem("About")
        start = gtk.MenuItem("Start daemon")
        stop = gtk.MenuItem("Stop daemon")
        restart = gtk.MenuItem("Restart daemon")
        check = gtk.MenuItem("Check updates")
        status = gtk.MenuItem("Status daemon")
        exit_sun = gtk.MenuItem("Exit")

        menu_items = [about, start, stop, restart, check, status, exit_sun]
        for item in menu_items:
            menu.append(item)

        about.connect_object("activate", self._about, "About")
        start.connect_object("activate", self._start, "Start daemon")
        stop.connect_object("activate", self._stop, "Stop daemon")
        restart.connect_object("activate", self._restart, "Restart daemon")
        check.connect_object("activate", self._check, "Check updates")
        status.connect_object("activate", self._status, "Status daemon")
        exit_sun.connect_object("activate", self._exit, "Exit")

        for item in menu_items:
            item.show()

        menu.popup(None, None, None, event_button, event_time, data)

    def message(self, data):
        """ Function to display messages to the user """

        msg = gtk.MessageDialog(None, gtk.DIALOG_MODAL, gtk.MESSAGE_INFO,
                                gtk.BUTTONS_OK, data)
        img = gtk.Image()
        img.set_from_file(self.sun_icon)
        msg.set_image(img)

        # action_area = msg.get_content_area()
        # label_2 = gtk.Label("Slackware Update Notifier")
        # action_area.add(label_2)

        msg.show_all()
        msg.run()
        msg.destroy()

    def right_click(self, data, event_button, event_time):
        self.icon_menu(event_button, event_time)

    def _about(self, data):
        self.message(data)

    def _start(self, data):
        subprocess.call("{0} {1}".format(self.cmd, "start"), shell=True)
        self.message("Starting sun daemon ...")

    def _stop(self, data):
        subprocess.call("{0} {1}".format(self.cmd, "stop"), shell=True)
        self.message("Stoping sun daemon ...")

    def _restart(self, data=None):
        subprocess.call("{0} {1}".format(self.cmd, "restart"), shell=True)
        self.message("Restarting sun daemon ...")

    def _check(self, data):
        upgraded, packages = fetch()[2:]
        if upgraded > 0:
            self.message("{0} software updates are available "
                         "!\n\n{1}".format(str(upgraded), "\n".join(packages)))
        else:
            self.message("No news is good news !")

    def _status(self, data):
        out = commands.getoutput("ps -A")
        if "sun_daemon" in out:
            self.message("sun is running ...")
        else:
            self.message("sun not running")

    def _exit(self, data):
        subprocess.call("{0} {1}".format(self.cmd, "stop"), shell=True)
        gtk.main_quit()


def main():

    GtkStatusIcon()

if __name__ == '__main__':
    main()