import os, sys
if __name__ == '__main__':
    execfile(os.path.join(sys.path[0], 'framework.py'))

import unittest
from Testing import ZopeTestCase
import CPSTaskTrackerTestCase

from Products.CMFCore.utils import getToolByName

class TestGlobalInstall(CPSTaskTrackerTestCase.CPSTaskTrackerTestCase):
    def afterSetUp(self):
        self.login('root')

    def testCPS3(self):
        try:
            import Products.CPSCore
        except ImportError:
            raise "This unit tests are for CPS3 only sorry... !"

    def testInstallerScript(self):
        from Products.ExternalMethod.ExternalMethod import ExternalMethod
        installer = ExternalMethod('installer',
            'CPS TASK TRACKER NSTALLER', 'CPSTaskTracker.install',
            'install')
        self.portal._setObject('installer', installer)
        self.portal.installer()

    def testSkinsFixture(self):
        stool = getToolByName(self.portal, 'portal_skins')
        self.assertEqual('cps_task_tracker' in stool.objectIds(), 1)

    def testWorkflowInstallation(self):
        """Test task workflow installation
        """
        wftool = getToolByName(self.portal, 'portal_workflow')

        # wftool Installation
        self.assertEqual('task_wf' in wftool.objectIds(), 1)

    def testPortalTasksFixture(self):
        tasks_tool = getToolByName(self.portal, 'portal_tasks', None)

        # Portal existence
        self.assertNotEqual(tasks_tool, None)

        # workflow configuration object
        wfc = getattr(tasks_tool, '.cps_workflow_configuration')

        self.assertNotEqual(wfc, None)
        self.assertEqual(wfc.getPlacefulChainFor('CPS Task'), ('task_wf',))

    def testTaskScreenFixture(self):
        ttool = getToolByName(self.portal, 'portal_types', None)
        self.assertEqual('CPS Task Screen' in ttool.objectIds(), 1)

    def testTaskBoxFixture(self):
        ttool = getToolByName(self.portal, 'portal_types', None)
        self.assertEqual('CPS Task Box' in ttool.objectIds(), 1)

    def testTaskTypeFixture(self):
        ttool = getToolByName(self.portal, 'portal_types', None)
        self.assertEqual('CPS Task' in ttool.objectIds(), 1)

    def testPortalActions(self):
        # Checking if the actions are on the portal
        actions = {
            'portal_actions': ('create_new_task',
                               'create_new_project',)}
        for tool, actionids in actions.items():
            actions = list(self.portal[tool]._actions)
            portal_action_ids = [x.id for x in actions]
            for id in actionids:
                if id not in portal_action_ids:
                    raise "Action %s not installer" %id
    def beforeTearDown(self):
        self.logout()

def test_suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(TestGlobalInstall))
    return suite
