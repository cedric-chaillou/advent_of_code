#!/usr/bin/env python3

import time
from typing import Union, Optional
from collections import namedtuple
from dataclasses import dataclass
import re

def get_test_file_path( i: int = None ) -> str :
    return "tests.txt" if i is None else f"tests_{i}.txt"

def get_input_file_path() -> str :
    return "input.txt"

def get_file_content( file_path ) -> str :
    print( f"Reading: {file_path}" )
    with open( file_path, 'r' ) as f :
        data = f.read()
    return data

# y02: 0
INPUT_RE = re.compile( r"^(?P<name>[\w\d]{3}): (?P<value>[01])$" )
# x00 AND y00 -> z00
GATE_RE = re.compile( r"^(?P<a>[\w\d]{3}) (?P<op>AND|OR|XOR) (?P<b>[\w\d]{3}) -> (?P<name>[\w\d]{3})$" )

@dataclass( frozen = True )
class Gate :
    op: str
    in_1: str
    in_2: str

    def __repr__( self ) :
        repr = f"< {self.in_1} {self.op} {self.in_2} >"
        return repr
    
    def __eq__( self, comp: 'Gate' ) :
        # Gates are symetrical (input wise)
        # we want Gate( "XOR", "abc", "def" ) == Gate( "XOR", "def", "abc" )
        return self.op == comp.op and \
                sorted( ( self.in_1, self.in_2 ) ) == \
                    sorted( ( comp.in_1, comp.in_2 ) )

    def __hash__( self ) :
        # Gates are symetrical (input wise)
        # we want dict[ Gate( "XOR", "abc", "def" ) ] <=> dict[ Gate( "XOR", "def", "abc" ) ]
        #print( f"__hash__ for gate {self}" )
        return hash( tuple( [ self.op, ] + sorted( ( self.in_1, self.in_2 ) ) ) )

    def eval( self, in_1_value: int, in_2_value: int ) -> int :
        if self.op == "AND" :
            return in_1_value & in_2_value
        elif self.op == "OR" :
            return in_1_value | in_2_value
        elif self.op == "XOR" :
            return in_1_value ^ in_2_value

@dataclass
class WiredGate :
    gate: Gate
    wire: str # "out wire"

def parse_data( str_data: str, verbose: bool = False ) :
    x: list[str] = []
    y: list[str] = []
    z: list[str] = []
    inputs: dict[ str, int ] = dict()
    gates: dict[ str, Gate ] = dict()
    input_mode = True
    for line in str_data.strip().split( "\n" ) :
        if line == "" :
            print( "Empty line" ) if verbose else None
            input_mode = False
        elif input_mode :
            print( f"Input line: {line}" ) if verbose else None
            match = INPUT_RE.match( line ).groupdict()
            name = match[ "name" ]
            value = int( match[ "value" ] )
            inputs[ name ] = value
            if name[0] == "x" :
                x.append( name )
            elif name[0] == "y" :
                y.append( name )
        else :
            print( f"Gate line: {line}" ) if verbose else None
            match = GATE_RE.match( line ).groupdict()
            name = match[ "name" ]
            gate = Gate( match[ "op" ], match[ "a" ], match[ "b" ] )
            if verbose :
                print( f"Adding gate: {gate}" )
            gates[ name ] = gate
            if name[0] == "z" :
                z.append( name )
    x = tuple( sorted( x, reverse=True ) )
    y = tuple( sorted( y, reverse=True ) )
    z = tuple( sorted( z, reverse=True ) )
    x_input = "".join( str( inputs[i] ) for i in x )
    x_decimal = int( x_input, base=2 )
    y_input = "".join( str( inputs[i] ) for i in y )
    y_decimal = int( y_input, base=2 )
    if verbose :
        print( f"z output wires: {z}" )
    return x_decimal, y_decimal, z, gates, inputs

def solve( name: str, gates: dict[ str, Gate ], solved: dict[ str, int ], verbose: bool ) -> int :
    if solved.get( name, None ) is None :
        gate = gates[ name ]
        in_1_value = solve( gate.in_1, gates, solved, verbose )
        in_2_value = solve( gate.in_2, gates, solved, verbose )
        solved[ name ] = gate.eval( in_1_value, in_2_value )
        if verbose:
            print( f"Solved {name}: {gate} = {solved[ name ]}" )
    return solved[ name ]

def get_input_names( index ) :
    return f"x{index:02}", f"y{index:02}"

def get_output_name( index ) :
    return f"z{index:02}"

def get_wire( gate, wires ) :
    if not gate in wires :
        msg = f"Gate not found: {gate}"
        print( msg )
        raise KeyError( msg )
    return wires[ gate ]

def get_gate( wire, gates ) :
    if not wire in gates :
        msg = f"Wire not found: {wire}"
        print( msg )
        raise KeyError( msg )
    return gates[ wire ]

def swap_wires( gates, wires, wire_1, wire_2 ) :
    print( f"Swapping wires: {wire_1} <-> {wire_2}" )
    gate_1 = gates[ wire_1 ]
    gate_2 = gates[ wire_2 ]
    print( f"    Before swap: {wire_1}: {gate_1} / {wire_2}: {gate_2}" )
    wires[ gate_1 ] = wire_2
    gates[ wire_2 ] = gate_1
    wires[ gate_2 ] = wire_1
    gates[ wire_1 ] = gate_2
    print( f"    After swap: {wire_1}: {gate_2} / {wire_2}: {gate_1}" )
    return gates, wires

def check_expected_wire( actual_wire, expected_wire, gates, wires, swaps: list[str] ) :
    swapped = False
    if actual_wire != expected_wire :
        print( f"Invalid z-out wire {actual_wire} (expected {expected_wire})" )
        swaps.append( ( actual_wire, expected_wire ) )
        swapped = True
        gates, wires = swap_wires( gates, wires, actual_wire, expected_wire )
    return gates, wires, swaps, swapped

def find_gates( op: str, input: str, wires: dict[ Gate, str ] ) -> list[Gate] :
    gates = []
    for gate in wires :
        if gate.op == op and input in ( gate.in_1, gate.in_2 ) :
            gates.append( gate )
    return gates

def get_other_input( gate: Gate, input: str ) -> str :
    if gate.in_1 == input :
        return gate.in_2
    elif gate.in_2 == input :
        return gate.in_1
    else :
        raise RuntimeError( f"{input} is not a wire input for gate {gate}" )

@dataclass
class HalfAdder :
    index: int
    x_in: str
    y_in: str
    z_out: WiredGate # Gate( "XOR", x_in, y_in )
    c_out: WiredGate # Gate( "AND", x_in, y_in )

    def __repr__( self ) :
        repr = [
            f"Half Adder #{self.index}:",
            f"    X in >> {self.x_in}",
            f"    Y in >> {self.y_in}",
            f"             {self.z_out}    >> Z out",
            f"             {self.c_out}    >> C out",
        ]
        return "\n".join( repr )

def get_half_adder( index: int, gates: dict[ str, Gate ], wires: dict[ Gate, str ] ) :
    print()
    print( f"Contructing Half Adder #{index}..." )
    swaps = []
    x_in, y_in = get_input_names( index )
    z_expected_wire = get_output_name( index )
    print( f"Making Z out gate" )
    z_gate = Gate( "XOR", x_in, y_in )
    z_actual_wire = get_wire( z_gate, wires )
    gates, wires, swaps, swapped = check_expected_wire( z_actual_wire, z_expected_wire, gates, wires, swaps )
    z_is_valid = z_actual_wire == z_expected_wire
    if not z_is_valid :
        print( f"Found invalid out wire {z_actual_wire} for gate {z_gate}" )
        swaps.append( ( z_actual_wire, z_expected_wire ) )
        gates, wires = swap_wires( gates, wires, z_actual_wire, z_expected_wire )
    print( f"Making C out gate" )
    c_gate = Gate( "AND", x_in, y_in )
    c_wire = get_wire( c_gate, wires )
    half_adder = HalfAdder( index, x_in, y_in, WiredGate( z_gate, z_expected_wire )
                            , WiredGate( c_gate, c_wire ) )
    #print( f"{half_adder}" )
    return swaps, half_adder

@dataclass
class FullAdder :
    index: int
    x_in: str
    y_in: str
    c_in: str
    xor_1: WiredGate # Gate( "XOR", x_in , y_in  )
    z_out: WiredGate # Gate( "XOR", xor_1, c_in  )
    and_1: WiredGate # Gate( "AND", x_in , y_in  )
    and_2: WiredGate # Gate( "AND", xor_1, c_in  )
    c_out: WiredGate # Gate( "OR" , and_1, and_2 )

    def __repr__( self ) :
        repr = [
            f"Full Adder #{self.index}:",
            f"    X in >> {self.x_in}",
            f"    Y in >> {self.y_in}",
            f"    C in >> {self.c_in}",
            f"            (XOR 1:) {self.xor_1}",
            f"            (AND 1:) {self.and_1}",
            f"            (AND 2:) {self.and_2}",
            f"                    {self.z_out}    >> Z out",
            f"                    {self.c_out}    >> C out",
        ]
        return "\n".join( repr )

def get_full_adder( index: int, c_in: str, gates: dict[ str, Gate ], wires: dict[ Gate, str ] ) :
    print()
    print( f"Contructing Full Adder #{index}..." )
    swaps = []
    x_in, y_in = get_input_names( index )
    z_expected_wire = get_output_name( index )
    print( f"Making XOR 1 gate" )
    xor_1_gate = Gate( "XOR", x_in, y_in )
    xor_1_wire = get_wire( xor_1_gate, wires )
    print( f"Making Z out gate" )
    z_gate = Gate( "XOR", xor_1_wire, c_in )
    print( f"Making AND 2 gate" )
    and_2_gate = Gate( "AND", xor_1_wire, c_in )
    try :
        z_actual_wire = get_wire( z_gate, wires )
        and_2_wire = get_wire( and_2_gate, wires )
    except KeyError :
        # z_gate & and/or_2_gate do not exists
        # means thet either xor_1_wire or c_in is swapped ...
        print( f"Either {xor_1_wire} (xor 1) or {c_in} (carry in) is swapped with another wire..." )
        xor_1_gates = find_gates( "XOR", xor_1_wire, wires ) + find_gates( "AND", xor_1_wire, wires )
        c_in_gates = find_gates( "XOR", c_in, wires ) + find_gates( "AND", c_in, wires )
        if len(xor_1_gates) == 2 and len(c_in_gates) == 2 :
            raise RuntimeError( f"Full Adder: Cannot decide which wire is swapped between {xor_1_wire} and {c_in}" )
        elif len(xor_1_gates) == 2 :
            # xor_1_wire is correct, c_in is swapped
            print( f"{xor_1_wire} (xor 1) is correct, {c_in} (carry in) is swapped with another wire..." )
            correct_c_in = get_other_input( xor_1_gates[0], xor_1_wire )
            if correct_c_in != get_other_input( xor_1_gates[1], xor_1_wire ) :
                raise RuntimeError( f"Full Adder: Cannot find swapped wire for carry input {c_in}" )
            gates, wires = swap_wires( gates, wires, c_in, correct_c_in )
            swaps.append( ( c_in, correct_c_in ) )
            c_in = correct_c_in
        elif len(c_in_gates) == 2 :
            # c_in is correct, xor_1_wire is swapped
            print( f"{c_in} (carry in) is correct, {xor_1_wire} (xor 1) is swapped with another wire..." )
            correct_xor_1_wire = get_other_input( c_in_gates[0], c_in )
            if correct_xor_1_wire != get_other_input( c_in_gates[1], c_in ) :
                raise RuntimeError( f"Full Adder: Cannot find swapped 'out wire' for xor_1 gate {xor_1_gate}, {xor_1_wire}" )
            gates, wires = swap_wires( gates, wires, xor_1_wire, correct_xor_1_wire )
            swaps.append( ( xor_1_wire, correct_xor_1_wire ) )
            xor_1_wire = correct_xor_1_wire
        else :
            raise RuntimeError( f"Full Adder: Cannot find 2 alternatove gates for {xor_1_wire} or {c_in}" )
        print( f"Remaking Z out gate" )
        z_gate = Gate( "XOR", xor_1_wire, c_in )
        z_actual_wire = get_wire( z_gate, wires )
        print( f"Remaking AND 2 gate" )
        and_2_gate = Gate( "AND", xor_1_wire, c_in )
        and_2_wire = get_wire( and_2_gate, wires )
    gates, wires, swaps, swapped = check_expected_wire( z_actual_wire, z_expected_wire, gates, wires, swaps )
    if swapped :
        print( f"Remaking AND 2 gate" )
        and_2_gate = Gate( "AND", xor_1_wire, c_in )
        and_2_wire = get_wire( and_2_gate, wires )
    # Carry out
    print( f"Making AND 1 gate" )
    and_1_gate = Gate( "AND", x_in, y_in )
    and_1_wire = get_wire( and_1_gate, wires )
    print( f"Making C out gate" )
    c_gate = Gate( "OR", and_1_wire, and_2_wire )
    try :
        c_wire = get_wire( c_gate, wires )
    except KeyError :
        # c_gate & does not exists
        # either and_1_wire or and_2_wore is false
        print( f"Either {and_1_wire} (and 1) or {and_2_wire} (and 2) is swapped with another wire..." )
    full_adder = FullAdder( index, x_in, y_in, c_in, WiredGate( xor_1_gate, xor_1_wire )
                           , WiredGate( z_gate, z_expected_wire ), WiredGate( and_1_gate, and_1_wire )
                           , WiredGate( and_2_gate, and_2_wire ), WiredGate( c_gate, c_wire ) )
    #print( f"{full_adder}" )
    return swaps, full_adder

def fix_gates( original_gates: dict[ str, Gate ], inputs: dict[ str, int ], bits: int ) :
    swaps = []
    wires: dict[ Gate, str ] = dict()
    for out, gate in original_gates.items() :
        wires[ gate ] = out
    new_gates = original_gates.copy()

    swaps, last_adder = get_half_adder( 0, new_gates, wires )
    valid_adders = []

    for index in range( 1, bits ) :
        new_swaps, next_adder = get_full_adder( index, last_adder.c_out.wire, new_gates, wires )
        last_adder.c_out.wire = next_adder.c_in
        swaps = swaps + new_swaps
        valid_adders.append( last_adder )
        last_adder = next_adder
    valid_adders.append( last_adder )

    print()
    #print( "*** Adders tower ***")
    #for adder in valid_adders :
    #    print( f"{adder}" )
    #print()
    print( f"Swaps found: {swaps}" )
    return swaps, new_gates

def solve_gates( z: list[str], gates: dict[ str, Gate], inputs: dict[ str, int] , verbose: bool ) :
    z_output = ""
    solved = inputs.copy()
    for name in z :
        z_output += str( solve( name, gates, solved, verbose ) )
    return int( z_output, base=2 )

def do_problem( str_data: str, bits: int, verbose: bool = False ) :
    x_decimal, y_decimal, z, gates, inputs = parse_data( str_data, verbose )
    z_expected = x_decimal + y_decimal

    z_decimal = solve_gates( z, gates, inputs, verbose )
    print( f"x input:   {bin(x_decimal)} = {x_decimal}" )
    print( f"y input:   {bin(y_decimal)} = {y_decimal}" )
    print( f"z output: {bin(z_decimal)} = {z_decimal}" )
    print( f"expected: {bin(z_expected)} = {z_expected}" )

    swaps, new_gates = fix_gates( gates, inputs, bits )
    print()

    z_decimal = solve_gates( z, new_gates, inputs, verbose )
    print( f"x input:   {bin(x_decimal)} = {x_decimal}" )
    print( f"y input:   {bin(y_decimal)} = {y_decimal}" )
    print( f"z output: {bin(z_decimal)} = {z_decimal}" )
    print( f"expected: {bin(z_expected)} = {z_expected}" )

    print()
    result = sorted( wire for swap in swaps for wire in swap )
    str_result = ",".join( result )
    print( f"Answer: {str_result}")
    print( f"END" )

def do_tests( i: int = None ) :
    str_data = get_file_content( get_test_file_path( i ) )
    do_problem( str_data, 45, True )

def do_input() :
    str_data = get_file_content( get_input_file_path() )
    do_problem( str_data, 45, False )

def main() :
    start = time.time()
    #do_tests(1)
    #do_tests(2)
    #do_tests(3)
    #do_tests(4)
    #do_tests(5)
    #do_tests()
    do_input()
    elapsed = time.time() - start
    print( f"Total execution time: {elapsed:.3f} s" )

main()
