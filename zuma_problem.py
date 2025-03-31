import search
import utils

ids = ["No numbers - I'm special!"]

""" Constants representing ball colors """
RED = 1
BLUE = 2
YELLOW = 3
GREEN = 4
COLORS = [RED, BLUE, YELLOW, GREEN]


class ZumaProblem(search.Problem):
    """This class implements the Zuma problem for solving."""

    def __init__(self, initial):
        search.Problem.__init__(self, initial)

    def successor(self, state):
        successors = []
        line, ammo = state

        if not ammo:
            # No ammo left; no actions can be performed
            return successors

        current_ball = ammo[0]
        ammo_rest = ammo[1:]

        positions = self.find_positions_for_ball(line, current_ball)

        if positions:
            # There is at least one group of the same color
            # Possible actions: Insert current_ball at positions found
            for pos in positions:
                new_line = list(line)
                new_line.insert(pos, current_ball)
                # Process the new line to handle eliminations
                processed_line = self.process_line(new_line)
                new_line_tuple = tuple(processed_line)
                new_state = (new_line_tuple, ammo_rest)
                action = ("Insert", pos)
                successors.append((action, new_state))

        # Discard action: Discard the current ammo ball
        new_state = (line, ammo_rest)
        action = "Discard"
        successors.append((action, new_state))

        return successors

    def process_line(self, line):
        """
        Process the line to eliminate groups of 3 or more consecutive balls of the same color.
        Handles chain reactions resulting from eliminations.
        """
        while True:
            found = False
            index = 0
            while index < len(line):
                color = line[index]
                count = 1
                # Count consecutive balls of the same color
                while index + count < len(line) and line[index + count] == color:
                    count += 1
                if count >= 3:
                    # Remove the group of balls
                    del line[index:index + count]
                    found = True
                    break  # Restart after modification
                else:
                    index += count  # Skip over this group
            if not found:
                break  # No more groups to remove
        return line

    def find_positions_for_ball(self, line, ball):
        """
        Find positions where inserting the ball could affect groups of the same color.
        Returns positions adjacent to groups of the same color.
        """
        positions = set()
        line_length = len(line)
        index = 0
        while index < line_length:
            current_color = line[index]
            count = 1
            # Count consecutive balls of the same color
            while index + count < line_length and line[index + count] == current_color:
                count += 1
            if current_color == ball:
                # Positions before and after the group
                if index > 0:
                    positions.add(index)
                if index + count <= line_length:
                    positions.add(index + count)
                # Middle positions within the group
                for pos in range(index + 1, index + count):
                    positions.add(pos)
            index += count  # Move to the next group
        return positions if positions else None

    def count_groups(self, line):
        """
        Count the number of groups of 1 or 2 balls of the same color in the line.
        """
        if not line:
            return 0
        groups = 0
        index = 0
        line_length = len(line)
        while index < line_length:
            count = 1
            while index + count < line_length and line[index + count] == line[index]:
                count += 1
            if count <= 2:
                groups += 1
            index += count
        return groups

    def goal_test(self, state):
        """
        Return True if the current state is a goal (line is empty); otherwise, False.
        """
        line, ammo = state
        return len(line) == 0

    def h(self, node):
        """
        Heuristic function that returns the minimal number of groups (of 1 or 2 balls)
        remaining in the line after shooting the earliest ammo ball that can be inserted
        into a group of the same color. If the current ammo ball cannot be inserted
        into any group (no group of the same color), we simulate discarding it and consider
        the next ammo ball.
        """
        line, ammo = node.state
        if not line:
            return 0  # Goal state reached

        min_groups = float('inf')
        ammo_index = 0

        while ammo_index < len(ammo):
            ball = ammo[ammo_index]
            positions = self.find_positions_for_ball(line, ball)
            if positions:
                # There is at least one group of the same color
                for pos in positions:
                    new_line = list(line)
                    new_line.insert(pos, ball)
                    processed_line = self.process_line(new_line)
                    groups = self.count_groups(processed_line)
                    if groups < min_groups:
                        min_groups = groups
                break  # Stop after considering the first ammo ball that can be inserted
            else:
                # No group of the same color; simulate discarding the ball
                ammo_index += 1  # Move to the next ammo ball

        if min_groups == float('inf'):
            # No possible insertions with any ammo ball; return the current number of groups
            return self.count_groups(line)
        else:
            return min_groups


def create_zuma_problem(game):
    """
    Create a Zuma problem instance based on the provided game state.
    game: A tuple containing:
        - The initial line of balls (tuple of integers).
        - The queue of balls to shoot (tuple of integers).
    """
    return ZumaProblem(game)