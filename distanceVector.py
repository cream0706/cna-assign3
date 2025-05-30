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

    def send_vector(self) -> dict[str, int]:
        return {d: c for d, (c, _) in self.table.items()}

    def update_from_neigh(self, neighbour: str, neigh_vector: dict[str, int]) -> bool:
        updated = False
        w_uv = self.neigh[neighbour]
        for dest, cost_v_to_dest in neigh_vector.items():
            if dest == self.name:
                continue
            new_cost = w_uv + cost_v_to_dest if cost_v_to_dest < INF else INF
            cur_cost, cur_nhop = self.table.get(dest, (INF, None))
            if (new_cost < cur_cost) or (
                new_cost == cur_cost and neighbour < (cur_nhop or "~")
            ):
                self.table[dest] = (new_cost, neighbour if new_cost < INF else None)
                updated = True
        return updated

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

    def print_routing(self, all_nodes):
        print(f"Routing Table of router {self.name}:")
        for dest in all_nodes:
            if dest == self.name:
                continue
            cost, nhop = self.table[dest]
            if cost >= INF:
                print(f"{dest},INF,INF")
            else:
                print(f"{dest},{nhop},{cost}")
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

def simulate(routers: Dict[str, Router]):
    all_nodes = sorted(routers.keys())
    t = 0
    for name in all_nodes:
        routers[name].print_distance(t, all_nodes)

    while True:
        vectors = {name: r.send_vector() for name, r in routers.items()}
        changed_any = False
        for name, r in routers.items():
            for neigh in r.neigh:
                if r.update_from_neigh(neigh, vectors[neigh]):
                    changed_any = True
        if not changed_any:
            break
        t += 1
        for name in all_nodes:
            routers[name].print_distance(t, all_nodes)

    for name in all_nodes:
        routers[name].print_routing(all_nodes)

if __name__ == "__main__":
    router_names = read_router_names(sys.stdin)
    routers: Dict[str, Router] = {n: Router(n) for n in router_names}
    
    read_links(sys.stdin, routers)

    all_nodes = sorted(routers.keys())
    for r in routers.values():
        r.init_table(all_nodes)

    #for name in all_nodes:
    #    routers[name].print_distance(t=0, all_nodes=all_nodes)

    simulate(routers)
