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

"""Task Tracker Property Manager

The aim of this class is to to store parameters corresponding to the
box (CPSTaskBox)and screener (CPSTaskScreen) parameter options.

It contains attributes and an API to access them.
"""

from Globals import InitializeClass
from AccessControl import ClassSecurityInfo

from Products.CMFCore.utils import getToolByName
from Products.CMFCore.CMFCorePermissions import View, ModifyPortalContent

class TaskTrackerPropertyManager:
    """TaskTrackerProperyManager class
    """

    security = ClassSecurityInfo()

    _properties = ({'id':'sort_date_on',
                    'type':'string',
                    'mode':'w',
                    'label':'Sort on date'},
                   {'id':'sort_order',
                    'type':'string',
                    'mode':'w',
                    'label':'Sort order'},
                   {'id':'sort_on',
                    'type':'string',
                    'mode':'w',
                    'label':'Sort on'},
                   {'id':'display_my_tasks',
                    'type':'boolean',
                    'mode':'w',
                    'label':'Display my tasks ?'},
                   {'id':'display_my_affected_tasks',
                    'type':'boolean',
                    'mode':'w',
                    'label':'Display the tasks affected to me ?'},
                   {'id':'display_my_groups_affected_tasks',
                    'type':'boolean',
                    'mode':'w',
                    'label':'Display tasks assigned to one of my groups ?'},
                   {'id':'display_my_accepted_tasks',
                    'type':'boolean',
                    'mode':'w',
                    'label':'Display the tasks I accepted ?'},
                   {'id':'display_on_project',
                    'type':'string',
                    'mode':'w',
                    'label':'Display the project ?'},
                   {'id':'skinner',
                    'type':'string',
                    'mode':'w',
                    'label':'Skinner'},
                   )

    # start_date, end_date
    sort_date_on = "start_date"
    # asc, desc
    sort_order   = "asc"

    # type, project or priority
    sort_on = "a" # For the alpha sorting algo

    display_my_tasks = 1
    display_my_affected_tasks = 1
    display_my_groups_affected_tasks = 1
    display_my_accepted_tasks = 1
    display_on_project = ""

    skinner = 'default'

    security.declarePublic("getSortDateOn")
    def getSortDateOn(self):
        """Return the possible values for the sort parameters date.
        """
        return [
            {'title':'_label_start_date', 'id':'start_date',},
            {'title':'_label_stop_date', 'id':'stop_date',},
            ]

    security.declarePublic("getSortOrder")
    def getSortOrder(self):
        """Get the sorting order parameters

        Yes, I know trivial but just to keep the code nice.
        """
        return [{'title':'_label_asc', 'id':'asc'},
                {'title':'_label_desc', 'id':'desc'}
                ]

    security.declarePublic("getSortOn")
    def getSortOn(self):
        """Get the sorting types
        """
        return [{'title':'_label_none', 'id':'None'},
                {'title':'_label_type', 'id':'type'},
                {'title':'_label_priority', 'id':'priority'},
                {'title':'_label_project', 'id':'project'},
                ]

    security.declareProtected(ModifyPortalContent, 'updateParameters')
    def updateParameters(self, form):
        """Change the properties of the sreener
        """

        self.sort_date_on = form.get('sort_date_on', 'start_date')
        self.sort_order = form.get('sort_order', 'asc')
        self.sort_on = form.get('sort_on', '')
        self.display_my_tasks = form.get('display_my_tasks', 0) and 1
        self.display_my_affected_tasks = form.get('display_my_affected_tasks', 0) and 1
        self.display_my_groups_affected_tasks = form.get('display_my_groups_affected_tasks', 0) and 1
        self.display_my_accepted_tasks = form.get('display_my_accepted_tasks',0) and 1
        self.display_on_project = form.get('display_on_project',"")
        self.skinner = form.get('skinner', 'default')

    security.declareProtected(View, 'getParameters')
    def getParameters(self):
        """Return a dictionnary containing the sortingparameters.

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
        struct['display_on_project'] = self.display_on_project

        return struct

InitializeClass(TaskTrackerPropertyManager)
