from .stolen.boneh_durfee import boneh_durfee_attack

class RSAKnife:
    def __init__(
        self, *,
        n=None, p=None, q=None, multiprime=None,
        e=None, d=None, phi=None
    ):
        n, p, q, e, d, phi = [
            ZZ(i) if i is not None else None
            for i in [n, p, q, e, d, phi]
        ]

        self.n = n
        self.p = p
        self.q = q
        self.multiprime = multiprime
        self.e = e
        self.d = d
        self.phi = phi

        self.process()

    def process(self):
        self.recover_pq_with_ed()
        self.recover_npq()
        self.recover_multiprime()
        self.recover_pqphi()
        self.recover_ed()

    def recover_pq_with_ed(self):
        n, p, q, e, d = self.n, self.p, self.q, self.e, self.d
        if not (
            n is not None and p is None and q is None and
            e is not None and d is not None
        ):
            return
        
        k = d * e - 1
        p, q = None, None
        for _ in range(1000):
            t = k
            g = randint(2, n - 1)

            while t % 2 == 0:
                t = t // 2
                x = ZZ(Zmod(n)(g) ^ t)
                if gcd(x - 1, n) > 1:
                    p = gcd(x - 1, n)
                    q = n // p

            if p is not None:
                break
        self.p, self.q = p, q

    def recover_npq(self):
        n, p, q = self.n, self.p, self.q
        npq_exists = (n is not None, p is not None, q is not None)
        if npq_exists == (True, True, True):
            assert n == p * q
        elif npq_exists == (True, True, False):
            q = n // p
        elif npq_exists == (True, False, True):
            p = n // q
        elif npq_exists == (False, True, True):
            n = p * q
        self.n, self.p, self.q = n, p, q

    def recover_multiprime(self):
        if self.multiprime is None:
            return
        multiprime = self.multiprime
        n, phi = 1, 1
        for p, x in multiprime:
            p, x = ZZ(p), ZZ(x)
            n = n * p ^ x
            phi = phi * (p - 1) * p ^ (x - 1)

        if self.n is None:
            self.n = n
        assert self.n == n
        if self.phi is None:
            self.phi = phi
        assert self.phi == phi

    def recover_pqphi(self):
        p, q, phi = self.p, self.q, self.phi
        pqphi_exists = (p is not None, q is not None, phi is not None)
        if pqphi_exists == (True, True, True):
            assert phi == (p - 1) * (q - 1)
        elif pqphi_exists == (True, True, False):
            phi = (p - 1) * (q - 1)
        elif pqphi_exists == (True, False, True):
            q = (phi // (p - 1)) + 1
        elif pqphi_exists == (False, True, True):
            p = (phi // (q - 1)) + 1
        self.p, self.q, self.phi = p, q, phi

        if self.phi is not None and self.n is not None:
            rnd = randint(1, self.n)
            assert Zmod(self.n)(rnd) ^ phi == 1

    def recover_ed(self):
        if self.phi is None:
            return
        e, d = self.e, self.d
        phi = self.phi
        ed_exists = (e is not None, d is not None)
        if ed_exists == (True, True):
            assert 1 == (e * d) % phi
        elif ed_exists == (True, False):
            d = ZZ(Zmod(phi)(1) / e)
        elif ed_exists == (False, True):
            e = ZZ(Zmod(phi)(1) / d)
        self.e, self.d = e, d

    def gen_d(self, e):
        assert self.phi is not None
        return ZZ(Zmod(self.phi)(1) / ZZ(e))

    def encrypt(self, pln):
        assert self.n is not None and self.e is not None
        return ZZ(Zmod(self.n)(ZZ(pln)) ^ self.e)
    
    def decrypt(self, enc):
        assert self.n is not None and self.d is not None
        return ZZ(Zmod(self.n)(ZZ(enc)) ^ self.d)

    def sign(self, pln):
        return self.decrypt(pln)

    def verify(self, pln, sig):
        return self.encrypt(sig) == pln

    def boneh_durfee(self, **kwargs):
        if self.d is not None:
            return
        d = boneh_durfee_attack(self.n, self.e, **kwargs)
        if d is not None:
            self.d = d
            self.process()
            return True
        return False