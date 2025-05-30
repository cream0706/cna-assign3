import sys
from typing import Dict

INF = 10 ** 9


class Router:
    def __init__(self, name: str) -> None:
        self.name: str = name
        self.neigh: Dict[str, int] = {}
        self.table: Dict[str, tuple[int, str | None]] = {}

    def __repr__(self) -> str:
        return f"Router({self.name})"


def read_router_names(stdin) -> list[str]:
    names: list[str] = []
    for line in stdin:
        token = line.strip()
        if token == "START":
            break
        if token:
            names.append(token)
    return names


if __name__ == "__main__":
    router_names = read_router_names(sys.stdin)
    routers: Dict[str, Router] = {n: Router(n) for n in router_names}

    print("Routers detected:", ", ".join(sorted(routers)))
