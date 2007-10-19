# (c) 2004 Nuxeo SARL <http://nuxeo.com>
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

__author__ = "Julien Anguenot <mailto:ja@nuxeo.com>"

"""CPS Task Screen

You can access the software requierements specifications within
the docs sub-directory of the product.
"""

from zLOG import LOG, DEBUG

from Globals import InitializeClass
from AccessControl import ClassSecurityInfo

from Products.CMFCore.CMFCorePermissions import View, ModifyPortalContent
from Products.CPSCore.CPSBase import CPSBaseDocument, CPSBase_adder

from TaskTrackerPropertyManager import TaskTrackerPropertyManager

factory_type_information = (
    {'id': 'CPS Task Screen',
     'title': '_portal_type_CPS_Task_Screen',
     'content_icon': 'task_screen_icon.png',
     'product': 'CPSTaskTracker',
     'factory': 'addCPSTaskScreen',
     'meta_type': 'CPS Task Screen',
     'immediate_view': 'cps_task_screen_edit_form',
     'allow_discussion': 0,
     'filter_content_types': 0,
     'actions': ({'id': 'view',
                  'name': 'action_view',
                  'action': 'cps_task_screen_view',
                  'permissions': (View,)},
                 {'id': 'edit',
                  'name': 'action_edit',
                  'action': 'cps_task_screen_edit_form',
                  'permissions': (ModifyPortalContent,)},
                 {'id': '_action_parameters',
                  'name': '_action_parameters',
                  'action': 'cps_task_screen_edit_parameters_form',
                  'permissions': (ModifyPortalContent,)},
                 {'id': 'create',
                  'name': '_action_create_',
                  'action': 'cps_task_screen_create',
                  'visible': 0,
                  'permissions': ()},
                 )
     },
    )

class CPSTaskScreen(CPSBaseDocument, TaskTrackerPropertyManager):
    """CPS Task Screen
    """

    meta_type = 'CPS Task Screen'
    portal_type = meta_type

    _properties = CPSBaseDocument._properties + \
                  TaskTrackerPropertyManager._properties

InitializeClass(CPSTaskScreen)

def addCPSTaskScreen(container, id, REQUEST=None, **kw):
    """Add CPS Task Screen.
    """
    ob = CPSTaskScreen(id, **kw)
    return CPSBase_adder(container, ob, REQUEST=REQUEST)
