# (C) Copyright 2004 Nuxeo SARL <http://nuxeo.com>
# Author: Julien Anguenot <ja@nuxeo.com>
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License version 2 as published
# by the Free Software Foundation.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA
# 02111-1307, USA.
#
# $Id$

__author__ = "Julien Anguenot <mailto:ja@nuxe.com>"

def install(self):
    """Common installer for CPS 2/3

    Check the version of CPS and invoke the corresponding installer script
    """

    try:
        import Products.CPSCore
        CPS_VERSION = 3
    except ImportError:
        try:
            import Products.NuxCPS
            CPS_VERSION = 2
        except ImportError:
            raise "Unknown version of CPS. Check your installation"

    if CPS_VERSION == 2:
        from Products.CPSTaskTracker.Extensions.install_cps2 import install
        return install(self)
    elif CPS_VERSION == 3:
        from Products.CPSTaskTracker.Extensions.install_cps3 import install
        return install(self)
    else:
        pass
