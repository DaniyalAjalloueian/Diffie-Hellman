from math import isqrt
from time import sleep


class DiffieHellman:
    COLORS: dict[str, str] = {
        "RED": "\033[91m",
        "GREEN": "\033[92m",
        "YELLOW": "\033[93m",
        "PURPLE": "\033[95m",
        "CYAN": "\033[96m",
        "WHITE": "\033[m"
    }

    def __init__(
        self,
        p: int | None = None,
        g: int | None = None,
        a: int | None = None,
        b: int | None = None,
        A: int | None = None,
        B: int | None = None,
        SA: int | None = None,
        SB: int | None = None
    ):
        self.p = p
        self.g = g
        self.a = a
        self.b = b
        self.A = A
        self.B = B
        self.SA = SA
        self.SB = SB

    @staticmethod
    def isNone(*NumsToCheck: int | None) -> bool:
        return any(num is None for num in NumsToCheck)

    @staticmethod
    def isPrime(*NumsToCheck: int | None) -> bool:
        """Check if all numbers are prime."""

        if not NumsToCheck:
            return False

        for num in NumsToCheck:
            if num is None or type(num) is not int or num < 2:
                return False

            for i in range(2, isqrt(num) + 1):
                if num % i == 0:
                    return False

        return True

    def getInput(
        self,
        message: str,
        checkPrime: bool = False
    ) -> int:
        value = self.convertToInt(input(message))

        if not self.checkInput(value, checkPrime=checkPrime):
            raise ValueError("Invalid Input!")

        return value

    @staticmethod
    def convertToInt(num: int | str) -> int:
        """Convert input to integer."""

        try:
            return int(num)
        except (ValueError, TypeError):
            raise ValueError("Not a Number!") from None

    def checkInput(
        self,
        *NumsToCheck: int | str | None,
        checkPrime: bool = False
    ) -> bool:
        """Validate input numbers."""

        if not NumsToCheck:
            return False

        for num in NumsToCheck:
            try:
                num = self.convertToInt(num)
            except ValueError:
                return False

            if num < 1:
                return False

            if checkPrime and not self.isPrime(num):
                return False

        return True

    def calcPublic(self, private: int) -> int:
        if self.isNone(self.p, self.g, private):
            raise ValueError("Invalid Input!")

        if self.p < 2 or self.g < 2 or private < 1:
            raise ValueError("Invalid Diffie-Hellman Parameters!")

        if self.g >= self.p:
            raise ValueError("Generator must be smaller than p!")

        return pow(self.g, private, self.p)

    def calcSharedSecret(self, person: str) -> int:
        if person.upper() == "A":
            if self.isNone(self.B, self.a, self.p):
                raise ValueError("Invalid Input!")
            return pow(self.B, self.a, self.p)
        elif person.upper() == "B":
            if self.isNone(self.A, self.b, self.p):
                raise ValueError("Invalid Input!")
            return pow(self.A, self.b, self.p)
        else:
            raise ValueError("Invalid Person!")

    def printMessage(self, message: str, color: str = "WHITE") -> None:
        color_code = self.COLORS.get(color.upper())

        if color_code is None:
            print(message)
            return

        print(f"{color_code}{message}{self.COLORS['WHITE']}")

    def main(self):
        try:
            self.p = self.getInput(
                "Please Enter a prime number, p:",
                checkPrime=True
            )

            self.g = self.getInput(
                "Please Enter a generator, g:"
            )

            self.a = self.getInput(
                "Please Enter Person A Private, a:"
            )

            self.b = self.getInput(
                "Please Enter Person B Private, b:"
            )

            self.printMessage("Inputs accepted!", "GREEN")

            self.printMessage("Calculating Person A Public...", "YELLOW")
            self.A = self.calcPublic(
                self.a
            )
            sleep(0.5)
            self.printMessage(f"Person A Public, A:{self.A}", "CYAN")

            self.printMessage("Calculating Person B Public...", "YELLOW")
            self.B = self.calcPublic(
                self.b
            )
            sleep(0.5)
            self.printMessage(f"Person B  Public, B:{self.B}", "CYAN")

            self.printMessage("Calculating Shared Secret...")
            self.SA = self.calcSharedSecret(
                "A"
            )
            self.SB = self.calcSharedSecret(
                "B"
            )
            sleep(0.5)
            self.printMessage(f"Shared Secret: {self.SA=} {self.SB=}", "CYAN")

        except ValueError as e:
            self.printMessage(str(e), "RED")


if __name__ == "__main__":
    dh = DiffieHellman()
    dh.main()