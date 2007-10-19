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

"""CPS Task Type.

You can access the software requierement specifications within
the docs sub-directory of the product.
Notice that this content type is following a given workflow defined in
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

from Products.CPSCore.CPSBase import CPSBase_adder
from Products.CPSDocument.CPSDocument import CPSDocument

class CPSTask(CPSDocument):
    """CPS Task Type.
    """

    meta_type   = 'CPS Task'
    portal_type = meta_type

    security = ClassSecurityInfo()

    _properties = CPSDocument._properties

    def __init__(self, id, **kw):
        """CPSTask constructor

        Call the CPSDocument constructor
        and then setup some attributes.
        """
        
        self.the_assigned = None   # the one who accepted it.
        self.is_closed = 0         # flag to see if the task has been closed.
        self.task_rejecter = []    # People who rejected the task
    
        CPSDocument.__init__(self, id, **kw)

    security.declarePublic('getMemberIds')
    def getMemberIds(self):
        """Return the member ids only
        """
        return self.members

    security.declarePrivate('getCurrentMemberId')
    def getCurrentMemberId(self):
        """Return the current logged in member
        """
        portal = self.portal_url.getPortalObject()
        member = portal.portal_membership.getAuthenticatedMember()

        return member.getMemberId()

    security.declarePublic('getGroupIds')
    def getGroupIds(self):
        """Return the group ids only
        """
        return self.groups

    security.declarePublic('isManager')
    def isManager(self):
        """Has the current member the Manager rights.
        """
        member = self.portal_membership.getAuthenticatedMember()
        roles_in_context = member.getRolesInContext(self)
        return "Manager" in roles_in_context

    security.declarePublic('isAssigned')
    def isAssigned(self):
        """Check if member_id is assigned to this task
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
        if member_id in [x['id'] for x in self.task_rejecter]:
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
            LOG("GROUP ID", DEBUG, group_id)
            if group_id != '':
                try:
                    group = portal.acl_users.getGroupById(group_id)
                    LOG("USERS", DEBUG, group.getUsers())
                    if member_id in group.getUsers():
                        return 1
                except AttributeError:
                    pass

        return 0

    security.declarePublic('getUserGroupsAssigned')
    def getUserGroupsAssigned(self):
        """Return the users from the assigned groups
        """
        portal = self.portal_url.getPortalObject()
        users = []
        if self.getGroupIds() == []:
            return []
        for group_id in self.getGroupIds():
            if group_id != '':
                try:
                    group = portal.acl_users.getGroupById(group_id)
                    for user in group.getUsers():
                        users.append(user)
                except AttributeError:
                    pass
        return users

    security.declarePublic('isCreator')
    def isCreator(self):
        """Check if member_id is the creator of the task
        """
        member_id = self.getCurrentMemberId()
        return member_id == self.Creator()

    security.declarePublic('acceptTask')
    def acceptTask(self):
        """Someone is accepting the task from the people who were
        assigned to it.
        """

        #
        # Changing the task state
        #

        portal = self.portal_url.getPortalObject()
        wftool = portal.portal_workflow
        wftool.doActionFor(self, 'accept', wf_id="task_wf")

        member_id = self.getCurrentMemberId()
        self.the_assigned = member_id

    security.declarePublic('getTheAssignedOne')
    def getTheAssignedOne(self):
        """Return the person who accepted the task
        """
        return self.the_assigned

    security.declarePublic('isTheAssignedOne')
    def isTheAssignedOne(self):
        """Check if the user the one who accepted the task
        """
        member_id = self.getCurrentMemberId()
        return member_id == self.the_assigned

    security.declarePublic('closeTask')
    def closeTask(self):
        """Close the task.
        """

        #
        # Changing the task state
        #

        portal = self.portal_url.getPortalObject()
        wftool = portal.portal_workflow
        wftool.doActionFor(self, 'close', wf_id="task_wf")

        if self.isTheAssignedOne():
            self.is_closed = 1
            self.the_assigned = None

    security.declarePublic('isClosed')
    def isClosed(self):
        """Is the task closed
        """
        return self.is_closed

    security.declarePublic('isLate')
    def isLate(self):
        """Is the task late according to the deadline.
        """
        today = DateTime()
        return ((not self.isClosed()) and (self.stop_task_date < today))

    security.declareProtected(View, 'getStatus')
    def getStatus(self):
        """Return the status of the task.
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

    security.declarePublic('')
    def reinitTask(self):
        """Reinit the task
        """

        self._p_changed = 1

        #
        # Changing WF state
        #

        portal = self.portal_url.getPortalObject()
        wftool = portal.portal_workflow
        wftool.doActionFor(self, 'reinit', wf_id="task_wf")

        #
        # Re-init attrs
        #

        self.members = []
        self.groups  = []

        self.is_closed = 0

        self.the_assigned = None
        self.task_rejecter = []

    security.declarePublic('rejectTask')
    def rejectTask(self):
        """The user rejects the task
        """

        portal = self.portal_url.getPortalObject()
        wftool = portal.portal_workflow
        wftool.doActionFor(self, 'reject', wf_id="task_wf")

        now = DateTime().strftime("%Y/%m/%d")
        member_id = self.getCurrentMemberId()
        struct = {'id':member_id, 'date':now}
        self.task_rejecter.append(struct)
        return 1 # No use since now.

    security.declarePublic('getTaskRejecters')
    def getTaskRejecters(self):
        """Return the list of people who rejected the task already
        """
        return [x['id'] for x in self.task_rejecter]

    security.declareProtected(ModifyPortalContent, 'getAllAssignedMembers')
    def getAllAssignedMembers(self):
        """Return assigned members.

        Used to recall them they got sthg to do.
        """

        res = []

        mtool = self.portal_directories
        portal = self.portal_url.getPortalObject()

        #
        # First the single members
        #

        member_ids = self.getMemberIds()


        for member_id in member_ids:
            try:
                member = mtool.members.getEntry(member_id)
                res.append(member)
            except AttributeError:
                pass

        #
        # Then the groups
        #

        for group_id in self.getGroupIds():
            if group_id != '':
                try:
                    group = portal.acl_users.getGroupById(group_id)
                    for member_id in group.getUsers():
                        try:
                            member = mtool.members.getEntry(member_id)
                            res.append(member)
                        except AttributeError:
                            pass
                except AttributeError:
                    pass

        return res

    security.declareProtected(ModifyPortalContent, 'sendMailTo')
    def sendMailTo(self, content="", emails=[], from_address="", subject=""):
        """Send a mail
        """

        if hasattr(self, 'MailHost'):
            mailhost = self.MailHost
            try:
                mailhost.send(content,
                              mto=emails,
                              mfrom=from_address,
                              subject=subject,
                              encode='8bit')
                return 1
            except:
                # Problème while sending mail
                pass
        return 0

InitializeClass(CPSTask)

def addCPSTask(container, id, REQUEST=None, **kw):
    """Add CPS Task.
    """
    ob = CPSTask(id, **kw)
    return CPSBase_adder(container, ob, REQUEST=REQUEST)
