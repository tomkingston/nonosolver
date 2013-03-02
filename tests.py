from unittest import TestCase
from gridsolver import GridSolver, GridSolverExceptions

# simple puzzle
#from gridsolver import GridSolver
#    g = GridSolver({'rows':[[1,2], [4], [3], [1,1]], 'cols':[[4], [2], [3], [2,1]]})
#    g.solve()
#    print g.grid.show()

#cols=[[2],[1,2],[2,3],[2,3],[3,1,1],[2,1,1],[1,1,1,2,2],[1,1,3,1,3],[2,6,4],[3,3,9,1],[5,3,2],[3,1,2,2],[2,1,7],[3,3,2],[2,4],[2,1,2],[2,2,1],[2,2],[1],[1]]
#rows=[[3],[5],[3,1],[2,1],[3,3,4],[2,2,7],[6,1,1],[4,2,2],[1,1],[3,1],[6],[2,7],[6,3,1],[1,2,2,1,1],[4,1,1,3],[4,2,2],[3,3,1],[3,3],[3],[2,1]]
#g1=GridSolver({'rows':rows,'cols':cols})
#g1.solve()
#print g1.grid.show()
#g1.fill_grid_pixel(10,1)
#g1.fill_grid_pixel(11,1)
#g1.solve()
#print g1.grid.show()


#cols=[[4],[1,3,3],[1,2,5],[2,9],[2,2,4,1],[8,2,1],[6,2,1],[3,4,1],[9,1],[8,2],[9,2],[2,1,2,3],[1,2,5],[1,1,5],[4,4]]
#rows=[[3],[1,2],[1,2,4],[2,1,2,1],[3,6,1],[10,3],[10],[2,2,3],[3,2,4],[11],[4,4,2],[9,3],[6,4],[1,6],[11]]
#g1=GridSolver({'rows':rows,'cols':cols})
#g1.solve()
#print g1.grid.show()

#cols=
#rows=[[3],[1,2],[1,2,4],[2,1,2,1],[3,6,1],[10,3],[10],[2,2,3],[3,2,4],[11],[4,4,2],[9,3],[6,4],[1,6],[11]]
#g1=GridSolver({'rows':rows,'cols':cols})
#g1.solve()
#print g1.grid.show()

class TestGridSolver(TestCase):
    simple_puzzle = {'rows':[[1,2], [4], [3], [1,1]], 
                           'cols':[[4], [2], [3], [2,1]]}
    simple_puzzle_solution = [['X','-','X','X'],
                              ['X','X','X','X'],
                              ['X','X','X','-'],
                              ['X','-','-','X']]
    simple_ambiguous_puzzle = {'rows':[[1],[1]],
                               'cols':[[1],[1]]}
    simple_ambiguous_puzzle_solutions = ([['X','-'],['-','X']], [['-','X'],['X','-']])
     
    def test_solving_simple_puzzle(self):
        simple_puzzle_solver = GridSolver(self.simple_puzzle)
        generated_solution = simple_puzzle_solver.solve()
        self.assertEqual(self.simple_puzzle_solution,
                         generated_solution,
                         "Simple puzzle was not solved correctly")
    
    def test_solving_simple_ambiguous_puzzle(self):
        """ Simple ambiguous puzzle has two solutions """
        simple_amiguous_puzzle_solver = GridSolver(self.simple_ambiguous_puzzle)
        self.assertRaises(GridSolverExceptions.AmbiguousPuzzleException, 
                          simple_amiguous_puzzle_solver.solve())
    
    def runTest(self):
        return self.test_solving_simple_puzzle()
        
# TestGridSolver().runTest()