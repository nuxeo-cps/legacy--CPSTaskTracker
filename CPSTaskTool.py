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

"""
CPS Task Tool
This tool will :
  - acts as a repository for all the tasks
  - Search API used by the CPSTaskScreen and CPSTaskBox types.
"""

from Globals import InitializeClass
from AccessControl import ClassSecurityInfo

from Products.BTreeFolder2.CMFBTreeFolder import CMFBTreeFolder

from Products.CMFCore.PortalFolder import PortalFolder
from Products.CMFCore.utils import UniqueObject

class CPSTaskTool(UniqueObject, CMFBTreeFolder):
    """
    Provides Task Repository
    """

    id = 'portal_tasks'
    meta_type = 'CPS Task Tool'

    security = ClassSecurityInfo()

    manage_options = CMFBTreeFolder.manage_options

    def __init__(self):
         CMFBTreeFolder.__init__(self, self.id)

    security.declareProtected("View", "searchTasks")
    def searchTasks(self, **kw):
        """
        Searching the tasks within the portal.
        """
        #
        # XXX : TO FINISH !
        #
        pcat = self.portal_catalog
        tasks = pcat.searchResults({'portal_type':'CPS Task'})
        tasks = [x.getObject() for x in tasks]
        return tasks

InitializeClass(CPSTaskTool)
