from collections import Counter

from ..chef import CK

class RSAKnife:
    def __init__(
        self, *,
        n=None, p=None, q=None, multiprime=None,
        e=None, d=None, phi=None, auto=True
    ):
        n, p, q, e, d, phi = [
            ZZ(i) if i is not None else None
            for i in [n, p, q, e, d, phi]
        ]

        if multiprime is not None:
            assert isinstance(multiprime, (tuple, list))
            if isinstance(multiprime[0], (tuple, list)):
                assert all([len(i) == 2 for i in multiprime])
            else:
                multiprime = [ ZZ(i) for i in multiprime ]
                multiprime = list(Counter(multiprime).items())

        self.n = n
        self.p = p
        self.q = q
        self.multiprime = multiprime
        self.e = e
        self.d = d
        self.phi = phi

        self.dirty = False

        if auto:
            self.npq()
            self.pqphi()
            self.ed_from_phi()
            self.pq_from_ed()

    def encrypt(self, pln):
        assert self.n is not None and self.e is not None
        return ZZ(Zmod(self.n)(ZZ(pln)) ^ self.e)
    
    def decrypt(self, enc):
        assert self.n is not None and self.d is not None
        return ZZ(Zmod(self.n)(ZZ(enc)) ^ self.d)

    def decrypt_bytes(self, enc):
        pln = self.decrypt(enc)
        return CK.init_int(int(pln)).into_bytes()

    def sign(self, pln):
        return self.decrypt(pln)

    def verify(self, pln, sig):
        return self.encrypt(sig) == pln
    
    def npq(self):
        if self.n is not None and self.p is not None and (self.q is None):
            self.q = self.n // self.p
            assert self.n == self.p * self.q

        if self.n is not None and (self.p is None) and self.q is not None:
            self.p = self.n // self.q
            assert self.n == self.p * self.q

        if (self.n is None) and self.p is not None and self.q is not None:
            self.n = self.p * self.q
            assert self.n == self.p * self.q

        return self

    def pqphi(self):
        if self.p is not None and self.q is not None and (self.phi is None):
            self.phi = (self.p-1) * (self.q-1)
            assert self.phi == (self.p-1) * (self.q-1)

        if self.p is not None and (self.q is None) and self.phi is not None :
            self.q = (self.phi // (self.p-1)) + 1
            assert self.phi == (self.p-1) * (self.q-1)
        
        if (self.p is None) and self.q is not None and self.phi is not None:
            self.p = (self.n // (self.q-1)) + 1
            assert self.phi == (self.p-1) * (self.q-1)

        return self

    def multiprime(self):
        if self.multiprime is None:
            return self

        n, phi = 1, 1
        for p, x in self.multiprime:
            p, x = ZZ(p), ZZ(x)
            n = n * p ^ x
            phi = phi * (p - 1) * p ^ (x - 1)

        self.n, self.phi = n, phi
        
        return self

    def ed_from_phi(self):
        if self.phi is None:
            return self

        if self.e is not None and self.d is None:
            self.d = ZZ(Zmod(self.phi)(self.e) ^ -1)
            assert (self.e * self.d) % self.phi == 1

        if self.e is None and self.d is not None:
            self.e = ZZ(Zmod(self.phi)(self.d) ^ -1)
            assert (self.e * self.d) % self.phi == 1

        return self

    def pq_from_ed(self, iters=1000):
        n, p, q, e, d = self.n, self.p, self.q, self.e, self.d
        if not (
            n is not None and p is None and q is None and
            e is not None and d is not None
        ):
            return self

        Fn = Zmod(n)
        p, q = None, None

        k = d * e - 1

        r = k
        t = 0
        while r % 2 == 0:
            r = r // 2
            t += 1

        for _ in range(iters):
            g = randint(2, n - 1)

            y = Fn(g) ^ r
            if y == 1 or y == Fn(-1):
                continue

            for j in range(1, t):
                x = y ^ 2

                if x == 1:
                    self.p = ZZ(gcd(y-1, n))
                    self.q = n // self.p
                    return self
                
                if x == Fn(-1):
                    break

        raise ValueError("Prime factors not found")