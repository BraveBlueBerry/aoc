with open("input.txt", "r") as file:
    connected_computers = [tuple(line.strip().split('-')) for line in file]

computer_connections = dict()

for pair in connected_computers:
    # if pair[0].startswith('t'):
    computer_connections.setdefault(pair[0], set()).add(pair[1])
    # if pair[1].startswith('t'):
    computer_connections.setdefault(pair[1], set()).add(pair[0])

class three_way:
    connection : set

    def __init__(self, pc1, pc2, pc3):
        self.connection = set(sorted([pc1, pc2, pc3]))

    def __eq__(self, other):
        if isinstance(other, three_way):
            if len(other.connection) is not len(self.connection):
                return False
            for x in other.connection:
                if x not in self.connection:
                    return False
            return True
        if isinstance(other, set|list):
            if len(other) is not len(self.connection):
                return False
            for x in other:
                if x not in self.connection:
                    return False
            return True
        return False

    def __hash__(self):
        return hash("".join(self.connection))

    def __repr__(self):
        return " ".join(self.connection)



all_three_ways = set()

for pc in computer_connections:
    if pc.startswith('t'):
        for connected_pc in computer_connections[pc]:
            for that_connection in computer_connections[connected_pc]:
                if that_connection in computer_connections[pc]:
                    three_way_connection = three_way(pc, that_connection, connected_pc)
                    all_three_ways.add(three_way_connection)


print(len(all_three_ways))

