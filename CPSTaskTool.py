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
CPS Task Tool
This tool will :
  - act as a repository for all the tasks.
  - define a search API used by the CPSTaskScreen and CPSTaskBox types.
  - store some lists like project list here.
"""

from zLOG import LOG, DEBUG

from Globals import InitializeClass
from AccessControl import ClassSecurityInfo

from Products.BTreeFolder2.CMFBTreeFolder import CMFBTreeFolder

from Products.CMFCore.PortalFolder import PortalFolder
from Products.CMFCore.utils import UniqueObject
from Products.CMFCore.CMFCorePermissions import View, ModifyPortalContent

class CPSTaskTool(UniqueObject, CMFBTreeFolder):
    """
    Provides a Task Repository
    """

    id = 'portal_tasks'
    meta_type = 'CPS Task Tool'

    security = ClassSecurityInfo()

    manage_options = CMFBTreeFolder.manage_options

    def __init__(self):
        """
        CMFBTreeFolder constructor
        """
        CMFBTreeFolder.__init__(self, self.id)
        self.lprojects = [] # We will keep the different projects here.


    #################################################
    # SORT API
    #################################################

    security.declarePrivate("_sortTaskObjects")
    def _sortTaskObjects(self, task_list=[], parameters={},
                         func=(lambda x,y:x <= y)):
        """
        Given a list of task objects we gonna sort it
        against the paramters.
        """

        def _doSort(self, func, task_list):
            """
            Realize the sort of task_list given a lambda function.
            """
            res = []
            j = 0
            for j in range(len(task_list)):
                i = 0
                for y in res:
                   if func(self, task_list[j], y):
                       break
                   i = i + 1
                res = res[:i] + task_list[j:j+1] + res[i:]
            return  res

        stupid_flag = 0

        #
        # Cheking in which case we are and then building the
        # lambda function.
        #

        if parameters['sort_date_on'] == 'start_date' and \
               parameters['sort_order']   == 'asc':
            func = (lambda self, x,y: x.start_task_date <= y.start_task_date)

        elif parameters['sort_date_on'] == 'start_date' and \
                 parameters['sort_order']   == 'desc':
            func = (lambda self, x,y: x.start_task_date > y.start_task_date)

        elif parameters['sort_date_on'] == 'stop_date' and \
                 parameters['sort_order']   == 'asc':
            func = (lambda self, x,y: x.stop_task_date <= y.stop_task_date)

        elif parameters['sort_date_on'] == 'stop_date' and \
                 parameters['sort_order']   == 'desc':
            func = (lambda self, x,y: x.stop_task_date > y.stop_task_date)

        else:
            # No way to sort anything in this condition ;)
            stupid_flag = 1

        if not stupid_flag:
            res = _doSort(self, func, task_list)
        else:
            # Nothing done in here. We got a weired case.
            return task_list

        #
        # Now sorting on something
        # type, priority or project.-> cf. num values
        # Same business -> building the lambda function.
        #

        task_list = res

        self.map_priority = {'high': 1, 'normal':2, 'low':3}

        stupid_flag = 0

        if parameters['sort_on'] == 'priority':
            func = (lambda self, x,y:
                    self.map_priority[x.task_priority]\
                    <= self.map_priority[y.task_priority])
        elif parameters['sort_on'] == 'project':
            # Alpha
            func = (lambda self, x,y:
                    x.task_project[0].lower\
                    <= y.task_project.lower[0])
        elif parameters['sort_on'] == 'type':
            # Case on the type -> Alpha sorting.
            func = (lambda self, x,y: x.task_type[0].lower()\
                    <= y.task_type[0].lower())
        elif parameters['sort_on'] == 'project':
            # Case on the project -> Alpha sorting.
            func = (lambda self, x,y: x.task_project[0].lower()\
                    <= y.task_project[0].lower())
        else:
            # No way to sort anything in this condition ;
            stupid_flag = 1

        if not stupid_flag:
            res = _doSort(self, func, task_list)
        else:
            # Nothing done in here. We got a weired case.
            return res

        # That's it now !
        return res

    security.declarePrivate("_getTaskList")
    def _getTaskLists(self, sorted_tasks, parameters):
        """
        Sorted_tasks is the list of tasks
        sorted according to the parameters.
        Now, we gonna split that in different categories
        according to the given parameters.
        """

        portal_membership = self.portal_membership
        if portal_membership.isAnonymousUser():
            return 0
        member = portal_membership.getAuthenticatedMember()
        member_id = member.getMemberId()

        task_lists = {}

        if parameters.get('display_my_tasks'):
            task_lists['my_tasks'] = [x for x in sorted_tasks \
                                      if x.isCreator()]
        if parameters.get('display_my_affected_tasks'):
            task_lists['my_affected_tasks'] = [x for x in sorted_tasks \
                                               if member_id in \
                                               x.getMemberIds()]
        if parameters.get('display_my_groups_affected_tasks'):
            task_lists['my_groups_affected_tasks'] = [x for x in \
                                                      sorted_tasks if \
                                                      x.isAssigned()]
        if parameters.get('display_my_accepted_tasks'):
            task_lists['my_accepted_tasks'] = [x for x \
                                               in sorted_tasks \
                                               if \
                                               x.isTheAssignedOne()]
        return task_lists


    security.declareProtected(View, "searchTasks")
    def searchTasks(self, parameters={}):
        """
        Searching the tasks within the portal.
        Main function used by CPSTaskScreen and CPSTaskBox.
        """
        pcat = self.portal_catalog
        tasks = pcat.searchResults({'portal_type':'CPS Task'})
        tasks = [x.getObject() for x in tasks]
        #
        # Sorting the tasks against the parameters
        #
        sorted_tasks = self._sortTaskObjects(tasks, parameters)
        #
        # Spliting to different lists depending on the choice
        # the user did.
        #
        task_lists = self._getTaskLists(sorted_tasks, parameters)
        return task_lists

    ################################################
    # PROJECT API
    ################################################

    security.declarePrivate("_hasIndex")
    def _hasIndex(self, project_title):
        """
        Returnt the index of the project in the list
        """
        i = 0
        for project in self.lprojects:
            if project_title == project['title']:
                return i
            i+=1

        return None

    security.declareProtected(View, "getProjects")
    def getProjects(self):
        """
        Returns the list of projects already stored.
        """
        return self.lprojects

    security.declareProtected(ModifyPortalContent, "addProject")
    def addProject(self, new_project={}):
        """
        Adds a brandly new project.
        """
        stupid_flag = 0
        if new_project != {} and \
           type(new_project) == type({}):
            i = 0
            for project in self.lprojects:
                if project['title'] == new_project['title']:
                    stupid_flag = 1
                    self.lprojects[i]['description'] = new_project['description']
                i += 1
            if not stupid_flag:
                self.lprojects.append(new_project)
            return 1
        return 0

    security.declareProtected(ModifyPortalContent, "delProject")
    def delProjects(self, titles=[]):
        """
        Removes projects given titles
        """
        for title in titles:
            index = self._hasIndex(title)
            if index is not None:
                del self.lprojects[index]
        return 1

InitializeClass(CPSTaskTool)
