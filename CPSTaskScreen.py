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

from Products.NuxCPSDocuments.BaseDocument import BaseDocument, \
     BaseDocument_adder

factory_type_information = (
    {'id': 'CPS Task Screen',
     'title': '_portal_type_CPS_Task_Screen',
     'content_icon': 'task_screen_icon.png',
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
                  'name': '_action_edit_',
                  'action': 'cps_task_screen_edit_form',
                  'permissions': (ModifyPortalContent,)},
                 {'id': 'action_parameters',
                  'name': 'action_parameters',
                  'action': 'cps_task_screen_edit_parameters_form',
                  'permissions': (ModifyPortalContent,)},
                 {'id': 'create',
                  'name': '_action_create_',
                  'action': 'cps_task_screen_create',
                  'visible': 0,
                  'permissions': ()},
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

    #
    # Filtering properties
    #

    _properties = BaseDocument._properties + (
        {'id':'sort_date_on', 'type':'string', 'mode':'w', \
         'label':'Sort on date'},
        {'id':'sort_order', 'type':'string', 'mode':'w', \
         'label':'Sort order'},
        {'id':'sort_on', 'type':'string', 'mode':'w', \
         'label':'Sort on'},
        {'id':'display_my_tasks', 'type':'boolean', 'mode':'w', \
         'label':'Display my tasks ?'},
        {'id':'display_my_affected_tasks', 'type':'boolean', 'mode':'w', \
         'label':'Display the tasks affected to me ?'},
        {'id':'display_my_groups_affected_tasks', 'type':'boolean', 'mode':'w', \
         'label':'Display the tasks affected to a one if my groups ?'},
        {'id':'display_my_accepted_tasks', 'type':'boolean', 'mode':'w', \
         'label':'Display the tasks I accepted ?'},
        )

    #
    # Initialization of the properties
    #

    # start_date, end_date
    sort_date_on = "start_date"
    # asc, desc
    sort_order   = "asc"

    # type, indicator or priority
    sort_on = "a" # For the alpha sorting algo

    display_my_tasks = 1
    display_my_affected_tasks = 1
    display_my_groups_affected_tasks = 1
    display_my_accepted_tasks = 1

    def __init__(self, id, **kw):
        """
        BaseDocument constructor +
        parameters ??
        XXX : TODO
        """
        BaseDocument.__init__(self, id, **kw)

    security.declareProtected("sortTasks", "Modify portal content")
    def changeScreenerProperties(self, form):
        """
        Change the properties of the sreener
        """
        self.sort_date_on = form.get('sort_date_on', 'start_date')
        self.sort_order = form.get('sort_order', 'asc')
        self.sort_on = form.get('sort_on', '')
        self.display_my_tasks = form.get('display_my_tasks', 0) and 1
        self.display_my_affected_tasks = form.get('display_my_affected_tasks', 0) and 1
        self.display_my_groups_affected_tasks = form.get('display_my_groups_affected_tasks', 0) and 1
        self.display_my_accepted_tasks = form.get('display_my_accepted_tasks', 0) and 1

    security.declareProtected("getParameters", "Modify portal content")
    def getParameters(self):
        """
        Return a dictionnary containing the sorting
        parameters.
        To be passed to the portak_tasks search API
        """

        struct = {}
        struct['sort_date_on'] = self.sort_date_on
        struct['sort_order'] = self.sort_order
        struct['sort_on'] = self.sort_on
        struct['display_my_tasks'] = self.display_my_tasks
        struct['display_my_affected_tasks'] = self.display_my_affected_tasks
        struct['display_my_groups_affected_tasks'] = self.display_my_groups_affected_tasks
        struct['display_my_accepted_tasks'] = self.display_my_accepted_tasks

        return struct

InitializeClass(CPSTaskScreen)


def addCPSTaskScreen(dispatcher, id, REQUEST=None, **kw):
    """Add CPS Task Screen."""
    ob = CPSTaskScreen(id, **kw)
    return BaseDocument_adder(dispatcher, id, ob, REQUEST=REQUEST)
