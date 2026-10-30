
from time import sleep
from secrets import randbits, randbelow


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
        q: int | None = None,
        g: int | None = None,
        a: int | None = None,
        b: int | None = None,
        A: int | None = None,
        B: int | None = None,
        SA: int | None = None,
        SB: int | None = None
    ):
        self.p = p
        self.q = q
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
    def isPrime(*NumsToCheck: int | None, k: int = 16) -> bool:
        """Check whether all given numbers are probably prime using Miller-Rabin."""

        if not NumsToCheck or k < 1:
            return False

        smallPrimes = (
            2, 3, 5, 7, 11, 13, 17, 19, 23, 29,
            31, 37, 41, 43, 47, 53, 59, 61, 67, 71,
            73, 79, 83, 89, 97
        )

        for n in NumsToCheck:
            if type(n) is not int or n < 2:
                return False

            for prime in smallPrimes:
                if n == prime:
                    break

                if n % prime == 0:
                    return False
            else:
                d = n - 1
                s = 0

                while d % 2 == 0:
                    d //= 2
                    s += 1

                for _ in range(k):
                    a = randbelow(n - 3) + 2
                    x = pow(a, d, n)

                    if x == 1 or x == n - 1:
                        continue

                    for _ in range(s - 1):
                        x = pow(x, 2, n)

                        if x == n - 1:
                            break
                    else:
                        return False

        return True

    def generateSafePrime(self) -> int:
        while True:
            q = randbits(511) | (1 << 510) | 1
            p = (q * 2) + 1

            if self.isPrime(q) and self.isPrime(p):
                self.q = q
                return p

    def generateGenerator(self) -> int:
        if self.isNone(self.p, self.q):
            raise ValueError("p and q must be initialized!")

        while True:
            h = randbelow(self.p - 3) + 2
            g = pow(h, 2, self.p)

            if g != 1:
                return g

    def generatePrivateKey(self) -> int:
        if self.q is None or self.q < 5:
            raise ValueError("Invalid q!")

        return randbelow(self.q - 3) + 2

    def getInput(
        self,
        message: str,
        generator=None
    ) -> int:
        value = input(message).strip()

        if value == "":
            if generator is None:
                raise ValueError("Empty input is not allowed!")

            return generator()

        value = self.convertToInt(value)

        if not self.checkInput(value):
            raise ValueError("Invalid input!")

        return value

    @staticmethod
    def convertToInt(num: int | str) -> int:
        try:
            return int(num)
        except (ValueError, TypeError):
            raise ValueError("Input must be a valid integer!") from None

    def checkInput(self, *NumsToCheck: int | str | None) -> bool:
        if not NumsToCheck:
            return False

        for num in NumsToCheck:
            try:
                num = self.convertToInt(num)
            except ValueError:
                return False

            if num < 1:
                return False

        return True

    def calcPublic(self, private: int) -> int:
        if self.isNone(self.p, self.g, private):
            raise ValueError("Invalid input!")

        if self.p < 2 or not 2 <= self.g < self.p or private < 1:
            raise ValueError("Invalid Diffie-Hellman parameters!")

        return pow(self.g, private, self.p)

    def calcSharedSecret(self, person: str) -> int:
        if person.upper() == "A":
            if self.isNone(self.B, self.a, self.p):
                raise ValueError("Invalid input!")

            return pow(self.B, self.a, self.p)

        if person.upper() == "B":
            if self.isNone(self.A, self.b, self.p):
                raise ValueError("Invalid input!")

            return pow(self.A, self.b, self.p)

        raise ValueError("Invalid person!")

    def printMessage(self, message: str, color: str = "WHITE") -> None:
        color_code = self.COLORS.get(color.upper())

        if color_code is None:
            print(message)
            return

        print(f"{color_code}{message}{self.COLORS['WHITE']}")

    def main(self):
        self.printMessage(
            "Leave Empty to auto generate parameters!",
            "YELLOW"
        )

        try:
            self.p = self.getInput(
                "Enter the public prime modulus (p): ",
                self.generateSafePrime
            )

            self.g = self.getInput(
                "Enter the public generator (g): ",
                self.generateGenerator
            )

            self.a = self.getInput(
                "Enter Person A's private key (a): ",
                self.generatePrivateKey
            )

            self.b = self.getInput(
                "Enter Person B's private key (b): ",
                self.generatePrivateKey
            )

            self.printMessage("All parameters have been accepted.", "GREEN")

            self.printMessage("Calculating Person A's public key...", "YELLOW")
            self.A = self.calcPublic(self.a)
            sleep(0.5)
            self.printMessage(f"Person A's public key (A): {self.A}", "CYAN")

            self.printMessage("Calculating Person B's public key...", "YELLOW")
            self.B = self.calcPublic(self.b)
            sleep(0.5)
            self.printMessage(f"Person B's public key (B): {self.B}", "CYAN")

            self.printMessage("Calculating the shared secret...", "YELLOW")
            self.SA = self.calcSharedSecret("A")
            self.SB = self.calcSharedSecret("B")
            sleep(0.5)

            self.printMessage(
                f"Shared secrets:\nPerson A = {self.SA}\nPerson B = {self.SB}",
                "CYAN"
            )

            if self.SA == self.SB:
                self.printMessage("Shared secrets match!", "GREEN")
            else:
                self.printMessage("Shared secrets do not match!", "RED")

        except ValueError as e:
            self.printMessage(str(e), "RED")


if __name__ == "__main__":
    dh = DiffieHellman()
    dh.main()
