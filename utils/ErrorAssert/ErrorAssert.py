from traceback import StackSummary, extract_stack


def ErrorAssertFactory(Printer):
    class ErrorAssert:
        @staticmethod
        def errorAssert(condition: bool, msg: str) -> None:
            if not condition:
                raise Exception(msg)

        @staticmethod
        def typeAssert(condition: bool, msg: str) -> None:
            if not condition:
                raise TypeError(msg)

        @staticmethod
        def valueAssert(condition: bool, msg: str) -> None:
            if not condition:
                raise ValueError(msg)

        @staticmethod
        def throwException(msg: str) -> None:
            raise Exception(msg)

        @staticmethod
        def throwTypeError(msg: str) -> None:
            raise TypeError(msg)

        @staticmethod
        def throwValueError(msg: str) -> None:
            raise ValueError(msg)

        @staticmethod
        def warningAssert(condition: bool, msg: str) -> None:
            if not condition:
                print()
                Printer.print("Warning: %s" % msg, color="yellow", bold=True)
                Printer.print("Traceback stack: ", color="yellow", bold=True)

                warningStack: StackSummary = extract_stack()
                ErrorAssert.printStack(warningStack)
                print()

        @staticmethod
        def throwWarning(msg: str) -> None:
            print()
            Printer.print("Warning: %s" % msg, color="yellow", bold=True)
            Printer.print("Traceback stack: ", color="yellow", bold=True)

            warningStack: StackSummary = extract_stack()
            ErrorAssert.printStack(warningStack)
            print()

        @staticmethod
        def printStack(
            errorStack: StackSummary,
            limit: int = -2,
            length: int = 3,
            color="yellow",
        ) -> None:
            errorStackLen = len(errorStack)

            if length is None or length < 0:
                length = 0

            elif length > errorStackLen:
                length = errorStackLen

            if limit is None or limit >= 0:
                if limit is None or limit == 0:
                    limit = errorStackLen

                elif limit > errorStackLen:
                    limit = errorStackLen

                if (limit - length) < 0:
                    length = limit

                for i in range(limit - length, limit):
                    Printer.print(
                        "-----------------------------------------------------------------------",
                        color=color,
                        bold=True,
                    )
                    Printer.print("File: %s" % str(errorStack[i][0]), color=color)
                    Printer.print("Line: %s" % str(errorStack[i][1]), color=color)
                    Printer.print("Call: %s" % str(errorStack[i][3]), color=color)

            else:
                if abs(limit) >= errorStackLen:
                    return None

                if (errorStackLen + limit - length) < 0:
                    length = errorStackLen + limit

                for i in range(errorStackLen + limit - length, errorStackLen + limit):
                    Printer.print(
                        "-----------------------------------------------------------------------",
                        color=color,
                        bold=True,
                    )
                    Printer.print("File: %s" % str(errorStack[i][0]), color=color)
                    Printer.print("Line: %s" % str(errorStack[i][1]), color=color)
                    Printer.print("Call: %s" % str(errorStack[i][3]), color=color)

    return ErrorAssert
