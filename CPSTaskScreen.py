# (c) 2002 Nuxeo SARL <http://nuxeo.com>
# (c) 2003 CEA <http://www.cea.fr>
# Author:Julien Anguenot <ja@nuxeo.com>
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

"""
  CPS Task Screen
"""

from zLOG import LOG, DEBUG

from Globals import InitializeClass
from AccessControl import ClassSecurityInfo

from Products.CMFCore.utils import getToolByName
from Products.CMFCore.CMFCorePermissions import View, ModifyPortalContent

from Products.NuxCPSDocuments.BaseDocument import BaseDocument, BaseDocument_adder

factory_type_information = (
    {'id': 'CPS Task Screen',
     'title': '_portal_type_CPS_Task_Screen',
     'content_icon': 'document_icon.png',
     'product': 'CPSTaskTracker',
     'factory': 'addCPSTaskScreen',
     'meta_type': 'CPS Task Screen',
     'immediate_view': 'cps_task_screen_edit_form',
     'allow_discussion': 1,
     'filter_content_types': 0,
     'actions': ({'id': 'view',
                  'name': '_action_view_',
                  'action': 'cps_task_screen_view',
                  'permissions': (View,)},
                 {'id': 'edit',
                  'name': '_action_modify_',
                  'action': 'cps_task_screen_edit_form',
                  'permissions': (ModifyPortalContent,)},
                 {'id': 'create',
                  'name': '_action_create_',
                  'action': 'cps_task_screen_create_form',
                  'visible': 0,
                  'permissions': ()},
                 {'id': 'content_view',
                  'name': 'content_view',
                  'action': 'cps_task_screen_content_view',
                  'visible': 0,
                  'permissions': (View, )},
                 {'id': 'isdocument',
                  'name': 'isdocument',
                  'action': 'isdocument',
                  'visible': 0,
                  'permissions': ()},
                 {'id': 'issearchabledocument',
                  'name': 'issearchabledocument',
                  'action': 'issearchabledocument',
                  'visible': 0,
                  'permissions': ()},
                 ),
     },
    )

class CPSTaskScreen(BaseDocument):
    """
    CPS Task Screen
    """
    meta_type = 'CPS Task Screen'

    portal_type = 'CPS Task Screen'

    security = ClassSecurityInfo()

InitializeClass(CPSTaskScreen)


def addCPSTaskScreen(dispatcher, id, REQUEST=None, **kw):
    """Add CPS Task Screen."""
    ob = CPSTaskScreen(id, **kw)
    return BaseDocument_adder(dispatcher, id, ob, REQUEST=REQUEST)
