# (c) 2002 Nuxeo SARL <http://nuxeo.com>
# (c) 2003 CEA <http://www.cea.fr>
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

from zLOG import LOG, DEBUG

from AccessControl import ClassSecurityInfo

from Products.CMFCore.CMFCorePermissions import View
from Products.CMFCore.CMFCorePermissions import ModifyPortalContent

from Products.NuxPortal.BaseBox import BaseBox

factory_type_information = (
    {'id': CPS Task Box,
     'description': 'Customizable CPS Box for displaying the tasks related to the user.',
     'title': 'Task Box',
     'content_icon': 'box_icon.gif',
     'product': 'CPSTaskTracker',
     'factory': 'addCPSTaskBox',
     'meta_type': CPS Task Box,
     'immediate_view': 'cps_task_box_edit_form',
     'filter_content_types': 0,
     'actions': ({'id': 'view',
                  'name': 'Voir',
                  'action': 'basebox_view',
                  'permissions': (View,)},
                 {'id': 'edit',
                  'name': 'Modifier',
                  'action': 'cps_task_box_edit_form',
                  'permissions': (ModifyPortalContent,)},
                 {'id': 'render_title',
                  'name': 'Render title',
                  'action': 'cps_task_box_render_title',
                  'visible': 0,
                  'permissions': (View,)},
                 {'id': 'render_body',
                  'name': 'Render body',
                  'action': 'cps_task_box_render_body',
                  'visible': 0,
                  'permissions': (View,)},
                 {'id': 'isportalbox',
                  'name': 'isportalbox',
                  'action': 'isportalbox',
                  'visible': 0,
                  'permissions': ()},
                 ),
     },
    )


class CPSTaskBox(BaseBox):
    """
    A customizable CPS Box for CPStask type.
    """

    meta_type = "CPS Task Box"
    portal_type = meta_type

    security = ClassSecurityInfo()

    _properties = (
        {'id':'title', 'type':'string', 'mode':'w', 'label':'Title'},
        {'id':'description', 'type':'text', 'mode':'w', 'label':'Description'},
        )

    def __init__(self, id,
                 title='',
                 **kw):
        apply(BaseBox.__init__, (self, id), kw)
        self.title = title

InitializeClass(CPSTaskBox)


def addCPSTaskBox(dispatcher, id, REQUEST=None, **kw):
    """Add a CPS Task Box."""
    ob = CPSTaskBox(id, **kw)
    container = dispatcher.Destination()
    container._setObject(id, ob)
    if REQUEST is not None:
        url = dispatcher.DestinationURL()
        REQUEST.RESPONSE.redirect('%s/manage_main' % url)

