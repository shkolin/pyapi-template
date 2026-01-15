class BaseRuntimeError(RuntimeError):
    message: str = 'Something went wrong'

    def __init__(self, *args: object) -> None:
        if args:
            super().__init__(*args)
        else:
            super().__init__(self.message)


class DomainError(RuntimeError):
    pass
