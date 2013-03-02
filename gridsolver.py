"""
Example:
from gridsolver import GridSolver
g = GridSolver({'rows':[[1,2], [4], [3], [1,1]], 'cols':[[4], [2], [3], [2,1]]})
g.solve()
print g.grid.show()

cols=[[2],[1,2],[2,3],[2,3],[3,1,1],[2,1,1],[1,1,1,2,2],[1,1,3,1,3],[2,6,4],[3,3,9,1],[5,3,2],[3,1,2,2],[2,1,7],[3,3,2],[2,4],[2,1,2],[2,2,1],[2,2],[1],[1]]
rows=[[3],[5],[3,1],[2,1],[3,3,4],[2,2,7],[6,1,1],[4,2,2],[1,1],[3,1],[6],[2,7],[6,3,1],[1,2,2,1,1],[4,1,1,3],[4,2,2],[3,3,1],[3,3],[3],[2,1]]
g1=GridSolver({'rows':rows,'cols':cols})
g1.solve()
print g1.grid.show()
"""
from canvas import Canvas

def generate_distributions(bits, slots):
    """ 
        Uses recursion to generates binomial distribution 
        for all possible combinations for arranging bits into slots
        ie generate_distributions(bits=3, slots=3) =
        [
            [0,0,3],
            [0,1,2],
            [0,2,1],
            [0,3,0],
            [1,0,2],
            [1,1,1],
            [1,2,0],
            [2,0,1],
            [2,1,0],
            [3,0,0]
        ]
    """
    if slots==0:
        return [[]]
    if slots==1:
        return [[bits]]
    bit_distributions = []
    for i in range(bits + 1):
        for inner_bit_distribution in generate_distributions(bits-i, slots-1):
            bit_distributions.append([i] + inner_bit_distribution)
    return bit_distributions

def col_row_index(line_index, opposing_index, is_row_not_col):
    """ Utility function to order col and row index """
    if is_row_not_col:
        return opposing_index, line_index
    else:
        return line_index, opposing_index

class GridSolver(object):
    """
    Solves nonogram puzzle based on input provided

    Example:
    from gridsolver import GridSolver
    g = GridSolver({'rows':[[1,2], [4], [3], [1,1]], 'cols':[[4], [2], [3], [2,1]]})
    g.solve()
    print g.grid.show()
    rows = [[1,2], [4], [3], [1,1]]
    cols = [[4], [2], [3], [2,1]]
    X-XX
    XXXX
    XXX-
    X--X
    """
    grid = Canvas()
    input = {'rows':[[]], 'cols':[[]]}  # no zeroes (can ensure this in a method)
    rows = [[]]
    cols = [[]]
    width = 0
    height = 0
    unknown_char = 'O'
    dot_char = '-'
    fill_char = 'X'
    max_iterations = 10
    
    def __init__(self, input = {'rows':[[]], 'cols':[[]]}, max_iterations=10):
        self.cols = input['cols']
        self.width = len(self.cols)
        self.rows = input['rows']
        self.height = len(self.rows)
        self.grid = Canvas(self.width, self.height, self.unknown_char)
        self.input = input
        self.max_iterations = max_iterations
    
    def fill_grid_pixel(self, x, y):
        self.grid.bitmap[x][y] = self.fill_char
    
    def dot_grid_pixel(self, x, y):
        self.grid.bitmap[x][y] = self.dot_char
    
    def is_grid_filled(self, x, y):
        return self.grid.bitmap[x][y] == self.fill_char
    
    def is_grid_dotted(self, x, y):
        return self.grid.bitmap[x][y] == self.dot_char
    
    def is_grid_unknown(self, x, y):
        return self.grid.bitmap[x][y] == self.unknown_char   # = not (self.is_grid_dotted(x, y) or self.is_grid_filled(x, y))
    
    def is_grid_complete(self):
        return not True in map(lambda col: self.unknown_char in col, self.grid.bitmap)
    
    def is_grid_row_complete(self, row_index):
        # checks if no unknowns in row
        return not self.unknown_char in self.grid.get_row(row_index)
    
    def is_grid_col_complete(self, col_index):
        # checks if no unknowns in col
        return not self.unknown_char in self.grid.get_col(col_index)
    
    def solve(self, max_iterations=10):
        self.max_iterations = max_iterations
        iterations = 0
        for n in range(0, self.max_iterations):
            # print n
            for col_index in range(self.width):
                #if not self.is_grid_col_complete(col_index):
                self.grid.bitmap[col_index] = self.solve_col(col_index)
            for row_index in range(self.height):
                #if not self.is_grid_row_complete(row_index):
                for col_index, pixel in enumerate(self.solve_row(row_index)):
                    if self.is_grid_unknown(col_index, row_index):
                        self.grid.colour_pixel(col_index, row_index, pixel)
            if self.is_grid_complete():
                iterations = n + 1
                break
        # print iterations
        return self.grid.transform()

    def solve_row(self, row_index):
        return self.solve_line(row_index, True)

    def solve_col(self, col_index):
        return self.solve_line(col_index, False)
        
    def solve_line(self, line_index, is_row_not_col):
        # check all combos in this line
        if is_row_not_col:
            combos = self.calculate_combos(self.rows[line_index], self.width)
        else:
            combos = self.calculate_combos(self.cols[line_index], self.height)
        cross_combo = None          # create cross referenced combo
        for combo in combos:
            # first loop to ignore combos that do not fit with canvas
            bad_combo = False
            for opposing_index, pixel in enumerate(combo):
                col_index, row_index = col_row_index(line_index, opposing_index, is_row_not_col)
                if (pixel == self.fill_char and self.is_grid_dotted(col_index, row_index)) or \
                  (pixel == self.dot_char and self.is_grid_filled(col_index, row_index)):
                    bad_combo = True
                    break   # stop checking this combo as it does not fit with existing grid
            if bad_combo:
                continue    # go to next item cos this one aint no good
            
            if cross_combo is None:
                cross_combo = list(combo)   # initialise cross reffed combo to first possible combo
            else:
                # cycle each pixel to see if it is different to cross combo
                for opposing_index, pixel in enumerate(combo):
                    col_index, row_index = col_row_index(line_index, opposing_index, is_row_not_col)
                    # pixels that have more than one variant combo are unknown
                    if cross_combo[opposing_index] != self.unknown_char and cross_combo[opposing_index] != pixel:
                        cross_combo[opposing_index] = self.unknown_char
        if cross_combo == None:
            # print "no solvable solns", is_row_not_col
            return [combos[0]]  # todo: raise error
        else:
            # print "".join(cross_combo)
            return cross_combo
    
    def calculate_combos(self, line, length):
        slot_count = len(line) + 1
        extra_spaces = length - sum(line) - len(line) + 1
        space_dists = generate_distributions(extra_spaces, slot_count)
        combos = []
        for space_dist in space_dists:
            combo = space_dist[0] * self.dot_char
            for n in range(len(space_dist) - 1):
                combo += line[n] * self.fill_char + (space_dist[n + 1] + 1) * self.dot_char
            combo = combo[:length]          # strip off the extra space generated in end slot
            combos.append(combo)
        return combos
