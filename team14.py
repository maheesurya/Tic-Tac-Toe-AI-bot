import random
import signal
import copy

class TimedOutExc(Exception):
    pass


class Team14():
    def __init__(self):
        self.best_move = []
        self.TIME = 15
        self.players = ['x', 'o']
        self.flag = 0
        self.current_depth = 0
        self.max_depth = 5

    def handler(self, signum, frame):
        #print 'Signal handler called with signal', signum
        raise TimedOutExc()

    def move(self, board, old_move, flag):
        cells = board.find_valid_move_cells(old_move)
        self.best_move = []
        self.flag = flag
        signal.signal(signal.SIGALRM, self.handler)
        signal.alarm(self.TIME)
        temp_board = copy.deepcopy(board)
        
        if old_move == (-1, -1):
            return cells[random.randrange(len(cells))]
            # return (1, 1)

        try:
            if flag == 'x':
                self.max_minimax(temp_board, float(-9223372036854775807 - 1),  float(9223372036854775807), self.current_depth, self.max_depth, flag, old_move)
            elif flag == 'o':
                self.min_minimax(temp_board, float(-9223372036854775807 - 1),  float(9223372036854775807), self.current_depth, self.max_depth, flag, old_move)
        except TimedOutExc:
            if self.best_move == [] or self.best_move not in cells:
                return cells[random.randrange(len(cells))]
            elif self.best_move != []:
                temp = self.best_move[random.randrange(len(self.best_move))]
                return temp

        if self.best_move != []:
            temp = self.best_move[random.randrange(len(self.best_move))]
            if temp not in cells:
                return cells[random.randrange(len(cells))]
            else:
                return temp
        else:
            return cells[random.randrange(len(cells))]
        # else:
            # signal.alarm(0)


    def next_player_detector(self, flag):
        if flag == 'x':
            next_player = 'o'
        else:
            next_player = 'x'
        return next_player

    #used to evaluate the row value in a particular small board
    def row_element_counter(self, board, i):
        row = i
        col_start = 0
        max_col = 4

        cntx = 0
        cnto = 0
        cntd = 0
        cnte = 0

        while col_start < max_col:
            if board[row][col_start] == 'x':
                cntx += 1
            elif board[row][col_start] == 'o':
                cnto += 1
            elif board[row][col_start] == 'd':
                cntd += 1
            else:
                cnte += 1
            col_start += 1
        return (cntx, cnto, cntd, cnte)

    #used to evaluate the column value in a particular small board
    def col_element_counter(self, board, i):
        col = i
        row_start = 0
        max_row = 4

        cntx = 0
        cnto = 0
        cntd = 0
        cnte = 0

        while row_start < max_row:
            if board[row_start][col] == 'x':
                cntx += 1
            elif board[row_start][col] == 'o':
                cnto += 1
            elif board[row_start][col] == 'd':
                cntd += 1
            else:
                cnte += 1
            row_start += 1
        return (cntx, cnto, cntd, cnte)


    #used to analyse and return weight according to the x,o,e in a row or column
    def row_col_evaluator(self, board, i, flag, row_or_col, main_mat_zero, wtp, wte):
        if row_or_col == 1: # 1 means row
            cntx, cnto, cntd, cnte = self.row_element_counter(board, i)
            value = self.row_count_analysis(board, flag, i, cntx, cnto, cntd, cnte, main_mat_zero, wtp, wte)
        else:               # 2 means col
            cntx, cnto, cntd, cnte = self.col_element_counter(board, i)
            value = self.col_count_analysis(board, flag, i, cntx, cnto, cntd, cnte, main_mat_zero, wtp, wte)
        return value

    #used to analyse and return weight according to the x,o,e in a diamond
    def row_count_analysis(self, board, flag, i, cntx, cnto, cntd, cnte, main_mat_zero, wtp, wte):
        wtx = 0
        wto = 0
        total = 0
        if cntd == 0:
            if cntx != 0:
                wtx = wtp * (10**cntx)
            if cnto != 0:
                wto = wte * (10**cnto)
            # if flag == 'x':
            if cntx > 0 and cnto == 0:
                for j in range(4):
                    if board[i][j] == '-':
                        total += main_mat_zero[i][j]
                return wtx + total
            # elif flag == 'o':
            elif cnto > 0 and cntx == 0:
                for j in range(4):
                    if board[i][j] == '-':
                        total += main_mat_zero[i][j]
                return total - wto
        return total


    def col_count_analysis(self, board, flag, i, cntx, cnto, cntd, cnte, main_mat_zero, wtp, wte):
        wtx = 0
        wto = 0
        total = 0
        if cntd == 0:
            if cntx != 0:
                wtx = wtp * (10**cntx)
            if cnto != 0:
                wto = wte * (10**cnto)
            # if flag == 'x':
            if cntx > 0 and cnto == 0:
                for j in range(4):
                    if board[j][i] == '-':
                        total += main_mat_zero[j][i]
                return wtx + total
            # elif flag == 'o':
            elif cnto > 0 and cntx == 0:
                for j in range(4):
                    if board[j][i] == '-':
                        total += main_mat_zero[j][i]
                return total - wto
        return total


    def diamond_count_analysis(self, board, flag, row, col, cntx, cnto, cntd, cnte, main_mat_zero, wtp, wte):
        wtx = 0
        wto = 0
        total = 0
        if cntx != 0:
            wtx = wtp * (10**cntx)
        if cnto != 0:
            wto = wte * (10**cnto)
        # if flag == 'x':
        if cntd == 0:
            if cntx > 0 and cnto == 0:
                if board[row][col] == '-':
                    total += main_mat_zero[row][col]
                if board[row + 1][col - 1] == '-':
                    total += main_mat_zero[row + 1][col - 1]
                if board[row + 1][col + 1] == '-':
                    total += main_mat_zero[row + 1][col + 1]
                if board[row + 2][col] == '-':
                    total += main_mat_zero[row + 2][col]
                return wtx + total
            # elif flag == 'o':
            elif cnto > 0 and cntx == 0:
                if board[row][col] == '-':
                    total += main_mat_zero[row][col]
                if board[row + 1][col - 1] == '-':
                    total += main_mat_zero[row + 1][col - 1]
                if board[row + 1][col + 1] == '-':
                    total += main_mat_zero[row + 1][col + 1]
                if board[row + 2][col] == '-':
                    total += main_mat_zero[row + 2][col]
                return total - wto
        return total

    #used to count the number of distinct characters in a particular diamond
    def diamond_counter(self, board, row, col, flag):
        cntx = 0
        cnto = 0
        cntd = 0
        cnte = 0
        
        if board[row][col] == 'x':
            cntx += 1
        elif board[row][col] == 'o':
            cnto += 1
        elif board[row][col] == 'd':
            cntd += 1
        else:
            cnte += 1

        if board[row + 1][col - 1] == 'x':
            cntx += 1
        elif board[row + 1][col - 1] == 'o':
            cnto += 1
        elif board[row + 1][col - 1] == 'd':
            cntd += 1
        else:
            cnte += 1

        if board[row + 2][col] == 'x':
            cntx += 1
        elif board[row + 2][col] == 'o':
            cnto += 1
        elif board[row + 2][col] == 'd':
            cntd += 1
        else:
            cnte += 1

        if board[row + 1][col + 1] == 'x':
            cntx += 1
        elif board[row + 1][col + 1] == 'o':
            cnto += 1
        elif board[row + 1][col + 1] == 'd':
            cntd += 1
        else:
            cnte += 1

        return (cntx, cnto, cntd, cnte)

    def diamond_evaluator(self, board, row, col, flag, main_mat_zero, wtp, wte):
        val = 0
        cntx, cnto, cntd, cnte = self.diamond_counter(board, row, col, flag)
        val = self.diamond_count_analysis(board, flag, row, col, cntx, cnto, cntd, cnte, main_mat_zero, wtp, wte)
        return val

    def arr_evaluator(self, arr):
        val = 0
        for i in range(12):
            val += arr[i]
        return val

    def small_board_evaluator(self, board, flag, main_mat_zero, wtp, wte):
        best_val = [0 for i in range(12)]
        total = 0
        row = 0
        col = 0
        for i in range(4):
            total += self.row_col_evaluator(board, i, flag, 1, main_mat_zero, wtp, wte)

        for i in range(4):
            total += self.row_col_evaluator(board, i, flag, 2, main_mat_zero, wtp, wte)

        total += self.diamond_evaluator(board, row , col + 1, flag,main_mat_zero, wtp, wte)

        total += self.diamond_evaluator(board, row, col + 2, flag,main_mat_zero, wtp, wte)

        total += self.diamond_evaluator(board, row + 1, col +1, flag,main_mat_zero, wtp, wte)

        total += self.diamond_evaluator(board, row + 1, col + 2, flag,main_mat_zero, wtp, wte)

        return total

    def eval_func(self, board, old_move, flag):
        board_val = 0
        next_player = self.next_player_detector(flag)
        main_mat = [[0 for i in range(4)] for j in range(4)]
        main_mat_zero = [[0 for i in range(4)] for j in range(4)]
        for i in range(0, 4):
            for j in range(0, 4):
                if board.block_status[i][j] == '-':
                    temp_smallboard = [['-' for z in range(4)] for p in range(4)]
                    for k in range(4 * i, 4 * i + 4):
                        for l in range(4 * j, 4 * j + 4):
                            temp_smallboard[k - (4 * i)][l - (4 * j)] = board.board_status[k][l]
                    main_mat[i][j] = (self.small_board_evaluator(temp_smallboard, flag, main_mat_zero, 0.1, 0.1))
        board_val = self.small_board_evaluator(board.block_status, flag, main_mat, 100, 100)
        return board_val

    def max_minimax(self, board, alpha, beta, current_depth, max_depth, player_flag, old_move):
        next_player = self.next_player_detector(player_flag)
        stat = board.find_terminal_state()
        possible_moves = board.find_valid_move_cells(old_move)

        if current_depth == max_depth or stat[1] == 'WON' or stat[1] == 'DRAW' or len(possible_moves) == 0:
            temp = self.eval_func(board, old_move, player_flag)
            # temp = self.eval_func(board, old_move, self.flag) - self.eval_func(board, old_move, self.next_player_detector(self.flag))
            return temp
        best_val_max = float(-9223372036854775807 - 1)  # modify according to min of heuristic
        # best_val_min = float(9223372036854775807)  # modify according to min of heuristic
        for move in possible_moves:
            old_val = board.block_status[(move[0]/4)][(move[1]/4)]
            # board.board_status[move[0]][move[1]] = player_flag
            board.update(old_move, move, player_flag)
            val = self.min_minimax(board, alpha, beta, current_depth+1, max_depth, next_player, move)
            board.board_status[move[0]][move[1]] = '-'
            board.block_status[(move[0] / 4)][(move[1] / 4)] = old_val
            if current_depth == 0:
                if self.flag == 'x':
                    if val == best_val_max:
                        self.best_move.append(move)
                    elif val > best_val_max:
                        self.best_move = []
                        self.best_move.append(move)

            best_val_max = max(best_val_max, val)
            ############pruning#############
            alpha = max(alpha, best_val_max)
            if alpha >= beta:
                return best_val_max

        return best_val_max

    def min_minimax(self, board, alpha, beta, current_depth, max_depth, player_flag, old_move):
        next_player = self.next_player_detector(player_flag)
        stat = board.find_terminal_state()
        possible_moves = board.find_valid_move_cells(old_move)
        
        if current_depth == max_depth or stat[1] == 'WON' or stat[1] == 'DRAW' or len(possible_moves) == 0:
            temp = self.eval_func(board, old_move, player_flag)
            # temp = self.eval_func(board, old_move, self.flag) - self.eval_func(board, old_move, self.next_player_detector(self.flag))
            return temp
        best_val = float(9223372036854775807)  # modify according to max of heuristic
        for move in possible_moves:
            # old_val = board.board_status[move[0]][move[1]]
            # board.board_status[move[0]][move[1]] = player_flag
            old_val = board.block_status[(move[0] / 4)][(move[1] / 4)]
            board.update(old_move, move, player_flag)
            val = self.max_minimax(board, alpha, beta, current_depth + 1, max_depth, next_player, move)
            board.board_status[move[0]][move[1]] = '-'
            board.block_status[(move[0] / 4)][(move[1] / 4)] = old_val
            if current_depth == 0:
                if self.flag == 'o':
                    if val == best_val:
                        self.best_move.append(move)
                    elif val < best_val:
                        self.best_move = []
                        self.best_move.append(move)

            best_val = min(best_val, val)
            ############pruning#############
            beta = min(beta, best_val)
            if alpha >= beta:
                return best_val

        return best_val
