# (c) 2004 Nuxeo SARL <http://nuxeo.com>
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

__author__ = "Julien Anguenot <mailto:ja@nuxeo.com>"

"""CPS Task Box

You can access the software requierements specifications within
the docs sub-directory of the product.
"""

from AccessControl import ClassSecurityInfo
from Globals import InitializeClass

from Products.CMFCore.CMFCorePermissions import View, ModifyPortalContent

from Products.CPSDefault.BaseBox import BaseBox

from TaskTrackerPropertyManager import TaskTrackerPropertyManager

factory_type_information = (
    {'id': 'CPS Task Box',
     'title': '_portal_type_task Box',
     'description': ('A Task Box.'),
     'meta_type': 'CPS Task Box',
     'content_icon': 'box_icon.gif',
     'product': 'CPSTaskTracker',
     'factory': 'addCPSTaskBox',
     'immediate_view': 'CPSTaskBox_editForm',
     'filter_content_types': 0,
     'actions': ({'id': 'view',
                  'name': 'View',
                  'action': 'basebox_view',
                  'permissions': (View,)},
                 {'id': 'edit',
                  'name': 'Edit',
                  'action': 'cpstaskbox_edit_form',
                  'permissions': (ModifyPortalContent,)},
                 ),
     'cps_is_portalbox': 1,
     },
    )

class CPSTaskBox(BaseBox, TaskTrackerPropertyManager):
    """CPSTaskBox

    A Box, that can be customized, displaying user related tasks.
    """

    meta_type = 'CPS Task Box'
    portal_type = meta_type

    security = ClassSecurityInfo()

    _properties = BaseBox._properties + \
                  TaskTrackerPropertyManager._properties

    def __init__(self, id, **kw):
        """CPSTaskBox Constructor
        """
        BaseBox.__init__(self, id, provider="cps_task_tracker", **kw)

InitializeClass(CPSTaskBox)


def addCPSTaskBox(dispatcher, id, REQUEST=None, **kw):
    """Add a CPS Task  Box.
    """
    ob = CPSTaskBox(id, **kw)
    dispatcher._setObject(id, ob)
    if REQUEST is not None:
        url = dispatcher.DestinationURL()
        REQUEST.RESPONSE.redirect('%s/manage_main' % url)
