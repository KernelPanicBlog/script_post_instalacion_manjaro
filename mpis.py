#!/usr/bin/env python3
#-*- coding: utf-8 -*-
#
# This file is part of MPIS (https://github.com/KernelPanicBlog/MPIS).
#
# MPIS(Manjaro Post Installation Script) is free software; you can redistribute
# it and/or modify it under the terms of the GNU General Public License as
# published by the Free Software Foundation; either version 3 of the License,or
# any later version.
#
# MPIS (Manjaro Post Installation Script):
# It allows  users to choose different options such as
# install an application or CONFIG some tools and environments.
#
# MPIS is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with MPIS; If not, see <http://www.gnu.org/licenses/>.
# ______________________________________________________________________________
import sys
import traceback
import webbrowser
import mpislib
from mpislib.core import db
from mpislib.core import resource
from mpislib.core import user_input
from mpislib.core import pause
from mpislib.core import clear
from mpislib.core import mkopts
from mpislib.core import show_banner
from mpislib.core import sleep
from mpislib.core import execute_command
from mpislib.core import wizard_config
from mpislib.core import set_language
from mpislib.core import toggle_config
from mpislib.menu import GlobalMenu
from mpislib.traslate import tr
from mpislib.colorize import colorize


list_cmd_to_install = []
try:
    show_banner()
    sleep(2)
    clear()
    print(colorize.aplicar(1, 31)
          + tr("The '--noconfirm' parameter is enabled by default."))
    print(tr("You can change this option in the Settings menu.")
          + colorize.reset())
    sleep(2)
    clear()
    option = 0
    menu_back = []
    GlobalMenu.load_appearance()
    menu = GlobalMenu.nodos[option]
    GlobalMenu.show_menu(menu, True if list_cmd_to_install else False)
    while True:
        try:
            option = user_input()
            if option in mkopts("back"):
                if len(menu_back):
                    menu = menu_back.pop()
            elif option in mkopts("help"):
                clear()
                title_text_colour = db.get_config("title_text_colour")
                title_back_colour = db.get_config("title_back_colour")
                option_menu_colour = db.get_config("option_menu_colour")

                print(colorize.aplicar(1, title_text_colour, title_back_colour)
                      + tr("Help") + colorize.reset())

                string = colorize.aplicar(1, option_menu_colour)
                string += "\n" + tr("You can select an option with the given number or write 4 shortcuts:")
                string += "\n" + tr("back or b -> Return to the previous option.")
                string += "\n" + tr("help or h -> Show help.")
                string += "\n" + tr("exit or e or Ctrl+C -> Finish execution script.")
                string += "\n" + tr("Tasks or t -> Execute the tasks added to the list.")
                print(string + colorize.reset())

                pause("\n")

            elif option in mkopts("tasks"):
                print(tr("We will proceed to install the selected applications."))
                for _cmd_ in list_cmd_to_install:
                    execute_command(_cmd_)
                list_cmd_to_install.clear()
            elif option in mkopts("exit"):
                sys.exit(0)
            elif int(option) <= len(menu.childern):
                option = int(option)
                if len(menu[option].childern):
                    menu_back.append(menu)
                    menu = menu.childern[option]
                else:
                    if menu.name == tr("Personalization"):
                        pause(tr("(not functional, yet)"))
                    elif menu.childern[option].name == tr("Appearance"):
                        wizard_config()
                        GlobalMenu.load_appearance()
                    elif menu.childern[option].name == tr("Set language"):
                        set_language()
                    elif menu.childern[option].name == tr("Toggle --noconfirm"):
                        toggle_config("noconfirm")
                    elif menu.childern[option].name == tr("Toggle multi-install"):
                        toggle_config("multi_install")
                    elif menu.childern[option].name == tr("About MPIS"):
                        show_banner()
                    elif menu.childern[option].name == tr("Report bug!"):
                        web_bug = "https://github.com/KernelPanicBlog/MPIS/issues"
                        webbrowser.open(web_bug)
                        clear()
                        pause(tr("Link is opening in your web browser."))
                    elif menu.childern[option].name == tr("See README File"):
                        with open(resource.path_file("README.rst"),
                                  "r") as _file:
                            pause(_file.read())
                    elif menu.childern[option].name == tr("See CHANGELOG File"):
                        with open(resource.path_file("CHANGELOG.rst"),
                                  "r") as _file:
                            pause(_file.read())
                    elif menu.childern[option].name == tr("See the content of mirrorlist file"):
                        with open("/etc/pacman.d/mirrorlist",
                                  "r") as _file:
                            pause(_file.read())
                    else:
                        arg = True if menu.parent.split()[0] == tr("Install") else False
                        cmd_ = db.get_command(menu.childern[option].name, arg)
                        if db.get_config('multi_install') == 'True':
                            list_cmd_to_install.append(cmd_)
                            pause(tr("The tasks was added to the installation list."))
                        else:
                            execute_command(cmd_)
            else:
                pause(tr("Sorry not valid Option."))
        except (ValueError, IndexError):
            pause(tr("Error in option, this value is outside the range of the list"))
        clear()
        GlobalMenu.show_menu(menu, True if list_cmd_to_install else False)
except KeyboardInterrupt:
    print(colorize.aplicar(1, 31)
          + tr("You had press the Ctrl+C keys combination. Accepted exit request. Bye!"))
    sleep(2)
    clear()
except Exception:
    traceback.print_exc(file=sys.stdout)
sys.exit(0)
