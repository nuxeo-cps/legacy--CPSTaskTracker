from Testing import ZopeTestCase
from Products.ExternalMethod.ExternalMethod import ExternalMethod
from Products.CPSDefault.tests import CPSTestCase

ZopeTestCase.installProduct('CPSNavigation')
ZopeTestCase.installProduct('CPSTaskTracker')

CPSTaskTrackerTestCase = CPSTestCase.CPSTestCase

class CPSTaskTrackerInstaller(CPSTestCase.CPSInstaller):
    def addPortal(self, id):
        """Override the Default addPortal method installing
        a Default CPS Site.

        Will launch the external method for CPSSubscriptions too.
        """

        # CPS Default Site
        factory = self.app.manage_addProduct['CPSDefault']
        factory.manage_addCPSDefaultSite(id,
                                         root_password1="passwd",
                                         root_password2="passwd",
                                         langs_list=['fr', 'en'])

        portal = getattr(self.app, id)

        # Install the CPSTaskTracker product
        cpstasktracker_installer = ExternalMethod('cpstasktracker_installer',
                                                    '',
                                                    'CPSTaskTracker.install',
                                                    'install')
        portal._setObject('cpstasktracker_installer', cpstasktracker_installer)
        portal.cpstasktracker_installer()

CPSTestCase.setupPortal(PortalInstaller=CPSTaskTrackerInstaller)

