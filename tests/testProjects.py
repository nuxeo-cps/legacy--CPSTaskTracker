import os, sys
if __name__ == '__main__':
    execfile(os.path.join(sys.path[0], 'framework.py'))

import unittest
from Testing import ZopeTestCase
import CPSTaskTrackerTestCase

from Products.CMFCore.utils import getToolByName

class TestProjects(CPSTaskTrackerTestCase.CPSTaskTrackerTestCase):
    def afterSetUp(self):
        self.login('root')

    def testProjects(self):
        #
        # Testing project API
        #
        tasks_tool = getToolByName(self.portal, 'portal_tasks')

        # Adding projects
        project1 = {'title':'Title1',
                    'description':'description1'}
        project2 = {'title':'Title2',
                    'description':'description2'}

        self.assertEqual(tasks_tool.addProject(project1), 1)
        self.assertEqual(tasks_tool.addProject(project1), 0)
        retreive_projects = tasks_tool.getProjects()

        self.assertEqual(len(retreive_projects), 1)
        self.assertEqual(retreive_projects[0], project1)

        self.assertEqual(tasks_tool.addProject(project2), 1)
        self.assertEqual(tasks_tool.addProject(project2), 0)
        retreive_projects = tasks_tool.getProjects()

        self.assertEqual(len(retreive_projects), 2)
        self.assertEqual(retreive_projects[1], project2)

        # Removals
        self.assertEqual(tasks_tool.delProjects(['Title1', 'Title2']), 1)
        self.assertEqual(tasks_tool.delProjects(['Title1', 'Title2']), 0)

        self.assertEqual(len(retreive_projects), 0)

        # Adding projects again
        project1 = {'title':'Title1',
                    'description':'description1'}
        project2 = {'title':'Title2',
                    'description':'description2'}

        self.assertEqual(tasks_tool.addProject(project1), 1)
        self.assertEqual(tasks_tool.addProject(project1), 0)
        retreive_projects = tasks_tool.getProjects()

        self.assertEqual(len(retreive_projects), 1)
        self.assertEqual(retreive_projects[0], project1)

        self.assertEqual(tasks_tool.addProject(project2), 1)
        self.assertEqual(tasks_tool.addProject(project2), 0)
        retreive_projects = tasks_tool.getProjects()

        self.assertEqual(len(retreive_projects), 2)
        self.assertEqual(retreive_projects[1], project2)

    def beforeTearDown(self):
        self.logout()

def test_suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(TestProjects))
    return suite
