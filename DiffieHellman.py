
from time import sleep
from secrets import randbits


class DiffieHellman:
    COLORS: dict[str, str] = {
        "RED": "\033[91m",
        "GREEN": "\033[92m",
        "YELLOW": "\033[93m",
        "PURPLE": "\033[95m",
        "CYAN": "\033[96m",
        "WHITE": "\033[m"
    }

    # RFC 7919 - FFDHE2048
    P_HEX = (
        "FFFFFFFFFFFFFFFFADF85458A2BB4A9AAFDC5620273D3CF1"
        "D8B9C583CE2D3695A9E13641146433FBCC939DCE249B3EF9"
        "7D2FE363630C75D8F681B202AEC4617AD3DF1ED5D5FD6561"
        "2433F51F5F066ED0856365553DED1AF3B557135E7F57C935"
        "984F0C70E0E68B77E2A689DAF3EFE8721DF158A136ADE735"
        "30ACCA4F483A797ABC0AB182B324FB61D108A94BB2C8E3FB"
        "B96ADAB760D7F4681D4F42A3DE394DF4AE56EDE76372BB19"
        "0B07A7C8EE0A6D709E02FCE1CDF7E2ECC03404CD28342F61"
        "9172FE9CE98583FF8E4F1232EEF28183C3FE3B1B4C6FAD73"
        "3BB5FCBC2EC22005C58EF1837D1683B2C6F34A26C1B2EFFA"
        "886B423861285C97FFFFFFFFFFFFFFFF"
    )

    def __init__(self):
        self.p = int(self.P_HEX, 16)
        self.q = (self.p - 1) // 2
        self.g = 2

        self.a = None
        self.b = None
        self.A = None
        self.B = None
        self.SA = None
        self.SB = None

    def generatePrivateKey(self) -> int:
        # RFC 7919 recommends at least 225-bit private exponents.
        return randbits(256) | (1 << 255)

    def calcPublic(self, private: int) -> int:
        if not 2 <= private < self.q:
            raise ValueError("Invalid private key!")

        return pow(self.g, private, self.p)

    def calcSharedSecret(self, public: int, private: int) -> int:
        if not 1 < public < self.p - 1:
            raise ValueError("Invalid public key!")

        return pow(public, private, self.p)

    def printMessage(self, message: str, color: str = "WHITE") -> None:
        color_code = self.COLORS.get(color.upper(), self.COLORS["WHITE"])
        print(f"{color_code}{message}{self.COLORS['WHITE']}")

    def main(self):
        try:
            self.printMessage("Using RFC 7919 FFDHE2048 parameters", "YELLOW")

            self.printMessage(f"p size: {self.p.bit_length()} bits", "CYAN")
            self.printMessage(f"q size: {self.q.bit_length()} bits", "CYAN")
            self.printMessage(f"Generator: {self.g}", "CYAN")

            self.printMessage("Generating private keys...", "YELLOW")

            self.a = self.generatePrivateKey()
            self.b = self.generatePrivateKey()

            self.printMessage("Private keys generated.", "GREEN")

            self.printMessage("Calculating public keys...", "YELLOW")

            self.A = self.calcPublic(self.a)
            self.B = self.calcPublic(self.b)

            sleep(0.2)

            self.printMessage(f"Person A public key: {self.A}", "CYAN")
            self.printMessage(f"Person B public key: {self.B}", "CYAN")

            self.printMessage("Calculating shared secrets...", "YELLOW")

            self.SA = self.calcSharedSecret(self.B, self.a)
            self.SB = self.calcSharedSecret(self.A, self.b)

            sleep(0.2)

            if self.SA == self.SB:
                self.printMessage("Shared secrets match!", "GREEN")
            else:
                self.printMessage("Shared secrets do not match!", "RED")

        except ValueError as e:
            self.printMessage(str(e), "RED")


if __name__ == "__main__":
    dh = DiffieHellman()
    dh.main()