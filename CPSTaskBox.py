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

__author__ = "Julien Anguenot <mailto:ja@nuxeo.com>"

"""
CPS Task Box
You can access the software requierements specifications within
the docs sub-directory of the product.
"""

from AccessControl import ClassSecurityInfo
from Globals import InitializeClass

from Products.CMFCore.CMFCorePermissions import View
from Products.CMFCore.CMFCorePermissions import ModifyPortalContent

from Products.NuxPortal.BaseBox import BaseBox

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
                  'action': 'CPSTaskBox_editForm',
                  'permissions': (ModifyPortalContent,)},
                 {'id': 'render_title',
                  'name': 'Render title',
                  'action': 'CPSTaskBox_renderTitle',
                  'visible': 0,
                  'permissions': ()},
                 {'id': 'render_body',
                  'name': 'Render body',
                  'action': 'CPSTaskBox_renderBody',
                  'visible': 0,
                  'permissions': ()},
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
    A Box, that can be customized, displaying user related tasks.
    """
    meta_type = 'CPS Task Box'
    portal_type = meta_type

    security = ClassSecurityInfo()

    _properties = BaseBox._properties + (
        {'id':'title', 'type':'string', 'mode':'w',
         'label':'Title'},
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
        {'id':'skinner', 'type':'string', 'mode':'w', \
         'label':'Skinner'},
        )

    visible_if_empty = 0

    #
    # Initialization of the properties
    #

    sort_date_on = "start_date"
    sort_order   = "asc"
    sort_on      = "a" # For the alpha sorting algo

    display_my_tasks = 1
    display_my_affected_tasks = 1
    display_my_groups_affected_tasks = 1
    display_my_accepted_tasks = 1

    skinner = "nuxeo"

    def __init__(self,
                 id,
                 title='',
                 display_my_tasks=1,
                 **kw):
        #
        # Following the box models of NuxPortal
        #
        apply(BaseBox.__init__, (self, id), kw)
        self.title = title

    security.declarePublic("getSortDateOn")
    def getSortDateOn(self):
        """
        Return the possible values for the sort
        parameters date.
        """
        return [
            {'title':'_label_start_date', 'id':'start_date',},
            {'title':'_label_stop_date', 'id':'stop_date',},
            ]

    security.declarePublic("getSortOrder")
    def getSortOrder(self):
        """
        Get the sorting order parameters
        Yes, I know trivial but just to keep the code nice.
        """
        return [{'title':'_label_asc', 'id':'asc'},
                {'title':'_label_desc', 'id':'desc'}
                ]

    security.declarePublic("getSortOn")
    def getSortOn(self):
        """
        Get the sorting types
        """
        return [{'title':'_label_none', 'id':'None'},
                {'title':'_label_type', 'id':'type'},
                {'title':'_label_priority', 'id':'priority'},
                ]

    security.declareProtected("changeScreenerProperties", ModifyPortalContent)
    def changeScreenerProperties(self, form):
        """
        Change the properties of the sreener
        """
        self.sort_date_on = form.get('sort_date_on', 'start_date')
        self.sort_order = form.get('sort_order', 'asc')
        self.sort_on = form.get('sort_on', '')
        self.display_my_tasks = form.get('display_my_tasks', 0) and 1
        self.display_my_affected_tasks = form.get(\
            'display_my_affected_tasks', 0) and 1
        self.display_my_groups_affected_tasks = form.get(\
            'display_my_groups_affected_tasks', 0) and 1
        self.display_my_accepted_tasks = form.get(\
            'display_my_accepted_tasks', 0) and 1

        self.skinner = form.get('skinner', 'nuxeo')

        return 1 # useless since now.

    security.declareProtected("getParameters", View)
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

InitializeClass(CPSTaskBox)


def addCPSTaskBox(dispatcher, id, REQUEST=None, **kw):
    """Add a CPS Task  Box."""
    ob = CPSTaskBox(id, **kw)
    dispatcher._setObject(id, ob)
    if REQUEST is not None:
        url = dispatcher.DestinationURL()
        REQUEST.RESPONSE.redirect('%s/manage_main' % url)
