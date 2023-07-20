from utils.ErrorAssert import ErrorAssert
from utils.Util import Util
from utils.Printer import Printer
from .Batch import BatchFactory

Batch = BatchFactory(
    ErrorAssert=ErrorAssert,
    Util=Util,
    Printer=Printer,
)
