class Machine:
    def __init__(self, name: str, family: str = None) -> None:
        self.name = name
        self.family = family if family else name

    def get_name(self) -> str:
        return self.name

    def get_family(self) -> str:
        return self.family

    def __str__(self):
        return self.name

    def __repr__(self):
        return self.name
