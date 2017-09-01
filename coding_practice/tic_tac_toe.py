class User(object):
    def __init__(self, name, symbol):
        self.name = symbol if not name else name
        self.symbol = symbol

    def name(self):
        return name

    def symbol(self):
        return symbol


class BlockAlreadyChosen(Exception):
    def __init__(self,*args,**kwargs):
        Exception.__init__(self,*args,**kwargs)


class InvalidBlock(Exception):
    def __init__(self,*args,**kwargs):
        Exception.__init__(self,*args,**kwargs)


class Board(object):
    def __init__(self, n, player1, player2):
        self.rows = self.cols = n
        self.layout = [[0 for x in xrange(n)] for i in xrange(n)]
        self.helplayout = [[self.rows*i+x+1 for x in xrange(self.cols)] for i in xrange(self.rows)]
        self.players = [player1, player2]


    def player_name(self, symbol):
        return self.players[0].name if self.players[0].symbol == symbol else self.players[1].name

    def diagonals(self):
        ret = list()
        ret.append([self.layout[n][n] for n in range(self.rows)])
        ret.append([self.layout[n][n] for n in range(self.rows-1, 0, -1)])
        return ret

    def check_winner(self):
        for row in self.layout:
            if sum(row) >= 3: return True, self.player_name('X')
            if sum(row) <= -3: return True, self.player_name('O')
        for col in zip(*self.layout):
            if sum(list(col)) >= 3: return True, self.player_name('X')
            if sum(list(col)) <= -3: return True, self.player_name('O')
        for diag in self.diagonals():
            if sum(diag) >= 3: return True, self.player_name('X')
            if sum(diag) <= -3: return True, self.player_name('O')

        return False, ''

    def reference_board(self):
        print "\nReference Board"
        for i in range(self.rows):
            print '  |  '.join([str(c) for c in self.helplayout[i]])
            print '_____'*self.rows

    def live_board(self):
        print "\nAction Board"
        t = list()
        for i in range(self.rows):
            print '  |  '.join([{c>=1: 'X', c<0: 'O'}.get(True, ' ') for c in self.layout[i]])
            print '_____'*self.rows

    def display_board(self, help=False):
        self.reference_board() if help else self.live_board()
        
    def insert(self, n, symbol):
        if n>self.rows*self.cols:
            print 'Choose a number less then {0}'.format(self.rows*self.cols)
            raise InvalidBlock()

        if self.layout[n/self.rows][n%self.cols] != 0:
            print 'This block is already chosen, find another block'
            raise BlockAlreadyChosen()

        self.layout[n/self.rows][n%self.cols] = 1 if symbol == 'X' else -1


if __name__ == "__main__":
    while 1:
        try:
            size = raw_input("Enter the Board size rows/cols(integer)? ")
            size = int(size)
            if size < 3:
                print 'Size should be greater than 2'
                continue
        except Exception as e:
            continue

        player1 = raw_input("Enter player1 name, his symbol (X)? ")
        player2 = raw_input("Enter player2 name, his symbol (O)? ")
        b = Board(size, User(player1, 'X'), User(player2, 'O'))
        player = 0
        b.display_board(help=True)

        while 1:
            n = raw_input("Player {0}.. Choose a number between 1 to {1}:  ".format(b.players[player].name, (size*size)))
            try:
                b.insert(int(n)-1, b.players[player].symbol)
                b.display_board()
                status, winner = b.check_winner()
                if status:
                    print "Player {0} won the game.... ".format(winner)
                    break
                b.display_board(help=True)
            except:
                continue

            player = 1 - player


        another = raw_input("Do you want to play another game [N/y]  ")
        if another == '' or another == 'N':
            exit()
        else:
            continue