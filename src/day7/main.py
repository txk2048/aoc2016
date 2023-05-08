import argparse
import itertools

from dataclasses import dataclass


@dataclass
class Address:
    supernets: list[str]
    hypernets: list[str]

    def from_str(s):
        supernets = []
        hypernets = []

        i = 0
        while i < len(s):
            # hypernet
            if s[i] == "[":
                j = s.find("]", i)
                hypernets.append(s[i + 1 : j])
                i = j + 1
            else:
                # supernet
                j = s.find("[", i)

                # no more hypernets
                if j == -1:
                    supernets.append(s[i:])
                    break

                # consume until hypernet
                else:
                    supernets.append(s[i:j])
                    i = j

        return Address(supernets, hypernets)

    def has_abba(self, s):
        for a, b, c, d in zip(s, s[1:], s[2:], s[3:]):
            if a == d and b == c and a != b:
                return True

        return False

    def supports_tls(self):
        for hypernet in self.hypernets:
            if self.has_abba(hypernet):
                return False

        for supernet in self.supernets:
            if self.has_abba(supernet):
                return True

        return False

    def supports_ssl(self):
        abas = []
        babs = []

        for supernet in self.supernets:
            for a, b, c in zip(supernet, supernet[1:], supernet[2:]):
                if a == c and a != b:
                    abas.append((a, b))

        for hypernet in self.hypernets:
            for a, b, c in zip(hypernet, hypernet[1:], hypernet[2:]):
                if a == c and a != b:
                    babs.append((a, b))

        return any(aba == bab[::-1] for aba, bab in itertools.product(abas, babs))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("input", help="input file")
    args = parser.parse_args()

    with open(args.input, "r") as f:
        addresses = [Address.from_str(line.strip()) for line in f]

    print(f"Part 1: {sum(address.supports_tls() for address in addresses)}")
    print(f"Part 2: {sum(address.supports_ssl() for address in addresses)}")


if __name__ == "__main__":
    main()
