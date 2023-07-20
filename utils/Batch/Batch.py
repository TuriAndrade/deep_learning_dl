from __future__ import annotations
from typing import Iterable, Any, Union
from tqdm import tqdm


def BatchFactory(ErrorAssert, Printer, Util) -> type:
    class Batch:
        def __init__(
            self,
            **inputArgs: dict,
        ) -> None:
            handledArgs: dict = self.__handleArgs(inputArgs=inputArgs)

            data: Iterable[Any] = handledArgs["data"]

            self.__size: int = len(data)
            self.__data: Iterable[Any] = data

        def getData(
            self,
            loader: Any,
        ) -> Any:
            loaded: Union[Any, tuple[Any, Any]] = loader(self.__data)

            loadedData: Any = None
            loadedLabels: Any = None

            if len(loaded) == 1:  # labels not included
                loadedData = loaded

                return loadedData

            elif len(loaded) == 2:  # labels included
                loadedData, loadedLabels = loaded

                return loadedData, loadedLabels

            else:
                ErrorAssert.throwValueError("Loaded data must be of shape N or NxN.")

        def getSize(self) -> int:
            return self.__size

        @staticmethod
        def split(**inputArgs: dict) -> list[Batch]:
            handledArgs: dict = Batch.__handleSplitArgs(inputArgs=inputArgs)

            data: Iterable[Any] = handledArgs["data"]
            size: int = handledArgs["size"]
            datasetName: str = handledArgs["datasetName"]
            verbose: bool = handledArgs["verbose"]

            Printer.print(
                "Spliting data into batches"
                if not datasetName
                else f"Spliting {datasetName} into batches",
                disable=(not verbose),
                fg="green",
                bold=True,
            )

            indexableData = list(data)

            lenData = len(data)
            correctedSize = size if size else lenData

            nBatches = (
                lenData // correctedSize
                if lenData % correctedSize == 0
                else (lenData // correctedSize) + 1
            )
            batches: list[Batch] = []

            with tqdm(total=nBatches, colour="green", disable=(not verbose)) as bar:
                for i in range(0, lenData, correctedSize):
                    batch = Batch(
                        data=indexableData[i : i + correctedSize],
                    )
                    batches.append(batch)
                    bar.update(1)

            return batches

        @staticmethod
        def __handleArgs(inputArgs: dict) -> dict:
            requiredArgs: dict = {
                "data": None,
            }

            Util.readRequiredArgs(requiredArgs=requiredArgs, inputArgs=inputArgs)

            args = requiredArgs
            ErrorAssert.valueAssert(
                hasattr(args["data"], "__iter__"), "Data must be iterable."
            )
            ErrorAssert.valueAssert(
                len(args["data"]) > 0, "Data size must be greater than 0."
            )

            return args

        @staticmethod
        def __handleSplitArgs(
            inputArgs: dict,
        ) -> dict:
            requiredArgs: dict = {
                "data": None,
                "verbose": True,
            }

            Util.readRequiredArgs(requiredArgs=requiredArgs, inputArgs=inputArgs)

            args = requiredArgs
            args["size"] = inputArgs["size"] if "size" in inputArgs else None
            args["datasetName"] = (
                inputArgs["datasetName"] if "datasetName" in inputArgs else None
            )

            ErrorAssert.valueAssert(
                (args["size"] is None)
                or (
                    isinstance(args["size"], int)
                    and (args["size"] > 0)
                    and args["size"] <= len(args["data"])
                ),
                "Invalid batch size.",
            )
            ErrorAssert.valueAssert(
                hasattr(args["data"], "__iter__"), "Data must be iterable."
            )
            ErrorAssert.valueAssert((len(args["data"]) > 0), "Invalid data size.")
            ErrorAssert.valueAssert(
                args["datasetName"] is None or len(args["datasetName"]) > 0,
                "Invalid dataset name.",
            )

            return args

    return Batch
