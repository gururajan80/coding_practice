class User(object):
    def __init__(self, name, symbol):
        self.name = symbol if not name else name
        self.symbol = symbol

    def name(self):
        return name

    def symbol(self):
        return symbol

class Board(object):
    def __init__(self, n, player1, player2):
        self.size = n
        self.boardsize = n * n
        self.board = [0 for i in range(n*n+1)]
        self.helpboard = [i for i in range(1, n*n+1)]
        self.players = [player1, player2]

    def reference_board(self):
        print "\nReference Board"
        for i in range(len(self.helpboard)/self.size+1):
            print "  |  ".join([str(c) for c in self.helpboard[i*self.size:(i+1)*self.size]])
            print '______'*self.size

    def live_board(self):
        print "\nAction Board"
        for i in range(len(self.board)/self.size+1):
            print "  |  ".join([{c>=1: 'X', c<0: 'O'}.get(True, ' ') for c in self.board[i*self.size:(i+1)*self.size]])
            print '______'*self.size

    def display_board(self, help=False):
        self.reference_board() if help else self.live_board()

    def insert(self, p, symbol):
        if p > self.boardsize or p < 0:
            print 'Choose a number between {0} and {1}'.format(1, len(self.board))
            raise InvalidBlock()

        if self.board[p] != 0:
            print 'This block is already chosen, find another block'
            raise BlockAlreadyChosen()

        self.board[p] = 1 if symbol == 'X' else -1

    def get_possibilities(self, position, symbol, start, end, interval, check=True):
        possibilities = list()
        if position-interval >= start and position+interval <= end and \
            self.board[position-interval] == symbol and self.board[position+interval] == symbol:
            possibilities.append([self.board[position-interval],
                                self.board[position],
                                self.board[position+interval]])

        if check:
            if (position-(2*interval) >= start and position-interval > start and \
                self.board[position-interval] == symbol and self.board[position-(2*interval)] == symbol):
                possibilities.append([self.board[position-2*interval],
                                      self.board[position-interval],
                                      self.board[position]])

            if (position+interval < end and position+(2*interval) < end and \
                self.board[position+interval] == symbol and self.board[position+2*interval] == symbol):
                possibilities.append([self.board[position], self.board[position+interval],
                                      self.board[position+2*interval]])
        return possibilities

    def check_horizontal(self, position, symbol):
        start = (position/self.size)* self.size
        end = (position/self.size) * self.size + self.size - 1
        possibilities = self.get_possibilities(position, symbol, start, end, 1)
        return any(sum(p) == 3 or sum(p) == -3 for p in possibilities)

    def check_vertical(self, position, symbol):
        start = 0
        end = self.size*self.size - 1
        possibilities = self.get_possibilities(position, symbol, start, end, self.size)
        return any(sum(p) == 3 or sum(p) == -3 for p in possibilities)

    def check_diagonal(self, position, symbol):
        start = 0
        end = self.size*self.size - 1
        diag1_possibilities = self.get_possibilities(position, symbol, start, end, self.size+1)
        print diag1_possibilities
        diag2_possibilities = self.get_possibilities(position, symbol, start, end, self.size-1, check=False)
        print diag2_possibilities
        return (any(sum(p) == 3 or sum(p) == -3 for p in diag1_possibilities) or
                any(sum(p) == 3 or sum(p) == -3 for p in diag2_possibilities))

        return possibilities

    def check_winner(self, position, symbol):
        symbol = 1 if symbol=='X' else -1
        symbol = int(symbol)
        return self.check_horizontal(position, symbol) or self.check_vertical(position, symbol) or \
               self.check_diagonal(position, symbol)

if __name__ == "__main__":
    player1 = raw_input("Enter player1 name, his symbol (X)? ")
    player2 = raw_input("Enter player2 name, his symbol (O)? ")
    while 1:
        try:
            size = raw_input("Enter the Board size rows/cols(integer)? ")
            size = int(size)
            if size < 3:
                print 'Size should be greater than 2'
                continue
        except Exception as e:
            continue
        b = Board(size, User(player1, 'X'), User(player2, 'O'))
        player = 0
        b.display_board(help=True)
        while 1:
            user = b.players[player]
            n = raw_input("Player {0}.. Choose a number between 1 to {1}:  ".format(user.name, (size*size)))
            try:
                n = int(n)-1
            except ValueError:
                continue
            try:
                b.insert(n, user.symbol)
                b.display_board()
                status = b.check_winner(n, user.symbol)
                if status:
                    print "Player {0} won the game.... ".format(user.name)
                    break
                b.display_board(help=True)
            except:
                continue
            player = 1 - player

        another = raw_input("Do you want to quit [n/y]  ")
        if another == '' or another.upper() == 'Y':
            exit()
        else:
            continue