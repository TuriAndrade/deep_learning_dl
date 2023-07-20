def InputCallbackFactory(Exception):
    class InputCallback:
        @staticmethod
        def gtN(n: int) -> int:
            def callback(value: int) -> int:
                if value <= n:
                    raise Exception(f"Value must be greater than {n}.")
                else:
                    return value

            return callback

        @staticmethod
        def betweenNandM(
            n: float,
            m: float,
            nInclusive: bool = False,
            mInclusive: bool = False,
        ) -> float:
            def callback(value: float) -> float:
                if (value < n if nInclusive else value <= n) or (
                    value > m if mInclusive else value >= m
                ):
                    raise Exception(f"Value must be between {n} and {m}.")
                else:
                    return value

            return callback

    return InputCallback
