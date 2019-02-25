from solver import *
import queue


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
        # Mark current position as visited
        if self.currentState.state == self.victoryCondition: return True
        movables = self.gm.getMovables()
        if movables:
            if not self.currentState.children:
                for movable in movables:
                    self.gm.makeMove(movable)
                    updated_gs = self.gm.getGameState()
                    if self.currentState.parent and updated_gs == self.currentState.parent.state:
                        self.gm.reverseMove(movable)
                        continue
                    else:
                        valid_gs = GameState(updated_gs, self.currentState.depth + 1, movable)
                        valid_gs.parent = self.currentState
                        self.currentState.children.append(valid_gs)
                        self.gm.reverseMove(movable)
        if movables:
            if self.currentState.children:
                while True:
                    if not self.currentState.parent and self.currentState.nextChildToVisit == len(self.currentState.children):
                        break
                    if self.currentState.nextChildToVisit < len(self.currentState.children):
                        if self.currentState.children[self.currentState.nextChildToVisit] not in self.visited:
                            self.currentState = self.currentState.children[self.currentState.nextChildToVisit]
                            self.currentState.parent.nextChildToVisit = self.currentState.parent.nextChildToVisit + 1
                            self.visited[self.currentState] = True
                            self.gm.makeMove(self.currentState.requiredMovable)
                            break
                        else:
                            self.currentState.nextChildToVisit = self.currentState.nextChildToVisit + 1
                            continue
                    else:
                        self.gm.reverseMove(self.currentState.requiredMovable)
                        self.currentState = self.currentState.parent
                        continue

        if self.currentState.state == self.victoryCondition:
            return True
        else:
            return False


class SolverBFS(UninformedSolver):
    def __init__(self, gameMaster, victoryCondition):
        super().__init__(gameMaster, victoryCondition)

        self.bfs_queue = queue.Queue()

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

        self.visited[self.currentState] = True

        if self.currentState.state == self.victoryCondition: return True

        movables = self.gm.getMovables()

        if movables:
            if not self.currentState.children:
                for movable in movables:
                    self.gm.makeMove(movable)
                    updated_gs = self.gm.getGameState()
                    if self.currentState.parent and updated_gs == self.currentState.parent.state:
                        self.gm.reverseMove(movable)
                        continue
                    else:
                        valid_gs = GameState(updated_gs, self.currentState.depth + 1, movable)
                        valid_gs.parent = self.currentState
                        self.currentState.children.append(valid_gs)
                        self.bfs_queue.put(valid_gs)
                        self.gm.reverseMove(movable)

        queue_item = self.bfs_queue.get()

        while self.currentState.requiredMovable:
            self.gm.reverseMove(self.currentState.requiredMovable)
            self.currentState = self.currentState.parent

        movables = []
        while queue_item.requiredMovable:
            movables.append(queue_item.requiredMovable)
            queue_item = queue_item.parent

        while movables:
            move = movables.pop()
            self.gm.makeMove(move)
            updated_gs = self.gm.getGameState()

            for child in self.currentState.children:
                if child.state == updated_gs:
                    self.currentState = child
                    self.visited[self.currentState] = True
                    break

        else:
            print('------------------------' + str(self.gm.getGameState()) + '----------------------')
            return False
