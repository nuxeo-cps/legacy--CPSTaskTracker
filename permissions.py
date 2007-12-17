# (C) Copyright 2004 Nuxeo SARL <http://nuxeo.com>
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

__author__ = "Julien Anguenot <ja@nuxeo.com>"

"""CPS Task Tracker Permissions

  - 'Task create' : Task creation facility
  - 'Manage projects' : Manage portal projects
"""

from Products.CMFCore.CMFCorePermissions import setDefaultRoles

TaskCreate = 'Task create'
setDefaultRoles(TaskCreate, ('Manager', 'Member'))

ViewProjects = 'View projects'
setDefaultRoles(ViewProjects, ('Manager', 'Member'))

ManageProjects = 'Manage projects'
setDefaultRoles(ManageProjects, ('Manager'))
