""" Controlpanel API
"""
from zope.interface import Interface
from zope.component import adapter
from plone.restapi.controlpanels import RegistryConfigletPanel
from eea.api.layout.interfaces import IFixedLayoutBlocksSettings
from eea.api.layout.interfaces import IEeaApiLayoutLayer


@adapter(Interface, IEeaApiLayoutLayer)
class Controlpanel(RegistryConfigletPanel):
    """ Control Panel
    """
    schema = IFixedLayoutBlocksSettings
    configlet_id = "fixed-layout"
    configlet_category_id = "Products"
    schema_prefix = None
