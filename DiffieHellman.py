class DiffieHellman:
    def __init__(self,  p: int = None, g: int = None,
                        a: int = None, b: int = None,
                        A: int = None, B: int = None):
        self.p: int = p # prime number
        self.g: int = g # generator
        self.a: int = a # Person A Private
        self.b: int = b # Person B Private
        self.A: int = A # Person A Public
        self.B: int = B # Person B Public

    @staticmethod
    def isNone(*NumsToCheck: int | None) -> bool:
        """True if None False if Not None"""
        for num in NumsToCheck:
            if num is None:
                return True
        return False

    def checkInput(*NumsToCheck: int | None) -> bool:
        """Check if input is a valid number or not"""
        if len(NumsToCheck) == 0:
            return False
        for num in NumsToCheck:
            if type(num) is not int or num < 1:
                return False
        return True

    def calcPublic(self, private: int) -> int:
        if (self.isNone(self.p, self.g, private)):
            return f"{self.COLORS["RED"]}Invalid Input!{self.COLORS["WHITE"]}"
        return pow(self.g, private, self.p)

    COLORS: dict = {
    'RED' : '\033[91m',
    'GREEN' :  '\033[92m',
    'YELLOW' :  '\033[93m',
    'BLUE' :  '\033[94m',
    'PURPLE' :  '\033[95m',
    'CYAN' : '\033[96m',
    'WHITE' : '\033[m'
    }