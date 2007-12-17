# (C) 2003-2007 Nuxeo SAS <http://nuxeo.com>
# (C) 2003 CEA <http://www.cea.fr>
# Authors:
# Julien Anguenot <mailto:ja@nuxeo.com>
# M.-A. Darche <madarche@nuxeo.com>
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

"""CPSTaskTracker

You can access the software requirements specifications within
the docs sub-directory of the product.
"""


##############################################
# PATCHING THE OFS.
##############################################

# I have to give the member the "Delete objects"
# permissions for them being able to delete their own tasks.
# But I don't want them to that for someone else's task.

from cgi import escape

from OFS.ObjectManager import ObjectManager
from AccessControl import ClassSecurityInfo
from Globals import MessageDialog
from logging import getLogger
from zope.app.container.interfaces import IObjectAddedEvent

from Products.CMFCore.permissions import AddPortalContent
from Products.CMFCore.utils import getToolByName

from Products.CPSTaskTracker.tasktool import TASK_TOOL_ID

LOG_KEY = 'CPSTaskTracker'

security = ClassSecurityInfo()

security.declareProtected("View", "manage_delObjects")
def manage_delObjects(self, ids=[], REQUEST=None):
        """
        Delete a subordinate object
        The objects specified in 'ids' get deleted.
        """

        #
        # Testing if we are in the tasks
        # And then if it's the owner of the task
        # trying to delete.
        #

        new_ids = []
        if self.id == "tasks":
            member = self.portal_membership.getAuthenticatedMember()
            roles_in_context = member.getRolesInContext(self)
            for id in ids:
                ob = self._getOb(id, self)
                if member.getMemberId() == ob.Creator() or \
                       "Manager" in roles_in_context:
                    new_ids.append(id)
                # Commit
                ids = new_ids
        if type(ids) is type(''): ids=[ids]
        if not ids:
            return MessageDialog(title='No items specified',
                   message='No items were specified!',
                   action ='./manage_main',)
        try:    p=self._reserved_names
        except: p=()
        for n in ids:
            if n in p:
                return MessageDialog(title='Not Deletable',
                       message='<EM>%s</EM> cannot be deleted.' % escape(n),
                       action ='./manage_main',)
        while ids:
            id=ids[-1]
            v=self._getOb(id, self)
            if v is self:
                raise 'BadRequest', '%s does not exist' % escape(ids[-1])
            self._delObject(id)
            del ids[-1]
        if REQUEST is not None:
            return self.manage_main(self, REQUEST, update_menu=1)


ObjectManager.manage_delObjects = manage_delObjects

########################################################
# END OF PATCHING THE OFS
########################################################


from Products.CMFCore.utils import ToolInit, ContentInit
from Products.CMFCore.DirectoryView import registerDirectory
from Products.CMFCore.permissions import AddPortalContent

from Products.GenericSetup import profile_registry
from Products.GenericSetup import EXTENSION

from Products.CPSCore.interfaces import ICPSSite

import tasktool
import CPSTaskScreen
import CPSTask

contentClasses = (
    CPSTask.CPSTask,
    CPSTaskScreen.CPSTaskScreen,
    )

contentConstructors = (
    CPSTask.addCPSTask,
    CPSTaskScreen.addCPSTaskScreen,
    )

#
# No factory type for CPSTask since it's
# a sub class of CPSDocument
#
fti = (CPSTaskScreen.factory_type_information)

registerDirectory('skins', globals())
registerDirectory('www', globals())

tools = (tasktool.CPSTaskTool,
         )

def initialize(context):
    """
    Registering the content of the module
    """
    #
    # Task tool & repository for the tasks
    #
    ToolInit(
        'CPS Task Repository',
        tools=tools,
        icon='tool.png',
        ).initialize(context)

    #
    # Registering content classes
    #
    ContentInit(
        'CPS Task Tracker',
        content_types=contentClasses,
        permission=AddPortalContent,
        extra_constructors=contentConstructors,
        fti=fti,
        ).initialize(context)


    profile_registry.registerProfile(
        'default',
        'CPS Task Tracker',
        "Task Tracker product for CPS.",
        'profiles/default',
        'CPSTaskTracker',
        EXTENSION,
        for_=ICPSSite)


def handleObjectEvent(obj, event):
    """To set the right permissions on the tasktool after it has been created.
    """
    log_key = LOG_KEY + '.handleObjectEvent'
    logger = getLogger(log_key)
    if not IObjectAddedEvent.providedBy(event):
        return
    if event.newName is None:
        return
    if not event.newName == TASK_TOOL_ID:
        return
    utool = getToolByName(obj, 'portal_url')
    if not utool.getRpath(obj) == TASK_TOOL_ID:
        return
    obj.manage_permission(AddPortalContent,
                          ['Manager', 'Member'],
                          acquire=True)



