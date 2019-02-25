from solver import *
from queue import *


class SolverDFS(UninformedSolver):
    def __init__(self, gameMaster, victoryCondition):
        super().__init__(gameMaster, victoryCondition)

    def solveOneStep(self):
        """
        Go to the next state that has not been explored. If a
        game state leads to more than one unexplored game states,
        explore in the order implied by the GameMaster.getMovables()
        function.
        If all game states reachable from a parent state has been explored,
        the next explored state should conform to the specifications of
        the Depth-First Search algorithm.
        Returns:
            True if the desired solution state is reached, False otherwise
        """
        # Get list of all movables
        movables = self.gm.getMovables()
        # print(str(movables))

        # From piazza bug; return True to avoid going into more states
        if self.currentState.state == self.victoryCondition: return True

        # If you have reached the limit w/ no more nodes, need to iterate through movables
        if not self.currentState.children:

            for movable in movables:
                # print(str(movable))

                self.gm.makeMove(movable)

                updated_gs = self.gm.getGameState()

                if self.currentState.parent:
                    if updated_gs == self.currentState.parent.state:
                        self.gm.reverseMove(movable)
                    else:
                        new_depth = 1 + self.currentState.depth
                        valid_gs = GameState(updated_gs, new_depth, movable)
                        valid_gs.parent = self.currentState
                        self.currentState.children.append(valid_gs)
                        self.gm.reverseMove(movable)

                else:
                    new_depth = 1 + self.currentState.depth
                    valid_gs = GameState(updated_gs, new_depth, movable)
                    valid_gs.parent = self.currentState
                    self.currentState.children.append(valid_gs)
                    self.gm.reverseMove(movable)

        # If there are still nodes, explore them
        if self.currentState.children:

            while movables and True:

                if self.currentState.nextChildToVisit < len(self.currentState.children):
                    if self.currentState.children[self.currentState.nextChildToVisit] not in self.visited:

                        self.currentState = self.currentState.children[self.currentState.nextChildToVisit]
                        self.visited[self.currentState] = True
                        self.currentState.parent.nextChildToVisit = 1 + self.currentState.parent.nextChildToVisit
                        self.gm.makeMove(self.currentState.requiredMovable)
                        break

                    else:
                        self.currentState.nextChildToVisit = 1 + self.currentState.nextChildToVisit
                else:
                    self.gm.reverseMove(self.currentState.requiredMovable)
                    self.currentState = self.currentState.parent

        if self.currentState.state == self.victoryCondition:
            return True
        else:
            print('------------------------' + str(self.gm.getGameState()) + '----------------------')
            return False


class SolverBFS(UninformedSolver):
    def __init__(self, gameMaster, victoryCondition):
        super().__init__(gameMaster, victoryCondition)

        self.bfs_queue = Queue()
        self.todo_movables = []

    def solveOneStep(self):
        """
        Go to the next state that has not been explored. If a
        game state leads to more than one unexplored game states,
        explore in the order implied by the GameMaster.getMovables()
        function.
        If all game states reachable from a parent state has been explored,
        the next explored state should conform to the specifications of
        the Breadth-First Search algorithm.
        Returns:
            True if the desired solution state is reached, False otherwise
        """

        self.todo_movables.clear()

        self.visited[self.currentState] = True

        if self.currentState.state == self.victoryCondition: return True

        movables = self.gm.getMovables()

        if movables:

            if not self.currentState.children:

                for movable in movables:
                    self.gm.makeMove(movable)
                    updated_gs = self.gm.getGameState()

                    if self.currentState.parent:
                        if updated_gs != self.currentState.parent.state:
                            new_depth = 1 + self.currentState.depth
                            valid_gs = GameState(updated_gs, new_depth, movable)
                            valid_gs.parent = self.currentState
                            self.currentState.children.append(valid_gs)
                            self.bfs_queue.put(valid_gs)
                        self.gm.reverseMove(movable)

                    else:
                        new_depth = 1 + self.currentState.depth
                        valid_gs = GameState(updated_gs, new_depth, movable)
                        valid_gs.parent = self.currentState
                        self.currentState.children.append(valid_gs)
                        self.bfs_queue.put(valid_gs)
                        self.gm.reverseMove(movable)

        queue_item = self.bfs_queue.get()

        while self.currentState.requiredMovable:
            self.gm.reverseMove(self.currentState.requiredMovable)
            self.currentState = self.currentState.parent

        while queue_item.requiredMovable:
            self.todo_movables.append(queue_item.requiredMovable)
            queue_item = queue_item.parent

        while self.todo_movables:
            self.gm.makeMove(self.todo_movables.pop())
            updated_gs = self.gm.getGameState()

            for child in self.currentState.children:
                if child.state == updated_gs:
                    self.currentState = child
                    self.visited[self.currentState] = True

        else:
            print('------------------------' + str(self.gm.getGameState()) + '----------------------')
            return False
