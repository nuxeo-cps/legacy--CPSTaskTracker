# (c) 2003-2007 Nuxeo SAS <http://nuxeo.com>
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

"""CPS Task Repository

This tool :

- Acts as a repository for all the tasks created in the whole portal
- Defines a task search API used by CPSTaskScreen and CPSTaskBox types
- Stores project records
"""

from pprint import pformat
from logging import getLogger
from operator import itemgetter

from zope.interface import implements
from Globals import InitializeClass
from AccessControl import ClassSecurityInfo
from persistent.dict import PersistentDict

from Products.BTreeFolder2.CMFBTreeFolder import CMFBTreeFolder
from Products.CMFCore.utils import getToolByName
from Products.CMFCore.PortalFolder import PortalFolder
from Products.CMFCore.utils import UniqueObject
from Products.CMFCore.CMFCorePermissions import View, ModifyPortalContent

from Products.CPSTaskTracker.CPSTaskTrackerPermissions import ManageProjects, \
     TaskCreate
from Products.CPSTaskTracker.interfaces import ITaskTool

LOG_KEY = 'CPSTaskTool'

_marker = object()

class CPSTaskTool(UniqueObject, CMFBTreeFolder, PortalFolder):
    """CPS Task Repository

    Provides a Task Repository for the whole portal
    """

    implements(ITaskTool)

    id = 'tasks'
    meta_type = 'CPS Task Repository'

    security = ClassSecurityInfo()

    manage_options = CMFBTreeFolder.manage_options

    def __init__(self, id=_marker):
        """CMFBTreeFolder constructor
        """
        if id is not _marker:
            self.id = id
        CMFBTreeFolder.__init__(self, self.id)

        # We will keep the different projects here.
        # We have to use a PersistentDict since the python built-in list
        # and dict don't notify the ZODB when they have been changed.
        self._projects = PersistentDict()

    #################################################
    #################################################

    security.declareProtected(View, 'searchTasks')
    def searchTasks(self, parameters={}):
        """Return all the tasks present in the task repository.

        parameters is to specify the choice of sorting.

        Main function used by CPSTaskScreen and CPSTaskBox.
        """
        pcat = self.portal_catalog
        tasks = pcat.searchResults({'portal_type':'CPS Task'})
        tasks = [x.getObject() for x in tasks]

        # Sorting the tasks against the parameters
        sorted_tasks = self._sortTaskObjects(tasks, parameters)

        # Spliting to different lists depending on the choice
        # the user did.
        task_lists = self._getTaskLists(sorted_tasks, parameters)

        return task_lists

    security.declarePrivate('_sortTaskObjects')
    def _sortTaskObjects(self, task_list=[], parameters={},
                         func=(lambda x,y:x <= y)):
        """Given a list of task objects we gonna sort it
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

        # Cheking in which case we are and then building the
        # lambda function.
        if parameters['sort_date_on'] == 'start_date' and \
               parameters['sort_order']   == 'asc':
            func = (lambda self, x,y: x.getContent().start_task_date \
            <= y.getContent().start_task_date)

        elif parameters['sort_date_on'] == 'start_date' and \
                 parameters['sort_order']   == 'desc':
            func = (lambda self, x,y: x.getContent().start_task_date > \
            y.getContent().start_task_date)

        elif parameters['sort_date_on'] == 'stop_date' and \
                 parameters['sort_order']   == 'asc':
            func = (lambda self, x,y: x.getContent().stop_task_date <= \
            y.getContent().stop_task_date)

        elif parameters['sort_date_on'] == 'stop_date' and \
                 parameters['sort_order']   == 'desc':
            func = (lambda self, x,y: x.getContent().stop_task_date > \
            y.getContent().stop_task_date)

        else:
            # No way to sort anything in this condition ;)
            stupid_flag = 1

        if not stupid_flag:
            res = _doSort(self, func, task_list)
        else:
            # Nothing done in here. We got a weired case.
            return task_list

        # Now sorting on something
        # type, priority or project.-> cf. num values
        # Same business -> building the lambda function.
        task_list = res

        self.map_priority = {'high': 1, 'normal': 2, 'low': 3}

        stupid_flag = 0

        if parameters['sort_on'] == 'priority':
            func = (lambda self, x,y:
                    self.map_priority[x.getContent().task_priority]\
                    <= self.map_priority[y.getContent().task_priority])

        elif parameters['sort_on'] == 'type':
            # Case on the type -> Alpha sorting.
            func = (lambda self, x,y: x.getContent().task_type[0].lower()\
                    <= y.getContent().task_type[0].lower())

        elif parameters['sort_on'] == 'project':
            # Case on the project -> Alpha sorting.
            func = (lambda self, x,y: x.getContent().task_project[0].lower()\
                    <= y.getContent().task_project[0].lower())

        else:
            # No way to sort anything in this condition ;
            stupid_flag = 1

        if not stupid_flag:
            res = _doSort(self, func, task_list)
        else:
            # Nothing done in here. We got a weired case.
            return res

        return res

    security.declarePrivate("_getTaskList")
    def _getTaskLists(self, sorted_tasks, parameters):
        """Return the list of tasks split in different categories

        Sorted_tasks is the list of tasks sorted according to the parameters.
        Now, we gonna split that in different categories according to the given
        parameters.
        """

        portal_membership = self.portal_membership
        if portal_membership.isAnonymousUser():
            return 0
        member = portal_membership.getAuthenticatedMember()
        member_id = member.getMemberId()

        task_lists = {}

        # Filtering for the different categories
        if parameters.get('display_my_tasks'):
            task_lists['my_tasks'] = [
                x for x in sorted_tasks if x.getContent().isCreator()]

        if parameters.get('display_my_affected_tasks'):
            task_lists['my_affected_tasks'] = [
                x for x in sorted_tasks if x.getContent().isAssigned()]

        if parameters.get('display_my_groups_affected_tasks'):
            task_lists['my_groups_affected_tasks'] = [
                x for x in sorted_tasks if member_id in x.getContent().getUserGroupsAssigned()]

        if parameters.get('display_my_accepted_tasks'):
            task_lists['my_accepted_tasks'] = [
                x for x in sorted_tasks if x.getContent().isTheAssignedOne()]

        # Cleaning the empty entries
        # For the visible if empty feature
        if task_lists.get('my_tasks') == []:
            del task_lists['my_tasks']
        if task_lists.get('my_affected_tasks') == []:
            del task_lists['my_affected_tasks']
        if task_lists.get('my_accepted_tasks') == []:
            del task_lists['my_accepted_tasks']
        if task_lists.get('my_groups_affected_tasks') == []:
            del task_lists['my_groups_affected_tasks']
        if task_lists.get('display_on_project') == []:
            del task_lists['display_on_project']

        return task_lists


    ################################################
    ################################################

    security.declareProtected(View, 'getProjects')
    def getProjects(self):
        """Returns all the projects as a list of items (id, definition).
        """
        return self._projects.items()

    security.declareProtected(View, 'getProjectDef')
    def getProjectDef(self, project_id):
        """Return the definition, ie a dictionary, of the project.
        """
        log_key = LOG_KEY + '.getProjectDef'
        logger = getLogger(log_key)
        logger.debug("project_id = %s" % project_id)
        return self._projects[project_id]

    security.declareProtected(View, 'getProjectsWithTasks')
    def getProjectsWithTasks(self):
        """Returns the list of projects with their associated tasks.

        The result is a dictionary with keys being project names and values
        being a dictionary containing information the project title and the
        task descriptions.
        """
        log_key = LOG_KEY + '.getProjectsWithTasks'
        logger = getLogger(log_key)
        # The result we want to return
        res = {}
        pcat = self.portal_catalog
        tasks = pcat.searchResults({'portal_type':'CPS Task'})
        tasks = [x.getObject() for x in tasks]

        for task in tasks:
            task_doc = task.getContent()
            task_def = {}
            task_def['id'] = task_doc.id
            task_def['title'] = task_doc.title
            task_def['status'] = task_doc.getStatus()
            task_def['start_date'] = task_doc.start_task_date
            task_def['stop_date'] = task_doc.stop_task_date
            task_def['members'] = task_doc.members
            task_def['groups'] = task_doc.groups
            task_def['dependency'] = task_doc.dependency

            # This is the ID of the project
            project_id = task_doc.task_project
            if project_id not in res.keys():
                project_title = self.getProjectDef(project_id)['title']
                res[project_id] = {'project_title': project_title}
                res[project_id]['tasks'] = []
                res[project_id]['dependencies'] = set()

            res[project_id]['tasks'].append(task_def)
            if task_doc.dependency:
                res[project_id]['dependencies'].add(task_doc.dependency)

        for project_id in res.keys():
            tasks_defs = res[project_id]['tasks']
            tasks_defs_new = []
            dependencies = res[project_id]['dependencies']
            #logger.debug("dependencies = %s" % str(dependencies))

            # Sorting the top tasks using the decorate-sort-undecorate pattern
            top_tasks_and_dependencies = []
            for dependency in dependencies:
                 top_task = [x for x in tasks_defs if x['id'] == dependency][0]
                 top_tasks_and_dependencies.append((top_task['start_date'],
                                                    top_task, dependency))

            # Tasks with no dependencies and not_dependent to other tasks
            tasks_defs_no_dependencies = [(x['start_date'], x, None)
                                          for x in tasks_defs
                                          if x['id'] not in dependencies
                                          and not x['dependency']]
            top_tasks_and_dependencies += tasks_defs_no_dependencies
            #logger.debug("top_tasks_and_dependencies = \n%s"
            #             % pformat(top_tasks_and_dependencies))

            top_tasks_and_dependencies.sort(key=itemgetter(0))
            #logger.debug("top_tasks_and_dependencies = \n%s"
            #             % pformat(top_tasks_and_dependencies))

            for top_task_and_dependency in top_tasks_and_dependencies:
                top_task = top_task_and_dependency[1]
                dependency = top_task_and_dependency[2]
                tasks_defs_new.append(top_task)

                if dependency is None:
                    continue

                tasks_defs_with_dependencies = [x for x in tasks_defs
                                                if x['dependency'] == dependency]
                # Sorting the tasks with dependency
                # using the decorate-sort-undecorate pattern.
                decorated = [(x['start_date'], x) for x in tasks_defs_with_dependencies]
                decorated.sort(key=itemgetter(0))
                tasks_defs_with_dependencies = [x[1] for x in decorated]
                tasks_defs_new += tasks_defs_with_dependencies

            #logger.debug(pformat(tasks_defs_new))
            res[project_id]['tasks'] = tasks_defs_new

        #logger.debug(pformat(res))
        return res

    security.declareProtected(View, 'getProjectTasks')
    def getProjectTasks(self, project_id):
        """Returns the list of tasks for a given project.

        The result is a list with itels being tasks information.
        """
        tasks_with_dates = []
        pcat = self.portal_catalog
        tasks = pcat.searchResults({'portal_type':'CPS Task'})
        tasks = [x.getObject() for x in tasks]

        for task in tasks:
            task_doc = task.getContent()
            if task_doc.task_project != project_id:
                continue
            task_def = {}
            task_def['id'] = task_doc.id
            task_def['title'] = task_doc.title
            task_def['status'] = task_doc.getStatus()
            task_def['start_date'] = task_doc.start_task_date
            task_def['stop_date'] = task_doc.stop_task_date
            task_def['members'] = task_doc.members
            task_def['groups'] = task_doc.groups
            # Using the decorate-sort-undecorate pattern
            tasks_with_dates.append((task_doc.start_task_date, task_def))
        tasks_with_dates.sort(key=itemgetter(0))
        task_defs = [x[1] for x in tasks_with_dates]
        return task_defs

    security.declareProtected(ManageProjects, 'addProject')
    def addProject(self, new_project):
        """Adds a brandly new project.
        """
        log_key = LOG_KEY + '.addProject'
        logger = getLogger(log_key)
        if not isinstance(new_project, dict) or new_project == {}:
            raise ValueError("Wrong project definition given")

        project_id = new_project['id']
        logger.debug("project_id = %s" % project_id)
        if self._projects.has_key(project_id):
            raise ValueError("A project already exist with the ID: %s"
                             % project_id)

        self._projects[project_id] = new_project
        logger.debug("project = %s" % self._projects[project_id])
        # At this point we don't need the project id anymore in the dictionary
        del self._projects[project_id]['id']
        logger.debug("project = %s" % self._projects[project_id])

    security.declareProtected(ManageProjects, 'editProject')
    def editProject(self, project_def):
        """Modify an existing project

        project_def should be a dictionary with id, title and description.
        """
        if not isinstance(project_def, dict) or project_def == {}:
            raise ValueError("Wrong project definition given")

        project_id = project_def['id']
        if not self._projects.has_key(project_id):
            raise ValueError("No project exists with the ID: %s" % project_id)

        # At this point we don't need the project id anymore in the dictionary
        del project_def['id']
        self._projects[project_id] = project_def

    security.declareProtected(ManageProjects, 'delProjects')
    def delProjects(self, project_ids=[]):
        """Removes projects with the given IDs.
        """
        for project_id in project_ids:
            del self._projects[project_id]

InitializeClass(CPSTaskTool)
