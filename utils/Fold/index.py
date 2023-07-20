from utils.ErrorAssert import ErrorAssert
from utils.Util import Util
from utils.Printer import Printer
from ..Batch import Batch
from .Fold import FoldFactory

Fold = FoldFactory(ErrorAssert=ErrorAssert, Util=Util, Batch=Batch, Printer=Printer)
