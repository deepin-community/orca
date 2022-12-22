# Orca
#
# Copyright 2004-2008 Sun Microsystems Inc.
#
# This library is free software; you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public
# License as published by the Free Software Foundation; either
# version 2.1 of the License, or (at your option) any later version.
#
# This library is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with this library; if not, write to the
# Free Software Foundation, Inc., Franklin Street, Fifth Floor,
# Boston MA  02110-1301 USA.

"""Provides i18n support for orca using the gettext module.  Tells
gettext where to find localized strings and creates an alias, _, that
maps to the gettext.gettext function.  This function will accept a
string and return a localized string for that string.
"""

import gettext
import imp
import os
import sys

# Alias gettext.gettext to _ and gettext.ngettext to ngettext
#
_ = gettext.gettext
ngettext = gettext.ngettext
cgettext = gettext.gettext

# Tell gettext where to find localized strings.
#
localedir = "${prefix}/share/locale".replace('${prefix}', '/home/jd/checkout/orca/bld')
gettext.bindtextdomain ("orca", localedir)
gettext.textdomain("orca")

########################################################################
#                                                                      #
# Utility methods to facilitate easier translation                     #
#                                                                      #
########################################################################

def C_(ctx, s):
    """Provide qualified translatable strings via context."""
    translated = cgettext('%s\x04%s' % (ctx, s))
    if '\x04' in translated:
        # no translation found, return input string
        return s
    return translated

def setModuleLocale(moduleName, newLocale=None):
    global _, ngettext, cgettext

    try:
        translation = gettext.translation('orca', localedir, languages=[newLocale])
        _ = translation.gettext
        ngettext = translation.ngettext
        cgettext = translation.gettext
    except:
        _ = gettext.gettext
        ngettext = gettext.ngettext
        cgettext = gettext.gettext
    module = sys.modules.get(moduleName)
    if module:
        imp.reload(module)

def setLocaleForMessages(newLocale=None):
    modules = ['orca.tutorialgenerator', 'orca.messages']
    for module in modules:
        setModuleLocale(module, newLocale)

def setLocaleForNames(newLocale=None):
    modules = ['orca.chnames', 'orca.keynames', 'orca.phonnames',
               'orca.text_attribute_names', 'orca.object_properties',
               'orca.cmdnames', 'orca.keybindings', 'orca.colornames',
               'orca.mathsymbols']
    for module in modules:
        setModuleLocale(module, newLocale)

def setLocaleForGUI(newLocale=None):
    modules = ['orca.orca_gtkbuilder',
               'orca.guilabels',
               'orca.brltablenames']
    for module in modules:
        setModuleLocale(module, newLocale)
