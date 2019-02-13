import unittest, inspect
from multiprocessing.pool import ThreadPool
from multiprocessing.context import TimeoutError
from student_code_game_masters import *
from student_code_uninformed_solvers import *


class KBTest(unittest.TestCase):

    def setUp(self):
        self.pool = ThreadPool(processes=1)
        self.lastEndStep = 0

    def playXSteps(self, solver, plays):
        """
        Call the solver's solveOneStep for x times, and record the result game state

        Args:
             solver: solver of the game
             plays: list of lists; inner list consists of the number of steps (x) followed by the expected outcome
        """
        res = []
        for play in plays:
            x = play[0]
            while self.lastEndStep < x:
                solver.solveOneStep()
                self.lastEndStep += 1
            res.append(solver.gm.getGameState())
        return res

    def solve(self, solver):
        """
        Call the solver's solve function, which should solve the game.

        Args:
             solver: solver of the game
        """
        solver.solve()

    def runPlayXSteps(self, solver, plays, timeout=5):
        """
        Wrapper function; calls playXSteps(..) with a timeout

        Args:
             solver: solver of the game
             plays: list of lists; inner list consists of the number of steps (x) followed by the expected outcome
             timeout: time out in seconds. Default 5 seconds
        """
        try:
            results = self.pool.apply_async(self.playXSteps, [solver, plays]).get(timeout)
            for index, play in enumerate(plays):
                expected = play[1]
                self.assertEqual(results[index], expected)
        except TimeoutError:
            raise Exception("Timed out: %s" % inspect.stack()[1][3])

    def runSolve(self, solver, timeout=5):
        """
        Wrapper function; calls solve(..) with a timeout

        Args:
             solver: solver of the game
             timeout: time out in seconds. Default 5 seconds
        """
        try:
            self.pool.apply_async(self.solve, [solver,]).get(timeout)
            self.assertTrue(solver.gm.isWon())
        except TimeoutError:
            raise Exception("Timed out: %s" % inspect.stack()[1][3])

    # Tests TOH game masters with 3 disks on peg 1
    def test01_GM_Hanoi(self):
        print("-------------------------------TEST ONE-------------------------------")
        th = TowerOfHanoiGame()
        th.read('hanoi_3_all_disks_on_peg_one.txt')
        required = [
            'fact: (movable disk1 peg3 peg1)',
            'fact: (movable disk1 peg3 peg2)',
        ]
        th.setWinningCondition(required, 'hanoi_all_forbidden.txt')
        self.assertFalse(th.isWon())

        movables = th.getMovables()
        self.assertEqual(th.getGameState(), ((1,2,3),(),()))
        th.makeMove(movables[0])
        self.assertEqual(th.getGameState(), ((2,3),(1,),()))
        th.reverseMove(movables[0])
        self.assertEqual(th.getGameState(), ((1,2,3),(),()))

    # Tests TOH game masters with 2 disks on peg 2 and 1 disk on peg 3
    def test09_GM_Hanoi(self):
        print("-------------------------------TEST 9-------------------------------")
        th = TowerOfHanoiGame()
        th.read('hanoi_3_two_disks_one_disk.txt')
        required = [
            'fact: (movable disk1 peg3 peg1)',
            'fact: (movable disk1 peg3 peg2)',
        ]
        th.setWinningCondition(required, 'hanoi_all_forbidden.txt')
        self.assertFalse(th.isWon())

        movables = th.getMovables()
        self.assertEqual(th.getGameState(), ((),(2,3),(1,)))
        th.makeMove(movables[1])
        self.assertEqual(th.getGameState(), ((1,), (2, 3), ()))
        th.reverseMove(movables[1])
        self.assertEqual(th.getGameState(), ((), (2, 3), (1,)))

    # Tests TOH game masters with 2 disks on peg 2 and 1 disk on peg 3
    def test010_GM_Hanoi(self):
        print("-------------------------------TEST 10-------------------------------")
        th = TowerOfHanoiGame()
        th.read('hanoi_3_two_disks_one_disk.txt')
        required = [
            'fact: (movable disk1 peg3 peg1)',
            'fact: (movable disk1 peg3 peg2)',
        ]
        th.setWinningCondition(required, 'hanoi_all_forbidden.txt')
        self.assertFalse(th.isWon())

        movables = th.getMovables()
        self.assertEqual(th.getGameState(), ((),(2,3),(1,)))
        th.makeMove(movables[2])
        self.assertEqual(th.getGameState(), ((), (1, 2, 3), ()))
        th.reverseMove(movables[2])
        self.assertEqual(th.getGameState(), ((), (2, 3), (1,)))

    # Tests TOH game masters with 2 disks on peg 2 and 1 disk on peg 3
    def test011_GM_Hanoi(self):
        print("-------------------------------TEST 11-------------------------------")
        th = TowerOfHanoiGame()
        th.read('hanoi_3_two_disks_one_disk.txt')
        required = [
            'fact: (movable disk1 peg3 peg1)',
            'fact: (movable disk1 peg3 peg2)',
        ]
        th.setWinningCondition(required, 'hanoi_all_forbidden.txt')
        self.assertFalse(th.isWon())

        movables = th.getMovables()
        self.assertEqual(th.getGameState(), ((),(2,3),(1,)))
        th.makeMove(movables[0])
        self.assertEqual(th.getGameState(), ((2,), (3,), (1,)))
        th.reverseMove(movables[0])
        self.assertEqual(th.getGameState(), ((), (2, 3), (1,)))

    def test02_DFS_Hanoi(self):
        print("-------------------------------TEST TWO-------------------------------")
        th = TowerOfHanoiGame()
        th.read('hanoi_3_two_disks_one_disk.txt')
        required = [
            'fact: (movable disk1 peg3 peg1)',
            'fact: (movable disk1 peg3 peg2)',
        ]
        th.setWinningCondition(required, 'hanoi_all_forbidden.txt')
        self.assertFalse(th.isWon())

        solver = SolverDFS(th,((),(),(1,2,3)))

        self.runPlayXSteps(solver, [
            # [step, expected game state]
            [3, ((1, 3), (), (2,))],
            [13, ((2,), (), (1, 3))],
            [22, ((2,), (1, 3), ())],
        ])

    def test03_DFS_Hanoi(self):
        print("-------------------------------TEST THREE-------------------------------")
        th = TowerOfHanoiGame()
        th.read('hanoi_3_all_disks_on_peg_one.txt')
        required = [
            'fact: (movable disk1 peg3 peg1)',
            'fact: (movable disk1 peg3 peg2)',
        ]
        th.setWinningCondition(required, 'hanoi_all_forbidden.txt')
        self.assertFalse(th.isWon())

        solver = SolverDFS(th, ((),(),(1,2,3)))
        self.runSolve(solver)

    def test04_BFS_Hanoi(self):
        print("-------------------------------TEST FOUR-------------------------------")
        th = TowerOfHanoiGame()
        th.read('hanoi_3_all_disks_on_peg_one.txt')
        required = [
            'fact: (movable disk1 peg3 peg1)',
            'fact: (movable disk1 peg3 peg2)',
        ]
        th.setWinningCondition(required, 'hanoi_all_forbidden.txt')
        self.assertFalse(th.isWon())

        solver = SolverBFS(th,((),(),(1,2,3)))

        self.runPlayXSteps(solver, [
            # [step, expected game state]
            [10, ((), (1,2), (3,))],
            [11, ((1,), (3,), (2,))],
            [20, ((), (1,2,3), ())],
        ])

    def test05_BFS_Hanoi(self):
        print("-------------------------------TEST FIVE-------------------------------")
        th = TowerOfHanoiGame()
        th.read('hanoi_3_all_disks_on_peg_one.txt')
        required = [
            'fact: (movable disk1 peg3 peg1)',
            'fact: (movable disk1 peg3 peg2)',
        ]
        th.setWinningCondition(required, 'hanoi_all_forbidden.txt')
        self.assertFalse(th.isWon())

        solver = SolverBFS(th, ((),(),(1,2,3)))
        self.runSolve(solver,)

    def test06_GM_8Puzzle(self):
        print("-------------------------------TEST SIX-------------------------------")
        p8 = Puzzle8Game()
        p8.read('puzzle8_top_right_empty.txt')
        required = [
            'fact: (movable tile6 pos3 pos2 pos3 pos3)',
            'fact: (movable tile8 pos2 pos3 pos3 pos3)',
        ]
        p8.setWinningCondition(required, 'puzzle8_all_forbidden.txt')
        self.assertFalse(p8.isWon())

        movables = p8.getMovables()
        self.assertEqual(p8.getGameState(), ((5,4,-1),(6,1,8),(7,3,2)))
        p8.makeMove(movables[0])
        self.assertEqual(p8.getGameState(), ((5,4,8),(6,1,-1),(7,3,2)))
        p8.reverseMove(movables[0])
        self.assertEqual(p8.getGameState(), ((5,4,-1),(6,1,8),(7,3,2)))


    def test07_DFS_8Puzzle(self):
        print("-------------------------------TEST SEVEN-------------------------------")
        p8 = Puzzle8Game()
        p8.read('puzzle8_top_right_empty.txt')
        required = [
            'fact: (movable tile6 pos3 pos2 pos3 pos3)',
            'fact: (movable tile8 pos2 pos3 pos3 pos3)',
        ]
        p8.setWinningCondition(required, 'puzzle8_all_forbidden.txt')
        self.assertFalse(p8.isWon())

        solver = SolverDFS(p8,((1,2,3),(4,5,6),(7,8,-1)))

        self.runPlayXSteps(solver, [
            # [step, expected game state]
            [9, ((4, 8, 1), (5, 3, -1), (6, 7, 2))],
            [17, ((8, 1, 2), (4, 3, -1), (5, 6, 7))],
            [34, ((2, 7, 6), (1, 3, 5), (8, 4, -1))],
        ])

    def test08_BFS_8Puzzle(self):
        print("-------------------------------TEST EIGHT-------------------------------")
        p8 = Puzzle8Game()
        p8.read('puzzle8_top_right_empty.txt')
        required = [
            'fact: (movable tile6 pos3 pos2 pos3 pos3)',
            'fact: (movable tile8 pos2 pos3 pos3 pos3)',
        ]
        p8.setWinningCondition(required, 'puzzle8_all_forbidden.txt')
        self.assertFalse(p8.isWon())

        solver = SolverBFS(p8,((1,2,3),(4,5,6),(7,8,-1)))

        self.runPlayXSteps(solver, [
            # [step, expected game state]
            [5, ((-1, 5, 4), (6, 1, 8), (7, 3, 2))],
            [13, ((5, 1, 4), (6, 8, -1), (7, 3, 2))],
            [21, ((5, 4, 8), (6, 1, 2), (-1, 7, 3))],
        ])


if __name__ == '__main__':
    unittest.main()
