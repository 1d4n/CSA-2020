import socket
import re
import time


class Node:
    def __init__(self, coord, parent=None):
        self.x = coord[0]
        self.y = coord[1]
        self.parent = parent

    def is_visited(self, stack):
        for visited in stack:
            if self.x == visited.x and self.y == visited.y:
                return True
        return False

    def get_adjacent(self, directions):
        # [l,r,u,d]
        adjacent = list()
        left = (self.x - 1, self.y)
        right = (self.x + 1, self.y)
        up = (self.x, self.y + 1)
        down = (self.x, self.y - 1)

        if directions[0]:
            adjacent.append(Node(left, self))
        if directions[1]:
            adjacent.append(Node(right, self))
        if directions[2]:
            adjacent.append(Node(up, self))
        if directions[3]:
            adjacent.append(Node(down, self))
        return adjacent


def send_msg(conn, msg):
    conn.send(msg.encode() + b'\n')
    response = conn.recv(128).decode('utf-8')
    conn.recv(128)
    return response


def get_options(conn):
    directions = send_msg(conn, 'i')
    opts = re.findall(r'\w=(\d)', directions)
    return list(map(int, opts))


def check_path(current, last):
    path = list()
    while current != last and last.parent:
        if last.x + 1 == last.parent.x:
            path.append('l')
        if last.x - 1 == last.parent.x:
            path.append('r')
        if last.y - 1 == last.parent.y:
            path.append('u')
        if last.y + 1 == last.parent.y:
            path.append('d')
        last = last.parent
    if last == current:
        return True, path
    return False, []


def backtrack(conn, current, last):
    good, path = check_path(current, last)
    while not good and current.parent:
        # Opposite direction
        if current.x + 1 == current.parent.x:
            send_msg(conn, 'r')
        elif current.x - 1 == current.parent.x:
            send_msg(conn, 'l')
        elif current.y + 1 == current.parent.y:
            send_msg(conn, 'u')
        elif current.y - 1 == current.parent.y:
            send_msg(conn, 'd')
        current = current.parent
        good, path = check_path(current, last)
    print(path)
    while len(path) > 0:
        send_msg(conn, path.pop())


def calculate(distance_squared, coord_list):
    sol_list = []
    x0, y0 = coord_list[0][0], coord_list[0][1]
    x1, y1 = coord_list[1][0], coord_list[1][1]
    x2, y2 = coord_list[2][0], coord_list[2][1]
    for x in range(250):
        for y in range(250):
            if distance_squared == (x - x0) ** 2 + (y - y0) ** 2 \
                    == (x - x1) ** 2 + (y - y1) ** 2 \
                    == (x - x2) ** 2 + (y - y2) ** 2:
                sol_list.append(f'({x}, {y})')
    return sol_list


def intro(conn):
    starting_point = (0, 0)
    msg = conn.recv(256)
    print(msg)
    while b"What" not in msg:
        msg = conn.recv(256)
        if b"starting position" in msg:
            coord = msg.decode('utf-8')
            starting_point = (int(re.search(r'\(([0-9]+),([0-9]+)\)', coord).group(1)),
                              int(re.search(r'\(([0-9]+),([0-9]+)\)', coord).group(2)))
        print(msg)
    return starting_point


def main(conn):
    start_time = time.time()
    stack = list()
    known = set()
    distances = dict()
    starting_coord = intro(conn)
    root = Node(starting_coord)
    current_point = root
    stack.append(current_point)

    while len(stack) > 0:
        current_point = stack.pop()
        g = send_msg(conn, 'g')
        print("\ncurrent:", "({}, {})".format(current_point.x, current_point.y))

        if "far" not in g:
            print("---------------")
            print(g)
            print("Total time:", round(time.time() - start_time), 'seconds.')
            print("current:", "({}, {})".format(current_point.x, current_point.y))
            print("---------------")
            distance = int(re.search(r"(\d+)", g).group(1))

            for val in distances.values():
                if len(val) > 2:
                    solutions = calculate(distance, val)
                    if len(solutions) > 0:
                        conn.send(b's\n')
                        s.recv(128)
                        print("sending the solution:", solutions[0])
                        conn.send(str.encode(solutions[0]) + b'\n')
                        print(conn.recv(1024).decode('utf-8'))  # the flag
                        input('press enter to exit')
                        conn.close()
                        break

            if distance in distances.keys():
                distances[distance].append((current_point.x, current_point.y))
            else:
                distances[distance] = [(current_point.x, current_point.y)]

        info = get_options(conn)
        print("directions", info)
        adjacents = current_point.get_adjacent(info)
        for adjacent in adjacents:
            if not adjacent.is_visited(known):
                print("adding:", f'({adjacent.x}, {adjacent.y})')
                known.add(adjacent)
                stack.append(adjacent)
        backtrack(conn, current_point, stack[-1])


if __name__ == '__main__':
    host, port = 'maze.csa-challenge.com', 80
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((host, port))
        main(s)
