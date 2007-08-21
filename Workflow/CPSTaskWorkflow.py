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

"""CPSTask type workflow definition
"""

import os, sys
from zLOG import LOG, INFO, DEBUG
from Products.CMFCore.CMFCorePermissions import View, ModifyPortalContent

from Products.CPSWorkflow.transitions import \
     TRANSITION_INITIAL_CREATE, \
     TRANSITION_ALLOWSUB_CHECKOUT, \
     TRANSITION_ALLOWSUB_CREATE, \
     TRANSITION_ALLOWSUB_DELETE, \
     TRANSITION_ALLOWSUB_COPY, \
     TRANSITION_ALLOWSUB_MOVE, \
     TRANSITION_BEHAVIOR_PUBLISHING

from Products.DCWorkflow.Transitions import \
     TRIGGER_USER_ACTION

def CPSTaskWorkflowInstall(self):
    """Installs the workflow for the CPS Task Type
    """

    portal = self.portal_url.getPortalObject()
    wftool = portal.portal_workflow

    wfids = wftool.objectIds()
    wfid = 'task_wf'

    if wfid in wfids:
        wftool.manage_delObjects([wfid])

    wftool.manage_addWorkflow(id=wfid,
                              workflow_type='cps_workflow (Web-configurable workflow for CPS)')

    wf = wftool[wfid]

    for p in (View, ModifyPortalContent, ):
        wf.addManagedPermission(p)

    ###########################################################################
    ###########################################################################

    #                                  STATES

    ###########################################################################
    ###########################################################################

    for s in ('waiting',
              'processed',
              'closed',):
        wf.states.addState(s)


    ###########################################################################
    #                                   WAITING
    ###########################################################################

    s = wf.states.get('waiting')

    #s.setPermission(ModifyPortalContent, 0, ('Manager',
    #                                         'Owner',
    #                                         'WorkspaceManager'
    #                                         'WorkspaceMember',))
    #s.setPermission(View, 0, ('Manager',
    #                          'Owner',
    #                          'WorkspaceManager',
    #                          'WorkspaceMember',
    #                          'WorkspaceReader',))

    s.setInitialState('waiting')
    s.setProperties(title='',
                    description='',
                    transitions=('accept',
                                 'close',
                                 'recall',
                                 'reject',
                                 'history',
                                 'reinit',
                                 ))


    ###########################################################################
    #                              PROCESSED
    ###########################################################################

    s = wf.states.get('processed')

    #s.setPermission(ModifyPortalContent, 0, ('Manager',
    #                                         'Owner',
    #                                         'WorkspaceManager',))
    #s.setPermission(View, 0, ('Manager',
    #                          'Owner',
    #                          'WorkspaceManager',
    #                          'WorkspaceMember',
    #                          'WorkspaceReader',))

    s.setProperties(title='',
                    description='',
                    transitions=('close',
                                 'recall',
                                 'history',
                                 'reinit',))


    ###########################################################################
    #                                      CLOSED
    ###########################################################################

    s = wf.states.get('closed')

    #s.setPermission(ModifyPortalContent, 0, ())
    #
    ## XXX check who's able to see the MailFolder in a closed state
    #s.setPermission(View, 0, ('Manager',
    #                          'Owner',
    #                          'WorkspaceManager',
    #                          'WorkspaceMember',
    #                          'WorkspaceReader'))

    s.setProperties(title='',
                    description='',
                    transitions=('assign',
                                 'history',
                                 'reinit',))


    ###########################################################################
    ###########################################################################

    #                               TRANSITIONS

    ###########################################################################
    ###########################################################################

    for t in ('create',
              'accept',
              'reinit',
              'close',
              'recall',
              'reject',
              'history'):
        wf.transitions.addTransition(t)

    ###########################################################################
    #                             CREATE
    ###########################################################################

    # Nota : this replaces the initial transition of DCWorkflow.
    t = wf.transitions.get('create')
    t.setProperties(title='Initial creation',
                    description='Intial transition like',
                    new_state_id='waiting',
                    transition_behavior=(TRANSITION_INITIAL_CREATE, ),
                    clone_allowed_transitions=None,
                    actbox_name='', actbox_category='', actbox_url='',
                    props={'guard_permissions':'',
                           'guard_roles':'Manager; Member',
                           'guard_expr':''},)

    ###########################################################################
    #                            ACCEPT
    ###########################################################################

    t = wf.transitions.get('accept')
    t.setProperties(title='',
                    description='',
                    new_state_id='processed',
                    trigger_type=TRIGGER_USER_ACTION,
                    actbox_name='_action_accept',
                    actbox_category='workflow',
                    actbox_url='%(content_url)s/cps_task_accept_form',
                    props={'guard_permissions':'',
                           'guard_roles':'Manager;Member',
                           'guard_expr':"python:state_change['object'].getContent().isAssigned()"},)

    ###########################################################################
    #                            CLOSE
    ###########################################################################

    t = wf.transitions.get('close')
    t.setProperties(title='',
                    description='',
                    new_state_id='closed',
                    trigger_type=TRIGGER_USER_ACTION,
                    actbox_name='_action_close_task',
                    actbox_category='workflow',
                    actbox_url='%(content_url)s/cps_task_close_form',
                    props={'guard_permissions':'',
                           'guard_roles':'Manager;Member',
                           'guard_expr':"python:state_change['object'].getContent().isTheAssignedOne()"},)


    ###########################################################################
    #                            RECALL
    ###########################################################################

    t = wf.transitions.get('recall')
    t.setProperties(title='',
                    description='',
                    new_state_id='',
                    trigger_type=TRIGGER_USER_ACTION,
                    actbox_name='_action_recall_',
                    actbox_category='workflow',
                    actbox_url='%(content_url)s/cps_task_recall_assignee_form',
                    props={'guard_permissions':'',
                           'guard_roles':'Manager;Member',
                           'guard_expr':"python:state_change['object'].getContent().isCreator()"},)

    ###########################################################################
    #                            REINIT
    ###########################################################################

    t = wf.transitions.get('reinit')
    t.setProperties(title='',
                    description='',
                    new_state_id='waiting',
                    trigger_type=TRIGGER_USER_ACTION,
                    actbox_name='_action_reinit_',
                    actbox_category='workflow',
                    actbox_url='%(content_url)s/cps_task_reinit_form',
                    props={'guard_permissions':'',
                           'guard_roles':'Manager;Member',
                           'guard_expr':"python:state_change['object'].getContent().isCreator()"},)

    ###########################################################################
    #                            REJECT
    ###########################################################################

    t = wf.transitions.get('reject')
    t.setProperties(title='',
                    description='',
                    new_state_id='',
                    trigger_type=TRIGGER_USER_ACTION,
                    actbox_name='_action_reject',
                    actbox_category='workflow',
                    actbox_url='%(content_url)s/cps_task_reject_form',
                    props={'guard_permissions':'',
                           'guard_roles':'Manager;Member',
                           'guard_expr':"python:state_change['object'].getContent().isAssigned()"},)

    ###########################################################################
    #                            REJECT
    ###########################################################################

    t = wf.transitions.get('history')
    t.setProperties(title='',
                    description='',
                    new_state_id='',
                    trigger_type=TRIGGER_USER_ACTION,
                    actbox_name='_action_current_status_',
                    actbox_category='workflow',
                    actbox_url='%(content_url)s/cps_task_status_history',
                    props={'guard_permissions':'',
                           'guard_roles':'Manager;Member',
                           'guard_expr':''},)

    ###########################################################################
    ###########################################################################

    #                                     VARIABLES

    ###########################################################################
    ###########################################################################

    for v in ('action',
              'actor',
              'comments',
              'review_history',
              'time',
              'dest_container',
              ):
        wf.variables.addVariable(v)


    wf.variables.setStateVar('review_state')
    vdef = wf.variables['action']
    vdef.setProperties(description='The last transition',
                       default_expr='transition/getId|nothing',
                       for_status=1, update_always=1)

    vdef = wf.variables['actor']
    vdef.setProperties(description='The ID of the user who performed '
                       'the last transition',
                       default_expr='user/getId',
                       for_status=1, update_always=1)

    vdef = wf.variables['comments']
    vdef.setProperties(description='Comments about the last transition',
                       default_expr="python:state_change.kwargs.get('comment',\
                       '')",
                       for_status=1, update_always=1)

    vdef = wf.variables['review_history']
    vdef.setProperties(description='Provides access to workflow history',
                       default_expr="state_change/getHistory",
                       props={'guard_permissions':'',
                              'guard_roles':'Manager; WorkspaceManager; \
                              WorkspaceMember; WorkspaceReader; Member',
                              'guard_expr':''})

    vdef = wf.variables['time']
    vdef.setProperties(description='Time of the last transition',
                       default_expr="state_change/getDateTime",
                       for_status=1, update_always=1)

    vdef = wf.variables['dest_container']
    vdef.setProperties(description='Destination container for the last \
    paste/publish',
                       default_expr="python:state_change.kwargs.get(\
                       'dest_container', '')",
                       for_status=1, update_always=1)
