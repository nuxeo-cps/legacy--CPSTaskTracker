# (c) 2003,2004 Nuxeo SARL <http://nuxeo.com>
# (c) 2003 CEA <http://www.cea.fr>
# Author: Julien Anguenot <mailto:ja@nuxeo.com>
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

CPSTaskTracker is a task tracker intended to be used with CPS
version 2 and version 3.

You can access the software requierements specifications within
the docs sub-directory of the product.
"""

#
# Checking what's the version of CPS3 in here.
# This flag will be in use to import the
# corresponding classes according to the version of CPS.
#

try:
        import Products.CPSCore
        CPS_VERSION = 3
except ImportError:
        try:
                import Products.NuxCPS
                CPS_VERSION = 2
        except ImportError:
                raise "Unknown version of CPS"

# For debug purposes (CPS2)
from AccessControl import ModuleSecurityInfo
ModuleSecurityInfo('zLOG').declarePublic('LOG', 'DEBUG')

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

security = ClassSecurityInfo()

security.declareProtected("View", "manage_delObjects")
def manage_delObjects(self, ids=[], REQUEST=None):
        """
        Delete a subordinate object
        The objects specified in 'ids' get deleted.
        """

        #
        # Testing if we are in the portal_tasks
        # And then if it's the owner of the task
        # trying to delete.
        #

        new_ids = []
        if self.id == "portal_tasks":
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


import sys

from Products.CMFCore.utils import ToolInit, ContentInit
from Products.CMFCore.DirectoryView import registerDirectory
from Products.CMFCore.CMFCorePermissions import AddPortalContent

if CPS_VERSION == 2:
        import CPSTaskTool
        import CPSTaskScreen
        import CPSTask
        import CPSTaskBox
else:
        import CPS3TaskTool as CPSTaskTool
        import CPS3TaskScreen as CPSTaskScreen
        import CPS3Task as CPSTask
        import CPS3TaskBox as CPSTaskBox

contentClasses = (
    CPSTask.CPSTask,
    CPSTaskScreen.CPSTaskScreen,
    CPSTaskBox.CPSTaskBox,
    )

contentConstructors = (
    CPSTask.addCPSTask,
    CPSTaskScreen.addCPSTaskScreen,
    CPSTaskBox.addCPSTaskBox,
    )

if CPS_VERSION == 2:
        fti = (
                CPSTask.factory_type_information +
                CPSTaskScreen.factory_type_information +
                CPSTaskBox.factory_type_information + ()
                )
if CPS_VERSION == 3:
        #
        # No factory type for CPSTask since it's
        # a sub class of CPSDocument
        #
        fti = (
                () +
                CPSTaskScreen.factory_type_information +
                CPSTaskBox.factory_type_information + ()
                )

registerDirectory('skins', globals())
registerDirectory('www', globals())

tools = ( CPSTaskTool.CPSTaskTool,
          )

def initialize(context):
    """
    Registering the content of the module
    """
    #
    # Task tool & repository for the tasks
    #
    ToolInit(
        'CPS Task Tool',
        tools = tools,
        product_name = 'CPSTaskTracker',
        icon = 'todo.png',
        ).initialize(context)

    #
    # Registering content classes :
    # Task, the Task Screen and the task box.
    #
    ContentInit(
        'CPS Task Tracker',
        content_types = contentClasses,
        permission = AddPortalContent,
        extra_constructors = contentConstructors,
        fti = fti,
        ).initialize(context)
