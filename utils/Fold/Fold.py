from __future__ import annotations
from typing import Iterable, Any
from sklearn.model_selection import KFold
from tqdm import tqdm


def FoldFactory(ErrorAssert, Util, Batch, Printer) -> type:
    class Fold:
        def __init__(self, **inputArgs: dict) -> None:
            handledArgs: dict = self.__handleArgs(inputArgs=inputArgs)

            self.__trainPartition: Iterable[Batch] = handledArgs["trainPartition"]
            self.__validationPartition: Iterable[Batch] = handledArgs[
                "validationPartition"
            ]

        def getSize(self) -> int:
            return self.getTrainSize() + self.getValidationSize()

        def getTrainSize(self) -> int:
            return len(self.__trainPartition)

        def getValidationSize(self) -> int:
            return len(self.__validationPartition)

        def getTrainPartition(self) -> Iterable[Batch]:
            return self.__trainPartition

        def getValidationPartition(self) -> Iterable[Batch]:
            return self.__validationPartition

        @staticmethod
        def split(**inputArgs: dict) -> list[tuple[list[Batch], list[Batch]]]:
            handledArgs: dict = Fold.__handleSplitArgs(inputArgs=inputArgs)

            data: Iterable[Any] = handledArgs["data"]
            nFolds: int = handledArgs["nFolds"]
            batchSize: int = handledArgs["batchSize"]
            verbose: bool = handledArgs["verbose"]
            datasetName: str = handledArgs["datasetName"]

            Printer.print(
                "Spliting data into folds"
                if not datasetName
                else f"Spliting {datasetName} into folds",
                disable=(not verbose),
                fg="green",
                bold=True,
            )

            indexableData = list(data)

            kf = KFold(n_splits=nFolds, shuffle=True)
            folds: list[Fold] = []

            with tqdm(total=nFolds, colour="green", disable=(not verbose)) as bar:
                for trainIndexes, validationIndexes in kf.split(indexableData):
                    trainData: list[Any] = []
                    for i in trainIndexes:
                        trainData.append(indexableData[i])

                    validationData: list[Any] = []
                    for i in validationIndexes:
                        validationData.append(indexableData[i])

                    trainBatches = Batch.split(
                        data=trainData,
                        size=batchSize,
                        verbose=False,
                    )
                    validationBatches = Batch.split(
                        data=validationData,
                        size=batchSize,
                        verbose=False,
                    )

                    fold = Fold(
                        trainPartition=trainBatches,
                        validationPartition=validationBatches,
                    )

                    folds.append(fold)
                    bar.update(1)

            return folds

        @staticmethod
        def __handleArgs(
            inputArgs: dict,
        ) -> dict:
            requiredArgs: dict = {
                "trainPartition": None,
                "validationPartition": None,
            }

            Util.readRequiredArgs(requiredArgs=requiredArgs, inputArgs=inputArgs)

            args = requiredArgs

            ErrorAssert.valueAssert(
                hasattr(args["trainPartition"], "__iter__"),
                "Train partition must be iterable.",
            )
            ErrorAssert.valueAssert(
                hasattr(args["validationPartition"], "__iter__"),
                "Validation partition must be iterable.",
            )

            return args

        @staticmethod
        def __handleSplitArgs(
            inputArgs: dict,
        ) -> dict:
            requiredArgs: dict = {
                "data": None,
                "nFolds": 5,
                "verbose": True,
            }

            Util.readRequiredArgs(requiredArgs=requiredArgs, inputArgs=inputArgs)

            args = requiredArgs
            args["batchSize"] = (
                inputArgs["batchSize"] if "batchSize" in inputArgs else None
            )
            args["datasetName"] = (
                inputArgs["datasetName"] if "datasetName" in inputArgs else None
            )

            ErrorAssert.valueAssert(args["nFolds"] > 0, "Invalid number of folds.")
            ErrorAssert.valueAssert(
                hasattr(args["data"], "__iter__"), "Data must be iterable."
            )
            ErrorAssert.valueAssert(
                (args["batchSize"] is None) or isinstance(args["batchSize"], int),
                "If batch size is set, it must be an int.",
            )
            ErrorAssert.valueAssert(
                (args["batchSize"] is None) or (args["batchSize"] > 0),
                "If batch size is set, it must be greater than 0.",
            )
            ErrorAssert.valueAssert(
                args["datasetName"] is None or len(args["datasetName"]) > 0,
                "Invalid dataset name.",
            )

            return args

    return Fold
