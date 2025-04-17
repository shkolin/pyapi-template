class UserEmail:
    def __init__(self, email: str) -> None:
        self.__email = email

    def __str__(self) -> str:
        return self.__email


class UserName:
    def __init__(self, name: str) -> None:
        self.__name = name

    def __str__(self) -> str:
        return self.__name


class UserPassword:
    def __init__(self, password: str) -> None:
        self.__pwd = password

    def __str__(self) -> str:
        return self.__pwd
