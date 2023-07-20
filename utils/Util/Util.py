def UtilFactory(ErrorAssert):
    class Util:
        @staticmethod
        def readRequiredArgs(requiredArgs: dict, inputArgs: dict) -> None:
            for key, value in requiredArgs.items():
                if value is None:
                    ErrorAssert.valueAssert(
                        (key in inputArgs) and (inputArgs[key] is not None),
                        f"{key} argmument must be passed.",
                    )
                    requiredArgs[key] = inputArgs[key]

                elif (key in inputArgs) and (inputArgs[key] is not None):
                    requiredArgs[key] = inputArgs[key]

    return Util
