# (C) Copyright 2003 Nuxeo SARL <http://nuxeo.com>
# (C) Copyright 2003 CEA <http://www.cea.fr>
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

import os, sys
from zLOG import LOG, INFO, DEBUG

def install(self):

    _log = []

    def pr(bla, zlog=1, _log=_log):
        if bla == 'flush':
            return '\n'.join(_log)

        _log.append(bla)
        if (bla and zlog):
            LOG('CPSTaskTracker install:', INFO, bla)

    def prok(pr=pr):
        pr(" Already correctly installed")


    pr("Starting CPSTaskTracker install")

    portal = self.portal_url.getPortalObject()

    def portalhas(id, portal=portal):
        return id in portal.objectIds()


    #################################################################
    # Creation of the CPS Task Tool
    #################################################################

    skins = ('cps_task_tracker', 'cmf_zpt_calendar', 'cmf_calendar')
    paths = {
        'cps_task_tracker': 'Products/CPSTaskTracker/skins/cps2_default',
        'cmf_zpt_calendar': 'Products/CMFCalendar/skins/zpt_calendar',
        'cmf_calendar': 'Products/CMFCalendar/skins/calendar',
    }

    for skin in skins:
        path = paths[skin]
        path = path.replace('/', os.sep)
        pr(" FS Directory View '%s'" % skin)
        if skin in portal.portal_skins.objectIds():
            dv = portal.portal_skins[skin]
            oldpath = dv.getDirPath()
            if oldpath == path:
                prok()
            else:
                pr("  Correctly installed, correcting path")
                dv.manage_properties(dirpath=path)
        else:
            portal.portal_skins.manage_addProduct['CMFCore'].manage_addDirectoryView(\
                filepath=path, id=skin)
            pr("  Creating skin")
    allskins = portal.portal_skins.getSkinPaths()
    for skin_name, skin_path in allskins:
        if skin_name != 'Basic':
            continue
        path = [x.strip() for x in skin_path.split(',')]
        path = [x for x in path if x not in skins] # strip all
        if path and path[0] == 'custom':
            path = path[:1] + list(skins) + path[1:]
        else:
            path = list(skins) + path
        npath = ', '.join(path)
        portal.portal_skins.addSkinSelection(skin_name, npath)
        pr(" Fixup of skin %s" % skin_name)

    #################################################################
    # i18n for the product
    #################################################################

    mcat = portal.portal_messages

    pr(" Checking available languages")
    langs = []
    languages = mcat.get_languages()

    # Working now on the po files
    product_path = sys.modules['Products.CPSTaskTracker'].__path__[0]
    i18n_path = os.path.join(product_path, 'i18n')
    pr(" po files for CPSTaskTracker are searched in %s" % i18n_path)
    pr(" po files for CPSTaskTracker %s are expected" % str(languages))

    # loading po files for the product itself.
    for lang in languages:
        po_filename = lang + '.po'
        pr("   importing %s file" % po_filename)
        po_path = os.path.join(i18n_path, po_filename)
        try:
            po_file = open(po_path)
        except NameError:
            pr("    %s file not found" % po_path)
        po_path = os.path.join(i18n_path, po_filename)
        try:
            po_file = open(po_path)
        except NameError:
            pr("    %s file not found" % po_path)
        else:
            pr("  before  %s file imported" % po_path)
            mcat.manage_import(lang, po_file)
            pr("    %s file imported" % po_path)

    # loading po files for the calendar product.
    for lang in languages:
        po_filename = 'Calendar-'+lang + '.po'
        pr("   importing %s file" % po_filename)
        po_path = os.path.join(i18n_path, po_filename)
        try:
            po_file = open(po_path)
        except NameError:
            pr("    %s file not found" % po_path)
        po_path = os.path.join(i18n_path, po_filename)
        try:
            po_file = open(po_path)
        except NameError:
            pr("    %s file not found" % po_path)
        else:
            pr("  before  %s file imported" % po_path)
            mcat.manage_import(lang, po_file)
            pr("    %s file imported" % po_path)

    #################################################################
    # Instanciation of the CPS Task Tool
    #################################################################

    if portalhas('portal_tasks'):
        prok()
    else:
        pr(" Creating portal_tasks")
        portal.manage_addProduct["CPSTaskTracker"].manage_addTool(
            'CPS Task Tool')

    #################################################################
    # Registring CPS Task/CPS Task Screen as portal_types
    #################################################################

    pr("Verifying portal types")
    newptypes = ('CPS Task', 'CPS Task Screen')
    ttool = portal.portal_types
    if 'Workgroup' in ttool.objectIds():
        workspaceACT = list(ttool['Workgroup'].allowed_content_types)
    else:
        #raise str("DependanceError"), str('Workspace')
        pass
    #
    # Only the CPSTaskScreen allowed within Workspaces
    #
    for ptype in ['CPS Task Screen']:
        if (ptype not in  workspaceACT):
            pr("Allowing %s in workgroup" %ptype)
            workspaceACT.append(ptype)

    allowed_content_type = {
                            'Workgroup' : workspaceACT,
                            }

    ttool['Workgroup'].allowed_content_types = allowed_content_type['Workgroup']

    ptypes_installed = ttool.objectIds()

    ptypes = {
        'CPSTaskTracker':('CPS Task',
                          'CPS Task Screen'
                          )
        }

    for prod in ptypes.keys():
        for ptype in ptypes[prod]:
            pr("  Type '%s'" % ptype)
            if ptype in ptypes_installed:
                ttool.manage_delObjects([ptype])
                pr("   Deleted   ")

            ttool.manage_addTypeInformation(
                id=ptype,
                add_meta_type='Factory-based Type Information',
                typeinfo_name=prod+': '+ptype,
                )
            pr("   Installation   ")

    #####################################################
    # Actions : my tasks
    #####################################################

    # Verification of the action and addinf if neccesarly
    action_found = 0
    for action in portal['portal_actions'].listActions():
        if action.id == 'Create a New Task':
            action_found = 1

    if not action_found:
        portal['portal_actions'].addAction(
            id='Create a New Task',
            name='_action_create_new_tasks',
            action='string: ${portal_url}/cps_task_create?base=CPS Task',
            condition='python:not portal.portal_membership.isAnonymousUser()',
            permission=('View',),
            category='global',
            visible=1)
        pr(" Added Action My Tasks")

    ##########################################
    # IMPORTING THE WORKFLOW
    ##########################################

    def package_home(name):
        """ Returns path to Products.name"""
        m = sys.modules['Products.%s' % name]
        return (m.__path__[0])

    def tryimport(container, name, zexpdir, suffix='xml', pr=None):
        zexppath = os.path.join(zexpdir, '%s.%s' % (name, suffix))
        container._importObjectFromFile(zexppath)
        pr(" Import of %s.%s" % (name, suffix))

    cps_home = package_home('CPSTaskTracker')
    zexpdir = os.path.join(cps_home, 'Install')

    if portal.portal_workflow is not None:
        # Ws for the tasks
        if 'task_wf' in portal.portal_workflow.objectIds():
            portal.portal_workflow.manage_delObjects('task_wf')
        tryimport(portal.portal_workflow, 'task_wf', zexpdir, suffix='xml', pr=pr)


        wfs = {
            'CPS Task' : 'task_wf',
            'CPS Task Screen' : '',
            }

        wftool = portal.portal_workflow
        pr("Updating workflow schemas")

        for pt, chain in wfs.items():
            wftool.setChainForPortalTypes([pt], chain)

    #################################################
    # CMF Calendar installation for the date
    #################################################

    # CMF Tools
    pr("")
    pr("### CMFCalendar update")
    if not portalhas('cmfcalendar_installer'):
        if portalhas('portal_calendar'):
            portal.manage_delObjects(['portal_calendar'])
        from Products.ExternalMethod.ExternalMethod import ExternalMethod
        pr('Adding cmfcalendar installer')
        cmfcalendar_installer = ExternalMethod('cmfcalendar_installer',
                                               'CMFCalendar Updater',
                                               'CMFCalendar.Install',
                                               'install')
        portal._setObject('cmfcalendar_installer', cmfcalendar_installer)
        pr(portal.cmfcalendar_installer())
    pr("### End of CMFCalendar update")
    pr("")

    pr("End of specific CPSTaskTracker install")
    return pr('flush')
