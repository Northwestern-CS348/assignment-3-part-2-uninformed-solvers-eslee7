from game_master import GameMaster
from read import *
from util import *

class TowerOfHanoiGame(GameMaster):

    def __init__(self):
        super().__init__()
        
    def produceMovableQuery(self):
        """
        See overridden parent class method for more information.

        Returns:
             A Fact object that could be used to query the currently available moves
        """
        return parse_input('fact: (movable ?disk ?init ?target)')

    def getGameState(self):
        """
        Returns a representation of the game in the current state.
        The output should be a Tuple of three Tuples. Each inner tuple should
        represent a peg, and its content the disks on the peg. Disks
        should be represented by integers, with the smallest disk
        represented by 1, and the second smallest 2, etc.

        Within each inner Tuple, the integers should be sorted in ascending order,
        indicating the smallest disk stacked on top of the larger ones.

        For example, the output should adopt the following format:
        ((1,2,5),(),(3, 4))

        Returns:
            A Tuple of Tuples that represent the game state
        """
        pegs = []
        for fact in self.kb.facts:
            if fact.statement.predicate == 'isPeg':
                peg_num = self.get_peg_num(fact.statement.terms[0])
                pegs.append([])

        for fact in self.kb.facts:
            if fact.statement.predicate == 'on':
                disk_num = self.get_disk_num(fact.statement.terms[0])
                peg_num = self.get_peg_num(fact.statement.terms[1])
                pegs[peg_num - 1].insert(0, disk_num) # hacky shortcut rn; go back to ensure this list is in order !!!

        for index, list in enumerate(pegs):
            pegs[index] = tuple(list)

        return tuple(pegs)

    def get_disk_num(self, disk_term):
        # helper for getting disk number
        return int(str(disk_term)[4:])

    def get_peg_num(self, peg_term):
        # helper for getting peg number
        return int(str(peg_term)[3:])

    def makeMove(self, movable_statement):
        """
        Takes a MOVABLE statement and makes the corresponding move. This will
        result in a change of the game state, and therefore requires updating
        the KB in the Game Master.

        The statement should come directly from the result of the MOVABLE query
        issued to the KB, in the following format:
        (movable disk1 peg1 peg3)

        Args:
            movable_statement: A Statement object that contains one of the currently viable moves

        Returns:
            None
        """

        game_state = self.getGameState()
        disk = movable_statement.terms[0]
        oldpeg = movable_statement.terms[1]
        newpeg = movable_statement.terms[2]

        disk_num = self.get_disk_num(disk)
        oldpeg_num = self.get_peg_num(oldpeg)
        newpeg_num = self.get_peg_num(newpeg)

        # if the peg that you left will be empty, declare it as empty
        if (len(game_state[oldpeg_num - 1]) == 1):
            # if so, it's empty!
            self.kb.kb_add(Fact(['empty', str(oldpeg)]))
            print('Making old peg ' + str(oldpeg) + ' empty')

        else:
            # else, if the peg you left is not going to be empty, find the disk below and make it topDisk
            for fact in self.kb.facts:
                if fact.statement.predicate == 'onDisk' and fact.statement.terms[0] == disk:
                    # get rid of the "onDisk" between the removed disk and the next dist
                    self.kb.kb_retract(fact)
                    # Add new topDisk
                    print('Updating top disk of old peg to be ' + str(fact.statement.terms[1]))
                    next_disk = fact.statement.terms[1]
                    self.kb.kb_add(Fact(['topDisk', str(next_disk), str(oldpeg)]))
                    break


        # if the peg you're going to is empty,
        # 1. make the dest peg not empty anymore
        # 2. "on" the disk to the peg
        if len(game_state[newpeg_num - 1]) == 0:
            for fact in self.kb.facts:
                if fact.statement.predicate == 'empty' and fact.statement.terms[0] == newpeg:
                    print('Retracting that the new peg ' + str(newpeg) + ' is empty, since it will have disk')
                    self.kb.kb_retract(fact)
                    break
            self.kb.kb_add(Fact(['on', str(disk), str(newpeg)]))

        # else, if the peg you're going to is not empty
        # 1. "onDisk" it to the topDisk of the new peg
        # 2. retract that the oldTopDisk is the topDisk
        else:
            for fact in self.kb.facts:
                # find old topDisk
                if fact.statement.predicate == 'topDisk' and fact.statement.terms[1] == newpeg:
                    oldTopDisk = fact.statement.terms[0]
                    self.kb.kb_add(Fact(['onDisk', str(disk), str(oldTopDisk)]))
                    self.kb.kb_retract(fact)
                    break

        # update topDisk:
        # 1. remove the disk as a topDisk of the old peg
        for fact in self.kb.facts:
            if fact.statement.predicate == 'topDisk' and fact.statement.terms[0] == disk and \
                    fact.statement.terms[1] == oldpeg:
                print("Retracting that the topDisk of " + str(oldpeg) + " is " + str(disk))
                self.kb.kb_retract(fact)
                break
        # 2. undo the "on" on the old peg
        for fact in self.kb.facts:
            if fact.statement.predicate == 'on' and fact.statement.terms[0] == disk and \
                    fact.statement.terms[1] == oldpeg:
                print("Taking disk " + str(disk) + ' off old peg')
                self.kb.kb_retract(fact)
                break
        # 3. add it as topDisk of new peg
        self.kb.kb_add(Fact(['topDisk', str(disk), str(newpeg)]))

        return

    def reverseMove(self, movable_statement):
        """
        See overridden parent class method for more information.

        Args:
            movable_statement: A Statement object that contains one of the previously viable moves

        Returns:
            None
        """
        pred = movable_statement.predicate
        sl = movable_statement.terms
        newList = [pred, sl[0], sl[2], sl[1]]
        self.makeMove(Statement(newList))

class Puzzle8Game(GameMaster):

    def __init__(self):
        super().__init__()

    def produceMovableQuery(self):
        """
        Create the Fact object that could be used to query
        the KB of the presently available moves. This function
        is called once per game.

        Returns:
             A Fact object that could be used to query the currently available moves
        """
        return parse_input('fact: (movable ?piece ?initX ?initY ?targetX ?targetY)')

    def getGameState(self):
        """
        Returns a representation of the the game board in the current state.
        The output should be a Tuple of Three Tuples. Each inner tuple should
        represent a row of tiles on the board. Each tile should be represented
        with an integer; the empty space should be represented with -1.

        For example, the output should adopt the following format:
        ((1, 2, 3), (4, 5, 6), (7, 8, -1))

        Returns:
            A Tuple of Tuples that represent the game state
        """

        rows = [[-1, -1, -1],[-1, -1, -1],[-1, -1, -1]]
        for fact in self.kb.facts:
            if fact.statement.predicate == 'xy' and str(fact.statement.terms[0]) != 'empty':
                x_num = self.get_pos_num(fact.statement.terms[1])
                y_num = self.get_pos_num(fact.statement.terms[2])
                rows[y_num - 1][x_num-1] = self.get_tile_num(fact.statement.terms[0])

        for index, list in enumerate(rows):
            rows[index] = tuple(list)

        return tuple(rows)

    def get_pos_num(self, pos_term):
    # helper for getting pos number
        return int(str(pos_term)[3:])

    def get_tile_num(self, tile_term):
    # helper for getting tile number
        return int(str(tile_term)[4:])

    def makeMove(self, movable_statement):
        """
        Takes a MOVABLE statement and makes the corresponding move. This will
        result in a change of the game state, and therefore requires updating
        the KB in the Game Master.

        The statement should come directly from the result of the MOVABLE query
        issued to the KB, in the following format:
        (movable tile3 pos1 pos3 pos2 pos3)

        Args:
            movable_statement: A Statement object that contains one of the currently viable moves

        Returns:
            None
        """
        ### Student code goes here
        pass

    def reverseMove(self, movable_statement):
        """
        See overridden parent class method for more information.

        Args:
            movable_statement: A Statement object that contains one of the previously viable moves

        Returns:
            None
        """
        pred = movable_statement.predicate
        sl = movable_statement.terms
        newList = [pred, sl[0], sl[3], sl[4], sl[1], sl[2]]
        self.makeMove(Statement(newList))
