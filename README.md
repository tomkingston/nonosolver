# Nonosolver

This is a simple nonogram solver that is able to solve simple puzzles using a row-solving algorithm. The algorithm is not capable of solving highly complicated puzzles or generating multiple solutions for ambiguous puzzles.  I intend to apply a field-solving algorithm to solve these harder puzzles.

## What is a nonogram?
Nonogram puzzles (also know as griddlers, hanjie, paint by numbers or picross) are grid-based logic puzzles. They are often found in newspapers where the solution normally reveals an image. They have also featured in computer games such as Mario Picross.

The header for each row and column specifies, in order, the number and size of contiguous blocks that must be placed in that row or column. Each block must have a minium of one space between it and the next block. For example, in a grid with width 5, a row header of 2,1 could be arranged in the following configurations: |XX-X-| |XX--X| |-XX-X|.

The puzzle is normally solved by iterating over each column and row and calculating the possible combinations - filling in blocks that are filled in every combination and dotting blocks that are blank in every combination. This is also the algorithm that is used by this solver.

###Example
The following shows the solution to a very simple small puzzle on a 5 by 5 grid:

            2
         4231
        ______
    1,2 |X-XX|
      4 |XXXX|
      3 |XXX-|
    1,1 |X--X|
        ‾‾‾‾‾‾
###Find out more
Visit [Wikipedia's Nonogram Page](http://en.wikipedia.org/wiki/Nonogram "Wikipedia Nonograms") for a full and detailed explanation.

## How to use this solver
To be completed

## How this solver works
To be completed