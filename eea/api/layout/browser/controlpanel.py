""" Control Panel
"""
from plone.app.registry.browser import controlpanel
from eea.api.layout.interfaces import IFixedLayoutBlocksSettings
from eea.api.layout import EEAMessageFactory as _


class ControlPanelForm(controlpanel.RegistryEditForm):
    """ Control Panel Form"""
    id = "fixed-layout"
    label = _(u"Dexterity Fixed Layout")
    schema = IFixedLayoutBlocksSettings


class ControlPanelView(controlpanel.ControlPanelFormWrapper):
    """ Control Panel
    """
    form = ControlPanelForm
