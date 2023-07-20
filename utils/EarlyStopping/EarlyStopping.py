import numpy as np


def EarlyStoppingFactory(ErrorAssert, Util, Printer) -> type:
    class EarlyStopping:
        def __init__(
            self,
            **inputArgs: dict,
        ):
            handledArgs: dict = self.__handleArgs(inputArgs=inputArgs)

            self.__patience: int = handledArgs["patience"]
            self.__verbose: bool = handledArgs["verbose"]
            self.__delta: float = handledArgs["delta"]
            self.__offset: int = handledArgs["offset"]

            self.__counter: int = 0
            self.__bestScore: float = None
            self.__stop: bool = False
            self.__minLoss: float = np.inf
            self.__iter: int = 0
            self.__isBest: bool = False

        def __call__(self, loss: float) -> None:
            self.__iter += 1

            if self.__iter > self.__offset:
                score: float = -loss

                if self.__bestScore is None:
                    self.__bestScore = score
                    self.__minLoss = loss
                    self.__counter = 0
                    self.__isBest = True

                elif score < self.__bestScore + self.__delta:
                    self.__counter += 1
                    self.__isBest = False

                    Printer.print(
                        f"EarlyStopping counter: {self.__counter} out of {self.__patience}",
                        disable=(not self.__verbose),
                        fg="green",
                        bold=True,
                    )

                    if self.__counter >= self.__patience:
                        self.__stop = True
                else:
                    self.__bestScore = score
                    self.__minLoss = loss
                    self.__counter = 0
                    self.__stop = False
                    self.__isBest = True

        def stop(self) -> bool:
            return self.__stop

        def getMinLoss(self) -> float:
            return self.__minLoss

        def isBest(self) -> bool:
            return self.__isBest

        @staticmethod
        def __handleArgs(inputArgs: dict) -> dict:
            requiredArgs: dict = {
                "patience": 10,
                "verbose": False,
                "delta": 0.0,
                "offset": 20,
            }

            Util.readRequiredArgs(requiredArgs=requiredArgs, inputArgs=inputArgs)

            args = requiredArgs

            ErrorAssert.typeAssert(
                isinstance(args["patience"], int), "Patience must be an int."
            )
            ErrorAssert.valueAssert(
                args["patience"] > 0, "Patience must be greater than 0"
            )

            ErrorAssert.typeAssert(
                isinstance(args["delta"], float) or isinstance(args["delta"], int),
                "Delta must be a number.",
            )
            ErrorAssert.valueAssert(
                args["delta"] >= 0, "Delta must be greater than or equal to 0."
            )

            ErrorAssert.typeAssert(
                isinstance(args["offset"], int), "Offset must be an int."
            )
            ErrorAssert.valueAssert(
                args["offset"] >= 0, "Offset must be greater than or equal to 0"
            )

            return args

    return EarlyStopping
