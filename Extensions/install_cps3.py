# Copyright (c) 2004 Nuxeo SARL <http://nuxeo.com>
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


from zLOG import LOG, INFO, DEBUG

import os, sys

from Products.PythonScripts.PythonScript import PythonScript

from Products.CMFCore.utils import getToolByName
from Products.CMFCore.CMFCorePermissions import ModifyPortalContent, View

from Products.CPSInstaller.CPSInstaller import CPSInstaller

from Products.CPSCore.CPSWorkflow import \
     TRANSITION_INITIAL_PUBLISHING, TRANSITION_INITIAL_CREATE, \
     TRANSITION_ALLOWSUB_CREATE, TRANSITION_ALLOWSUB_PUBLISHING, \
     TRANSITION_BEHAVIOR_PUBLISHING, TRANSITION_BEHAVIOR_FREEZE, \
     TRANSITION_BEHAVIOR_DELETE, TRANSITION_BEHAVIOR_MERGE, \
     TRANSITION_ALLOWSUB_CHECKOUT, TRANSITION_INITIAL_CHECKOUT, \
     TRANSITION_BEHAVIOR_CHECKOUT, TRANSITION_ALLOW_CHECKIN, \
     TRANSITION_BEHAVIOR_CHECKIN, TRANSITION_ALLOWSUB_DELETE, \
     TRANSITION_ALLOWSUB_MOVE, TRANSITION_ALLOWSUB_COPY

SECTIONS_ID = 'sections'
WORKSPACES_ID = 'workspaces'
SKINS = {'cps_task_tracker' : 'Products/CPSTaskTracker/skins/cps3_default',
         }

from Products.CPSTaskTracker.CPSTaskTrackerPermissions import TaskCreate, \
     ManageProjects

class CPSInstaller(CPSInstaller):
    """Base Class Installer for CPSTaskTracker
    """

    product_name = 'CPSTaskTracker'

    def install(self):
        """CPSTaskTracker installer.
        """

        self.log("Starting CPSTaskTracker install")
        self.verifySkins(SKINS)
        self.resetSkinCache()
        self.setupTranslations()
        self.installSchemas()
        self.installLayouts()
        self.installVocabularies()
        self.setupTaskType()
        self.setupTaskWorkflow()
        self.setupPortalTaskTool()
        self.setupTaskScreenType()
        self.setupTaskBoxType()
        self.setupPortalActions()
        self.finalize()
        self.reindexCatalog()
        self.log("End of specific CPSTaskTracker install")

    def installSchemas(self):
        """Install Specfic Schemas
        """

        self.log("Verifiying schemas")

        schemas = self.portal.getCPSTaskTrackerSchemas()

        stool = self.portal.portal_schemas
        for id, info in schemas.items():
            self.log(" Schema %s" % id)
            if id in stool.objectIds():
                self.log("  Deleting.")
                stool.manage_delObjects([id])
            self.log("  Installing.")
            schema = stool.manage_addCPSSchema(id)
            for field_id, fieldinfo in info.items():
                self.log("   Field %s." % field_id)
                schema.manage_addField(field_id, fieldinfo['type'],
                                       **fieldinfo['data'])
    def installLayouts(self):
        """Install the spcific layouts
        """

        self.log("Verifiying layouts")

        layouts = self.portal.getCPSTaskTrackerLayouts()

        ltool = self.portal.portal_layouts
        for id, info in layouts.items():
            self.log(" Layout %s" % id)
            if id in ltool.objectIds():
                self.log("  Deleting.")
                ltool.manage_delObjects([id])
            self.log("  Installing.")
            layout = ltool.manage_addCPSLayout(id)
            for widget_id, widgetinfo in info['widgets'].items():
                self.log("   Widget %s" % widget_id)
                widget = layout.manage_addCPSWidget(widget_id, widgetinfo['type'],
                                                    **widgetinfo['data'])
                layout.setLayoutDefinition(info['layout'])
                layout.manage_changeProperties(**info['layout'])

    def installVocabularies(self):
        """Install the specific vocabularies
        """

        self.log("Verifiying vocabularies")
        vocabularies = self.portal.getCPSTaskTrackerVocabularies()

        vtool = self.portal.portal_vocabularies
        for id, info in vocabularies.items():
            self.log(" Vocabulary %s" % id)
            if id in vtool.objectIds():
                self.log("  Deleting.")
                vtool.manage_delObjects([id])
            self.log("  Installing.")
            type = info.get('type', 'CPS Vocabulary')
            vtool.manage_addCPSVocabulary(id, type, **info['data'])

    def registerTypes(self):
        ptypes_installed = self.ttool.objectIds()
        display_in_cmf_calendar = []
        for ptype, data in self.flextypes.items():
            self.log("  Type '%s'" % ptype)
            if ptype in ptypes_installed:
                self.ttool.manage_delObjects([ptype])
                self.log("   Deleted")
            ti = self.ttool.addFlexibleTypeInformation(id=ptype)
            if data.get('display_in_cmf_calendar'):
                display_in_cmf_calendar.append(ptype)
                del data['display_in_cmf_calendar']
            ti.manage_changeProperties(**data)

            if data.has_key('actions'):
                self.log("    Setting actions")
                # delete all actions
                nb_action = len(ti.listActions())
                ti.deleteActions(selections=range(nb_action))
                # and set the new ones
                for a in data['actions']:
                    ti.addAction(a['id'],
                                 a['name'],
                                 a['action'],
                                 a.get('condition', ''),
                                 a['permissions'][0],
                                 'object',
                                 visible=a.get('visible',1))
            self.log("   Installation")

        # register ptypes to portal_calendar
        if display_in_cmf_calendar and hasattr(self.portal, 'portal_calendar'):
            self.portal.portal_calendar.calendar_types = display_in_cmf_calendar

    def setupTaskWorkflow(self):
        """Install the Task Workflow
        """

        from Products.CPSTaskTracker.Workflow.CPSTaskWorkflow import \
             CPSTaskWorkflowInstall
        CPSTaskWorkflowInstall(self.context)

    def setupPortalTaskTool(self):
        """Setup the portal_tasks tool

        Creation / Permissions
        """

        # Adding the portal tasks tool
        self.log("Checking the portal_tasks tool")

        if getToolByName(self.portal, 'portal_tasks', None) is None:
            self.log("Creating portal_tasks tool")
            self.portal.manage_addProduct["CPSTaskTracker"].manage_addTool(
                'CPS Task Tool')
        else:
            self.log("portal_tasks tool already exists")

        # Updating permissions there
        self.log("Update portal_tasks permissions")
        self.portal['portal_tasks'].manage_permission('Add portal content',
                                                      ['Member'],
                                                      1)
        self.portal['portal_tasks'].manage_permission('Modify portal content',
                                                      ['Member'],
                                                      1)
        self.portal['portal_tasks'].manage_permission('Delete objects',
                                                      ['Member'],
                                                      1)
        self.portal['portal_tasks'].reindexObjectSecurity()

        # Creation of the .cps_workflow_configuration.
        tasks_tool = getToolByName(self.portal, 'portal_tasks')
        if '.cps_workflow_configuration' not in tasks_tool.objectIds():
            tasks_tool.manage_addProduct['CPSCore'].addCPSWorkflowConfiguration()

        # Adding wfc task chain
        wfc = getattr(tasks_tool, '.cps_workflow_configuration')
        wfc.manage_addChain(portal_type='CPS Task', chain='task_wf')

    def setupTaskScreenType(self):
        """Setup the CPSTaskScreen portal_type

        This one doesn't have any workflow.
        """

        ttool = getToolByName(self.portal, 'portal_types')
        ptypes_installed = ttool.objectIds()

        self.log("CPSTaskScreen portal type installation")
        newptypes = ('CPS Task Screen',)

        if 'Workspace' in ptypes_installed:
            workspaceACT = list(ttool['Workspace'].allowed_content_types)
        else:
            raise "DependanceError : Workspace portal type"

        for ptype in newptypes:
            if ptype not in  workspaceACT:
                self.log("Allowing %s in Workspaces" %ptype)
                workspaceACT.append(ptype)

        allowed_content_type = {
            'Workspace' : workspaceACT,
            }

        ttool['Workspace'].allowed_content_types = allowed_content_type['Workspace']

        ptypes = {
            'CPSTaskTracker':('CPS Task Screen',
                              )
            }

        for prod in ptypes.keys():
            for ptype in ptypes[prod]:
                if ptype in ptypes_installed:
                    ttool.manage_delObjects([ptype])
                ttool.manage_addTypeInformation(
                    id=ptype,
                    add_meta_type='Factory-based Type Information',
                    typeinfo_name=prod+': '+ptype,
                    )

    def setupTaskBoxType(self):
        """Setup the CPSTaskBox portal_type
        """

        ttool = getToolByName(self.portal, 'portal_types')
        ptypes_installed = ttool.objectIds()

        self.log("CPSTaskBox portal type installation")
        newptypes = ('CPS Task Box',)

        ptypes = {
            'CPSTaskTracker':('CPS Task Box',
                              )
            }

        for prod in ptypes.keys():
            for ptype in ptypes[prod]:
                if ptype in ptypes_installed:
                    ttool.manage_delObjects([ptype])
                ttool.manage_addTypeInformation(
                    id=ptype,
                    add_meta_type='Factory-based Type Information',
                    typeinfo_name=prod+': '+ptype,
                    )
        #
        # Workflow chains
        #

        workspaces = getattr(self.portal, WORKSPACES_ID)
        if '.cps_workflow_configuration' not in workspaces.objectIds():
            workpaces.manage_addProduct['CPSCore'].addCPSWorkflowConfiguration()

        # Adding wfc task chain
        wfc = getattr(workspaces, '.cps_workflow_configuration')
        wfc.manage_addChain(portal_type='CPS Task Screen', chain='workspace_folder_wf')

    def setupTaskType(self):
        """Setup CPS Task portal_type
        """

        self.log("Verifying CPS Task Tracker portal types")

        #
        # Registering the task
        #

        self.flextypes = self.portal.getCPSTaskTrackerTypes()
        self.newptypes = self.flextypes.keys()
        self.ttool = self.portal.portal_types
        self.registerTypes()

        #
        # Allowing in workspaces
        #

        ##ttool = getToolByName(self.portal, 'portal_types')
        ##ptypes_installed = ttool.objectIds()
        ##newptypes = ('CPS Task',)
        ##if 'Workspace' in ptypes_installed:
        ##    workspaceACT = list(ttool['Workspace'].allowed_content_types)
        ##else:
        ##    raise "DependanceError : Workspace portal type"
        ##
        ##for ptype in newptypes:
        ##    if ptype not in  workspaceACT:
        ##        self.log("Allowing %s in Workspaces" %ptype)
        ##        workspaceACT.append(ptype)
        ##
        ##allowed_content_type = {
        ##    'Workspace' : workspaceACT,
        ##    }
        ##
        ##ttool['Workspace'].allowed_content_types = allowed_content_type['Workspace']

        #
        # Workflow chains
        #

        ##workspaces = getattr(self.portal, WORKSPACES_ID)
        ##if '.cps_workflow_configuration' not in workspaces.objectIds():
        ##    workpaces.manage_addProduct['CPSCore'].addCPSWorkflowConfiguration()
        ##
        ### Adding wfc task chain
        ##wfc = getattr(workspaces, '.cps_workflow_configuration')
        ##wfc.manage_addChain(portal_type='CPS Task', chain='task_wf')

    def setupPortalActions(self):
        """Install the portal actions
        """

        # Cleaning actions
        actiondelmap = {
            'portal_actions': ('create_new_task',
                               'create_new_project',)}

        for tool, actionids in actiondelmap.items():
            actions = list(self.portal[tool]._actions)
            new_actions = []
            for ac in actions:
                id = ac.id
                if id not in actionids:
                    new_actions.append(ac)
                self.portal[tool]._actions = new_actions


        # ACTION : Create a new task
        # category : User
        self.portal['portal_actions'].addAction(
            id='create_new_task',
            name='_action_create_new_tasks',
            action='string: ${portal_url}/cps_task_create',
            condition="python:not portal.portal_membership.isAnonymousUser()",
            permission=(TaskCreate,),
            category='user',
            visible=1)

        self.log("  Added Action Create new task  ")

        # ACTION : Create a new project
        # category :Portal
        self.portal['portal_actions'].addAction(
            id='create_new_project',
            name='_action_create_new_project',
            action='string: ${portal_url}/cps_task_tool_manage_projects_form',
            condition="",
            permission=(ManageProjects,),
            category='global',
            visible=1)

        self.log("  Added Action Create new project  ")

    ###############################################
    ###############################################

###############################################
# __call__
###############################################

def install(self):
    installer = CPSInstaller(self)
    installer.install()
    return installer.logResult()
