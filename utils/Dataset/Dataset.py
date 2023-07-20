from typing import Iterable, Any
from sklearn.model_selection import train_test_split


def DatasetFactory(ErrorAssert, Printer, Batch, Fold, Util) -> type:
    class Dataset:
        def __init__(
            self,
            **inputArgs: dict,
        ):
            handledArgs: dict = self.__handleArgs(inputArgs=inputArgs)

            self.__data: Iterable[Any] = handledArgs["data"]
            self.__trainData: Iterable[Any] = handledArgs["trainData"]
            self.__validationData: Iterable[Any] = handledArgs["validationData"]
            self.__testData: Iterable[Any] = handledArgs["testData"]
            self.__dataLoader: Any = handledArgs["dataLoader"]
            self.__crossValidation: bool = handledArgs["crossValidation"]
            self.__randomState: int = handledArgs["randomState"]
            self.__splitInBatches: bool = handledArgs["splitInBatches"]
            self.__nFolds: int = handledArgs["nFolds"]
            self.__trainSetFrac: float = handledArgs["trainSetFrac"]
            self.__validationSetFrac: float = handledArgs["validationSetFrac"]
            self.__batchSize: int = (
                handledArgs["batchSize"] if self.__splitInBatches else None
            )
            self.__verbose: bool = handledArgs["verbose"]
            self.__name: str = handledArgs["name"]
            self.__splitTrainAndTest: bool = handledArgs["splitTrainAndTest"]

            self.__isDataSplit: bool = self.__data is None
            self.__testSetFrac: bool = 1 - self.__trainSetFrac
            self.__crossValidationSet: list[Fold] = []
            self.__trainSet: list[Batch] = []
            self.__validationSet: list[Batch] = []
            self.__testSet: list[Batch] = []
            self.__dataset: list[Batch] = []
            self.__trainSize: int = 0
            self.__crossValidationSize: int = 0
            self.__validationSize: int = 0
            self.__datasetSize: int = 0

        def getName(self) -> str:
            return self.__name

        def getNFolds(self) -> int:
            return self.__nFolds

        def getTrainSize(self) -> int:
            return self.__trainSize

        def getCrossValidationSize(self) -> int:
            return self.__crossValidationSize

        def getValidationSize(self) -> int:
            return self.__validationSize

        def getTestSize(self) -> int:
            return self.__testSize

        def getDatasetSize(self) -> int:
            return self.__datasetSize

        def crossValidation(self) -> bool:
            return self.__crossValidation

        def getDataLoader(self) -> Any:
            return self.__dataLoader

        def splitTrainAndTest(self) -> tuple:
            Printer.print(
                "Spliting data into train, validation and test sets",
                disable=(not self.__verbose),
                fg="green",
                bold=True,
            )

            trainAndVal, self.__testData = train_test_split(
                self.__data,
                train_size=self.__trainSetFrac,
                random_state=self.__randomState,
            )

            self.__trainData, self.__validationData = train_test_split(
                trainAndVal,
                test_size=self.__validationSetFrac,
                random_state=self.__randomState,
            )

        def getTrainSet(self) -> list[Fold]:
            return self.__trainSet

        def getCrossValidationSet(self) -> list[Fold]:
            return self.__crossValidationSet

        def getValidationSet(self) -> list[Batch]:
            return self.__validationSet

        def getTestSet(self) -> list[Batch]:
            return self.__testSet

        def getDataset(self) -> list[Batch]:
            return self.__dataset

        def build(self) -> tuple:
            Printer.print(
                "Building dataset"
                if not self.__name
                else f"Building {self.__name} dataset",
                disable=(not self.__verbose),
                fg="blue",
                bold=True,
            )

            if self.__splitTrainAndTest:
                if not self.__isDataSplit:
                    self.splitTrainAndTest()

                if self.__crossValidation:
                    self.__crossValidationSet = Fold.split(
                        data=self.__trainData,
                        nFolds=self.__nFolds,
                        batchSize=self.__batchSize,
                        verbose=self.__verbose,
                        datasetName="cross validation set",
                    )

                    for fold in self.__crossValidationSet:
                        self.__crossValidationSize += fold.getSize()

                self.__trainSet = Batch.split(
                    data=self.__trainData,
                    size=self.__batchSize,
                    verbose=self.__verbose,
                    datasetName="train set",
                )
                self.__trainSize = len(self.__trainSet)

                self.__validationSet = Batch.split(
                    data=self.__validationData,
                    size=self.__batchSize,
                    verbose=self.__verbose,
                    datasetName="validation set",
                )
                self.__validationSize = len(self.__validationSet)

                self.__testSet = Batch.split(
                    data=self.__testData,
                    size=self.__batchSize,
                    verbose=self.__verbose,
                    datasetName="test set",
                )
                self.__testSize = len(self.__testSet)

            else:
                self.__dataset = Batch.split(
                    data=self.__data,
                    size=self.__batchSize,
                    verbose=self.__verbose,
                    datasetName="train set",
                )
                self.__datasetSize = len(self.__dataset)

            Printer.print(
                "Dataset built\n",
                disable=(not self.__verbose),
                fg="blue",
                bold=True,
            )

            return (
                (
                    self.__trainSet,
                    self.__validationSet,
                    self.__testSet,
                    self.__crossValidationSet,
                )
                if self.__splitTrainAndTest
                else self.__dataset
            )

        @staticmethod
        def __handleArgs(
            inputArgs: dict,
        ) -> dict:
            requiredArgs: dict = {
                "crossValidation": True,
                "splitInBatches": True,
                "randomState": 42,
                "nFolds": 5,
                "trainSetFrac": 0.9,
                "validationSetFrac": 0.1,
                "batchSize": 32,
                "verbose": True,
                "dataLoader": lambda data: data,
                "splitTrainAndTest": True,
            }

            Util.readRequiredArgs(requiredArgs=requiredArgs, inputArgs=inputArgs)

            args = requiredArgs
            args["data"] = inputArgs["data"] if "data" in inputArgs else None
            args["trainData"] = (
                inputArgs["trainData"] if "trainData" in inputArgs else None
            )
            args["validationData"] = (
                inputArgs["validationData"] if "validationData" in inputArgs else None
            )
            args["testData"] = (
                inputArgs["testData"] if "testData" in inputArgs else None
            )
            args["name"] = inputArgs["name"] if "name" in inputArgs else None

            ErrorAssert.valueAssert(
                args["data"] is not None
                and hasattr(args["data"], "__iter__")
                or (
                    (
                        args["trainData"] is not None
                        and hasattr(args["trainData"], "__iter__")
                    )
                    and (
                        args["validationData"] is not None
                        and hasattr(args["validationData"], "__iter__")
                    )
                    and (
                        args["testData"] is not None
                        and hasattr(args["testData"], "__iter__")
                    )
                ),
                "Data must be iterable.",
            )

            ErrorAssert.typeAssert(
                isinstance(args["splitTrainAndTest"], bool),
                "Split train and test arg must be bool.",
            )

            ErrorAssert.typeAssert(
                not args["splitTrainAndTest"]
                or isinstance(args["trainSetFrac"], float),
                "Train set fraction must be a float.",
            )
            ErrorAssert.valueAssert(
                not args["splitTrainAndTest"]
                or args["trainSetFrac"] > 0
                and args["trainSetFrac"] < 1,
                "Train set fraction must be between 0 and 1.",
            )

            ErrorAssert.typeAssert(
                not args["splitTrainAndTest"]
                or isinstance(args["validationSetFrac"], float),
                "Train set fraction must be a float.",
            )
            ErrorAssert.valueAssert(
                not args["splitTrainAndTest"]
                or args["validationSetFrac"] > 0
                and args["validationSetFrac"] < 1,
                "Validation set fraction must be between 0 and 1.",
            )

            ErrorAssert.valueAssert(
                not args["splitTrainAndTest"]
                or args["crossValidation"] is False
                or isinstance(args["nFolds"], int),
                "If cross validation is set, number of folds must be an int.",
            )
            ErrorAssert.valueAssert(
                not args["splitTrainAndTest"]
                or args["crossValidation"] is False
                or (args["nFolds"] > 0),
                "If cross validation is set, number of folds must be greater than 0.",
            )

            ErrorAssert.valueAssert(
                not args["splitTrainAndTest"] or isinstance(args["randomState"], int),
                "Random state must be an int.",
            )
            ErrorAssert.valueAssert(
                not args["splitTrainAndTest"] or (args["randomState"] >= 0),
                "Random state must be greater than or equal to 0.",
            )

            ErrorAssert.valueAssert(
                args["splitInBatches"] is False or isinstance(args["batchSize"], int),
                "If split in batches is set, batch size must be an int.",
            )
            ErrorAssert.valueAssert(
                args["splitInBatches"] is False or (args["batchSize"] > 0),
                "If split in batches is set, batch size must be greater than 0.",
            )

            return args

    return Dataset
