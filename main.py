import copy
import itertools

d = [3, 3, 2, 2, 2, 1, 1]
links = {}
unique_links_list = []


def validate_links():
    for k, v in links.items():
        if d[k] != len(v):
            return False
    return True


def is_unique():
    default_permutation = []
    for i in range(len(d)):
        default_permutation.append(i)

    arrangements = list(itertools.permutations(range(len(d))))

    for unique_links in unique_links_list:
        for arrangement in arrangements:
            curr_graph = copy.deepcopy(links)
            was_replaced_earlier = []
            for i in range(len(d)):
                if i != arrangement[i] and i not in was_replaced_earlier:
                    replace_in_graph(curr_graph, i, arrangement[i])
                    was_replaced_earlier.append(arrangement[i])
            if curr_graph == unique_links:
                return False
    unique_links_list.append(copy.deepcopy(links))
    return True


def replace_in_graph(graph, a, b):
    for k, v in graph.items():
        if a in graph[k] and b in graph[k]:
            continue
        elif a in graph[k]:
            graph[k].remove(a)
            graph[k].add(b)
        elif b in graph[k]:
            graph[k].remove(b)
            graph[k].add(a)
    graph[a], graph[b] = graph[b], graph[a]


def connect(a, b):
    links[a].add(b)
    links[b].add(a)


def disconnect(a, b):
    links[a].remove(b)
    links[b].remove(a)


def gen_variants(u, conns, variants):
    if len(conns) + len(links[u]) >= d[u]:
        variants.append(conns.copy())
    else:
        conns_copy = conns.copy()
        last_element = -1 if len(conns) == 0 else conns[-1]
        for v in range(last_element+1, len(d)):
            if v != u and v not in links[u]:
                conns_copy.append(v)
                gen_variants(u, conns_copy, variants)
                conns_copy.pop()

visited = set()


def iterate(curr):
    visited_was_empty = len(visited) == 0
    variants = []
    gen_variants(curr, [], variants)
    for variant in variants:
        for vertex in variant:
            connect(curr, vertex)
            iterate(vertex)

        for i in range(len(d)):
            if is_connected(curr, i, set()):
                visited.add(i)

        for i in range(len(d)):
            if i not in visited:
                iterate(i)
        if visited_was_empty:
            visited.clear()

        if validate_links() and is_unique():
            print(links)

        for vertex in variant:
            disconnect(curr, vertex)


def is_connected(a, b, visited):
    visited.add(a)
    if a == b:
        return True
    for vertex in links[a]:
        if vertex not in visited:
            if is_connected(vertex, b, visited):
                return True

    return False

def setup():
    for i in range(len(d)):
        links[i] = set()

if __name__ == '__main__':
    setup()
    iterate(0)
