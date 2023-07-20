from typer import BadParameter
from .InputCallback import InputCallbackFactory

InputCallback = InputCallbackFactory(Exception=BadParameter)
