#!/usr/bin/env python3

import time
import re
from collections import namedtuple
from functools import reduce, cache
from operator import mul
from statistics import pvariance

def get_test_file_path() :
    return "tests.txt"

def get_input_file_path() :
    return "input.txt"

def get_file_content( _file_path, _as_lines = True ) :
    with open( _file_path, 'r' ) as f :
        if ( _as_lines ) :
            data = f.readlines()
        else :
            data = f.read()
    return data

robot_re = re.compile( r"^p=(?P<px>[-+]?\d+),(?P<py>[-+]?\d+) v=(?P<vx>[-+]?\d+),(?P<vy>[-+]?\d+)$" )

Position = namedtuple( "Position", [ "x", "y" ] )
Vector = namedtuple( "Vector", [ "x", "y" ] )
Grid = namedtuple( "Grid", [ "width", "height", "robots" ] )
GridScore = namedtuple( "GridScore", [ "axis", "variance", "iteration", "max_iterations" ] )

def parse_data( str_data, verbose = False ) :
    robots = []
    for id, line in enumerate( str_data ) :
        if verbose :
            print( f"Line #{id}" )
        match = robot_re.match( line.strip() ).groupdict()
        position = Position( x=int(match["px"]), y=int(match["py"]) )
        vector = Vector( x=int(match["vx"]), y=int(match["vy"]) )
        robot = ( id, position, vector )
        print( f"New robot: {robot}" )
        robots.append( robot )
    print( f"Nb of robots: {len(robots)}" )
    return robots

def count_robots( x, y, robots ) :
    count = 0
    for id, position, vector in robots :
        if position == ( x, y ) :
            count += 1
    return count

EMPTY = "."
def print_grid( grid, iteration = None, verbose = False ) :
    print()
    print( f"Grid {grid.width}x{grid.height}:" )
    for y in range( grid.height ) :
        line = ""
        for x in range( grid.width ) :
            nb_robots = count_robots( x, y, grid.robots )
            line += str(nb_robots) if nb_robots > 0 else EMPTY
        print( line )
    if ( iteration is not None ) :
        print( f"Grid iteration #{iteration}" )
    print()

def move_robots( grid, nb_iterations, verbose = False ) :
    for index, robot in enumerate( grid.robots ) :
        id, position, vector = robot
        # since the vectors are constant, we can do all the iterations at once !
        new_x = ( position.x + nb_iterations * vector.x ) % grid.width
        new_y = ( position.y + nb_iterations * vector.y ) % grid.height
        new_position = Position( x=new_x, y=new_y )
        grid.robots[ index ] = ( id, new_position, vector )
    return grid

def get_grid_scores( grid, iteration, verbose = False ) :
    positions = [ pos for id, pos, v in grid.robots ]
    print( f"Computing grid scores for iteration #{iteration}" )
    scores = []
    if iteration < grid.width :
        # we calculate "x" score only for iteration between 0 and width (excluded)
        # as "x" scores will rotate every "width" iteration (width prime)
        var_x = pvariance( [ x for x, y in positions ] )
        if verbose :
            print( f"Variance for 'x' axis: {var_x}" )
        scores.append(
            GridScore( variance=var_x, iteration=iteration, max_iterations=grid.width, axis="x" )
        )
    if iteration < grid.height :
        # we calculate "y" score only for iteration between 0 and height (excluded)
        # as "y" scores will rotate every "height" iteration (height prime)
        var_y = pvariance( [ y for x, y in positions ] )
        if verbose :
            print( f"Variance for 'y' axis: {var_y}" )
        scores.append(
            GridScore( variance=var_y, iteration=iteration, max_iterations=grid.height, axis="y" )
        )
    return scores

def extended_euclid( a : int, b : int ) -> tuple[ int, int, int ] :
    """
    Applies the extended Euclid algorithm to integer pair a, b
    to extract gcd & solutions to diophantine equation a*u + b*v = gcd

    Args:
        a (int): first integer
        b (int): second integer

    Returns:
        tuple[ int, int, int ]: (gcd, u, v) such that:
        - gcd is the greatest common divisor between a and b
        - a*u + b*v = gcd
    """
    if a == 0 or b == 0 :
        except_message  = f"Extended Euclid algorithm: arguments ({a}, {b}) must be non-zero integers"
        raise ValueError( except_message )
    elif a < 0 or b < 0 :
        # the algorithm is made for positive integers only !
        gcd, u, v = extended_euclid( abs(a), abs(b) )
        u = -u if a < 0 else u
        v = -v if b < 0 else v
    elif a < b :
        gcd, v, u = extended_euclid( b, a )
    elif a == b :
        # gcd = a = b
        gcd, u, v = a, 1, 0
    else :
        # actual extended Euclid algorithm
        # source: https://fr.wikipedia.org/wiki/Algorithme_d%27Euclide_%C3%A9tendu
        # step 0 of algorithm: r(0), u(0), v(0), init as previous values for r, u, v
        r1, u1, v1 = a, 1, 0
        # step 1 of algorithm: r(1), u(1), v(1), init as current values for r, u, v
        r, u, v = b, 0, 1
        # steps 2+ of algorithm:
        while r > 0 :
            r2, u2, v2 = r1, u1, v1
            r1, u1, v1 = r, u, v
            q, r = divmod( r2, r1 ) # r2 = q * r1 + r <=> r = r2 - q * r1
            u, v = u2 - q * u1, v2 - q * v1
        # r == 0 stops the algorithm, r1, u1, v1 contains the wanted values
        gcd, u, v = r1, u1, v1
    return gcd, u, v

def chinese_remainder( *args : *tuple[ int, int ] ) -> tuple[ int, int ] :
    """
    Computes x = X % n from the congruences given as arguments
        args are tuples of integers ( x_i, n_i ) where x_i = X % n_i, X being the searched value

    Raises:
        ValueError: if chinese remainder algorithm cannot be applied because of non coprime values

    Returns:
        tuple[ int, int ]: x, n such that 0 <= x < n,
        with n = lcm( n_i ), and x % n_i = x_i, for all x_i, n_i passed as args
        
        Nota: all numbers X = x + k*n are solutions, for k in Z
    """
    if len( args ) == 0 :
        return None
    elif len( args ) == 1 :
        return args[ 0 ]
    elif len( args ) == 2 :
        x1, n1 = args[0]
        x2, n2 = args[1]
        gcd, u1, u2 = extended_euclid( n1, n2 ) # gcd = u1*n1 + u2*n2
        if gcd != 1 and ( x1 - x2 ) % gcd != 0 :
            # n1, n2 are not coprimes !
            # CR algorithm works ONLY when gcd divides x1-x2
            except_message  = f"chinese_remainder(({x1}, {n1}), ({x2}, {n2})): NO SOLUTION"
            except_message += f"\n{gcd} = gcd({n1}, {n2}) does not divide {x1-x2} = {x1} - {x2})"
            raise ValueError( except_message )
        n = n1 * n2 // gcd # = lcm( n1, n2 ) (= n1 * n2 if n1, n2 are coprimes)
        l = ( x1 - x2 ) // gcd
        x = x1 - n1 * u1 * l # or: x = x2 + n2 * u2 * l
        return ( x % n, n )
    else : # len( args ) > 2
        # faster if we compute between 2 n_i, n_j with similar nb of digits
        # => we sort the args on their n_i values and group them 2 by 2
        list_args = [ arg for arg in args ]
        list_args.sort( key = lambda t : t[1] )
        new_args = []
        for i in range( len( list_args ) // 2 ) :
            couple_1 = list_args[ 2*i ]
            couple_2 = list_args[ 2*i+1 ]
            new_args.append( chinese_remainder( couple_1, couple_2 ) )
        if ( len( list_args ) % 2 == 1 ) :
            # odd number of args: we need to add the last remaining arg to the new args
            new_args.append( list_args[ -1 ] )
        return chinese_remainder( *new_args )

def do_problem( str_data, width, height, verbose = False ) :
    robots = parse_data( str_data, verbose )
    starting_robots = robots[::]
    grid = Grid( width=width, height=height, robots=robots )
    if verbose :
        print_grid( grid, None, verbose )
    else :
        print( f"Grid size: {grid.width}x{grid.height}" )
    all_scores = []
    max_iteration = max( grid.width, grid.height )
    print( f"Computing scores for grid iterations #0 to #{max_iteration}" )
    for iteration in range( max_iteration ) :
        if verbose :
            print( f"Iteration #{iteration}" )
        grid = move_robots( grid, 1 if iteration != 0 else 0, verbose ) # no move for iteration #0!
        all_scores += get_grid_scores( grid, iteration, verbose )
    print( f"Sorting grids results..." )
    scores_x = [ score for score in all_scores if score.axis == "x" ]
    best_x = min( scores_x )
    print( f"Best score for x: grid iteration #{best_x.iteration} (variance: {best_x.variance})" )
    scores_y = [ score for score in all_scores if score.axis == "y" ]
    best_y = min( scores_y )
    print( f"Best score for y: grid iteration #{best_y.iteration} (variance: {best_y.variance})" )
    print( f"Computing nb of iterations to get both minimums" )
    nb_iteration, max_iteration = chinese_remainder(
        ( best_x.iteration, width ), ( best_y.iteration, height )
    )
    print( f"Value of iteration found: {nb_iteration}, for max nb of iterations {max_iteration}" )
    grid = Grid( width=width, height=height, robots=starting_robots[::] )
    grid = move_robots( grid, nb_iteration, verbose )
    print_grid( grid, nb_iteration, verbose )
    print( f"END" )

def do_tests() :
    str_data = get_file_content( get_test_file_path(), True )
    do_problem( str_data, 11, 7, True )

def do_input() :
    str_data = get_file_content( get_input_file_path(), True )
    do_problem( str_data, 101, 103, False )

def main() :
    start = time.time()
    #do_tests()
    do_input()
    elapsed = time.time() - start
    print( f"Total execution time: {elapsed:.3f} s" )

main()
