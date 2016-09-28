""" main dandelion package
"""

from dandelion.base import DandelionException, DandelionConfig
from dandelion.datagem import Datagem
from dandelion.datatxt import DataTXT
from dandelion.datatxt import ClassifierCrud

__version__ = '0.2.2'
default_config = DandelionConfig()
