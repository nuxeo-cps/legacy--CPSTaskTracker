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

__author__ = "Julien Anguenot <mailto:ja@nuxeo.com>"

"""
CPS Task Type.
You can access the software requierements specifications within
the docs sub-directory of the product.
Notice that this type is following a given workflow defined in
the Install sub-directory of this product.
"""

import string
from types import ListType
from DateTime import DateTime

from zLOG import LOG, DEBUG

from Globals import InitializeClass
from AccessControl import ClassSecurityInfo

from Products.CMFCore.utils import getToolByName
from Products.CMFCore.CMFCorePermissions import View, ModifyPortalContent

from Products.NuxCPSDocuments.BaseDocument import BaseDocument_adder
from Products.NuxCPSFlexibleDocument.FlexibleDocument import FlexibleDocument


factory_type_information = (
    {'id': 'CPS Task',
     'title': '_portal_type_CPS_Task',
     'content_icon': 'task_icon.png',
     'product': 'CPSTaskTracker',
     'factory': 'addCPSTask',
     'meta_type': 'CPS Task',
     'immediate_view': 'cps_task_edit_form',
     'allow_discussion': 1,
     'filter_content_types': 0,
     'actions': ({'id': 'view',
                  'name': '_action_view_',
                  'action': 'cps_task_view',
                  'permissions': (View,)},
                 {'id': 'create',
                  'name': '_action_create_',
                  'action': 'cps_task_create',
                  'visible': 0,
                  'permissions': ()},
                 {'id': 'edit',
                  'name': '_action_modify_',
                  'action': 'cps_task_edit_form',
                  'permissions': (ModifyPortalContent,)},
                 {'id': 'recall',
                  'name': '_action_recall_',
                  'action': 'cps_task_recall_assigned_form',
                  'permissions': (ModifyPortalContent,)},
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

class CPSTask(FlexibleDocument):
    """
    CPS Task Type.
    """

    meta_type   = 'CPS Task'
    portal_type = meta_type

    security = ClassSecurityInfo()

    _properties = FlexibleDocument._properties + (
        {'id':'start_task_date', 'type':'date', 'mode':'w', \
         'label':'Task begins'},
        {'id':'stop_task_date', 'type':'date', 'mode':'w', \
         'label':'Task ends'},
        {'id':'task_priority', 'type':'string', 'mode':'w', \
         'label':'Task Priority'},
        {'id':'task_indicator', 'type':'string', 'mode':'w', \
         'label':'Task Indicator'},
        {'id':'task_type', 'type':'string', 'mode':'w', \
         'label':'Task Type'},
        {'id':'task_project', 'type':'text', 'mode':'w', \
         'label':'Task Project'},
        {'id':'task_goal', 'type':'text', 'mode':'w', \
         'label':'Task Goal'},
        {'id':'members', 'type':'text', 'mode':'w', \
         'label':'Task  Assigned to Members'},
        {'id':'groups', 'type':'text', 'mode':'w', \
         'label':'Task  Assigned to Groups'},
        )

    #
    # Initialization of the properties
    #

    start_task_date = ''
    stop_task_date  = ''
    task_priority   = 'normal'
    task_indicator  = 'normal'
    task_type       = ''
    task_project    = ''
    task_goal       = ''
    members = ''
    groups  = ''
    the_assigned = None   # the one who accepted it.
    is_closed = 0         # flag to see if the task has been closed.
    task_rejecter = []    # People who rejected the task

    security.declarePublic("getMemberIds")
    def getMemberIds(self):
        """
        Return the member ids only
        """

        if self.members != '':
            return string.split(self.members[1], "\r\n")

        # No members assigned to this task
        return []

    security.declarePrivate("getCurrentMemberId")
    def getCurrentMemberId(self):
        """
        Return the current logged in member
        """
        portal = self.portal_url.getPortalObject()
        member = portal.portal_membership.getAuthenticatedMember()

        return member.getMemberId()

    security.declarePublic("getGroupIds")
    def getGroupIds(self):
        """
        Return the group ids only
        """

        if self.groups != '':
            return string.split(self.groups[1], "\r\n")

        # No groups assigned to this task
        return []

    security.declarePublic("isAssigned")
    def isAssigned(self):
        """
        Check if member_id is assigned to this task
        """
        portal = self.portal_url.getPortalObject()
        member_id = self.getCurrentMemberId()

        # Checking if the task is closed or not
        if self.isClosed():
            return 0

        # Checking if someone already accepted the task
        the_assigned = self.getTheAssignedOne()
        if  the_assigned is not None:
            return 0

        # Checking if the user rejected the task
        if member_id in self.task_rejecter:
            return 0

        # Checking within the assigned members.
        if member_id in self.getMemberIds():
            return 1
        #
        # Loop over the groups to see if the user
        # belongs to one of the groups
        #
        if self.getGroupIds() == []:
            return 0
        for group_id in self.getGroupIds():
            if group_id != '':
                group = portal.acl_users.getGroupById(group_id)
                if member_id in group.getUsers():
                    return 1

        return 0

    security.declarePublic("isCreator")
    def isCreator(self):
        """
        Check if member_id is the creator of the task
        """
        member_id = self.getCurrentMemberId()
        return member_id == self.Creator()

    security.declarePublic("acceptTask")
    def acceptTask(self):
        """
        Someone is accepting the task from the people who were
        assigned to it.
        """
        member_id = self.getCurrentMemberId()
        self.the_assigned = member_id

    security.declarePublic("getTheAssignedOne")
    def getTheAssignedOne(self):
        """
        Return the person who accepted the task
        """
        return self.the_assigned

    security.declarePublic("isTheAssignedOne")
    def isTheAssignedOne(self):
        """
        Check if the user the one who accepted the task
        """
        member_id = self.getCurrentMemberId()
        return member_id == self.the_assigned

    security.declarePublic("closeTask")
    def closeTask(self):
        """
        Close the task.
        """
        if self.isTheAssignedOne():
            self.is_closed = 1
            self.the_assigned = None

    security.declarePublic("isClosed")
    def isClosed(self):
        """
        Is the task closed
        """
        return self.is_closed

    security.declarePrivate("isLate")
    def isLate(self):
        """
        Is the task late according to the deadline.
        """
        today = DateTime()
        task_deadline = DateTime(str(self.stop_task_date) + " 0:00am")
        return today >= task_deadline

    security.declareProtected('getStatus', View)
    def getStatus(self):
        """
        Return the status of the task.
        """

        #
        # OPENED : not assigned yet.
        # ASSIGNED : no comment
        # CLOSED : no comment
        # LATE : according to the deadline.
        #

        if self.isClosed():
            return "closed"
        elif self.the_assigned is not None:
            return "assigned"
        elif self.isLate():
            return "late"
        else:
            return "opened"

    security.declarePublic("changeAssigned")
    def changeAssigned(self, members='', groups=''):
        """
        After the task had been closed we can re-assigned it to others
        """

        #
        # Re-assigning
        #

        self.members = members
        self.groups  = groups

        #
        # Re-opening it
        #

        self.is_closed = 0

        #
        # Re-init
        #

        self.the_assigned = None
        self.task_rejecter = []

    security.declarePublic("rejectTask")
    def rejectTask(self):
        """
        The user rejects the task
        """
        member_id = self.getCurrentMemberId()
        self.task_rejecter.append(member_id)
        return 1 # No use since now.

    security.declarePublic("getTaskRejecters")
    def getTaskRejecters(self):
        """
        Return the list of people who rejected the task already
        """
        return self.task_rejecter

    security.declareProtected("getAssignedEmails", ModifyPortalContent)
    def getAssignedEmails(self):
        """
        Return assigned member emails.
        Used to recall them they got sthg to do.
        """

        res = []
        member_ids = self.getMemberIds()

        mtool = self.portal_metadirectories
        member_directory = mtool.members

        for member_id in member_ids:
            member = member_directory.getEntry(member_id)
            #member_email = member['email']
            res.append(member)

        return res


InitializeClass(CPSTask)

def addCPSTask(dispatcher, id, REQUEST=None, **kw):
    """Add CPS Task."""
    ob = CPSTask(id, **kw)
    return BaseDocument_adder(dispatcher, id, ob, REQUEST=REQUEST)
