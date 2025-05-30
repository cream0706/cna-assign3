import sys
from typing import Dict

INF = 10 ** 9

class Router:
    def __init__(self, name: str) -> None:
        self.name: str = name
        self.neigh: Dict[str, int] = {}
        self.table: Dict[str, tuple[int, str | None]] = {}

    def init_table(self, all_nodes):
        for dest in all_nodes:
            if dest == self.name:
                continue
            if dest in self.neigh:
                w = self.neigh[dest]
                self.table[dest] = (w, dest)
            else:
                self.table[dest] = (INF, None)

    def print_distance(self, t: int, all_nodes):
        header = " ".join(f"{d:>5}" for d in all_nodes if d != self.name)
        print(f"Distance Table of router {self.name} at t={t}:")
        print("    ", header)
        for via in all_nodes:
            if via == self.name:
                continue
            row = []
            for dest in all_nodes:
                if dest == self.name:
                    continue
                cost, nhop = self.table[dest]
                value = cost if nhop == via else INF
                row.append("INF" if value >= INF else str(value))
            print(f"{via:>3} ", " ".join(f"{c:>5}" for c in row))
        print()

def read_router_names(stdin) -> list[str]:
    names: list[str] = []
    for line in stdin:
        token = line.strip()
        if token == "START":
            break
        if token:
            names.append(token)
    return names

def read_links(stdin, routers: Dict[str, Router]):
    for line in stdin:
        line = line.strip()
        if line == "UPDATE":
            break
        if not line:
            continue
        u, v, w = line.split()
        w = int(w)
        if u not in routers:
            routers[u] = Router(u)
        if v not in routers:
            routers[v] = Router(v)
        if w != -1:
            routers[u].neigh[v] = w
            routers[v].neigh[u] = w
        else:
            routers[u].neigh.pop(v, None)
            routers[v].neigh.pop(u, None)

if __name__ == "__main__":
    router_names = read_router_names(sys.stdin)
    routers: Dict[str, Router] = {n: Router(n) for n in router_names}
    
    read_links(sys.stdin, routers)

    all_nodes = sorted(routers.keys())
    for r in routers.values():
        r.init_table(all_nodes)

    for name in all_nodes:
        routers[name].print_distance(t=0, all_nodes=all_nodes)
