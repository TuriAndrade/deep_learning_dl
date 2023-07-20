from utils.ErrorAssert import ErrorAssert
from utils.Util import Util
from utils.Printer import Printer
from ..Batch import Batch
from ..Fold import Fold
from .Dataset import DatasetFactory

Dataset = DatasetFactory(
    ErrorAssert=ErrorAssert,
    Printer=Printer,
    Batch=Batch,
    Fold=Fold,
    Util=Util,
)
