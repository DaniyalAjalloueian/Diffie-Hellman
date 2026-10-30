import DiffieHellman as dh
diffieHellman = dh.DiffieHellman(p = 23, g = 5)
print(diffieHellman.calcPublic(6))