import typer


def PrinterFactory():
    class Printer:
        @staticmethod
        def print(msg: str, disable: bool = False, **kwargs) -> None:
            if (not disable) and (len(str(msg)) > 0):
                typer.secho(msg, **kwargs)

    return Printer
