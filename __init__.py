# (c) 2003 Nuxeo SARL <http://nuxeo.com>
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

import sys

from Products.CMFCore.utils import ToolInit, ContentInit
from Products.CMFCore.DirectoryView import registerDirectory
from Products.CMFCore.CMFCorePermissions import AddPortalContent

import CPSTaskTool
import CPSTask
import CPSTaskScreen

contentClasses = (
    CPSTask.CPSTask,
    CPSTaskScreen.CPSTaskScreen,
    )

contentConstructors = (
    CPSTask.addCPSTask,
    CPSTaskScreen.addCPSTaskScreen,
    )

fti = (
    CPSTask.factory_type_information +
    CPSTaskScreen.factory_type_information +
    ()
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
        icon = 'tool.png',
        ).initialize(context)

    #
    # Registering content : Task and the Task Screen
    #
    ContentInit(
        'CPS Task Tracker',
        content_types = contentClasses,
        permission = AddPortalContent,
        extra_constructors = contentConstructors,
        fti = fti,
        ).initialize(context)
