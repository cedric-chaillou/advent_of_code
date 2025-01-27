#!/usr/bin/env python3

import time
from dataclasses import dataclass
from typing import Union
import re

def get_test_file_path( i: int = None ) -> str :
    return "tests.txt" if i is None else f"tests_{i}.txt"

def get_input_file_path() -> str :
    return "input.txt"

def get_file_content( file_path: str ) -> str :
    with open( file_path, 'r' ) as f :
        data = f.read()
    return data

@dataclass
class Signal :
    wire: str
    value: int = None
    
    def get( self ) -> int :
        if self.value is None :
            self.value = solve( self.wire )
        return self.value

    def set( self, value ) :
        self.value = value

@dataclass
class BinaryGate :
    op: str
    in1: Signal
    in2: Signal
    out: Signal
    
    def solve( self) -> int :
        value_1 = self.in1.get()
        value_2 = self.in2.get()
        if self.op == "AND" :
            value = value_1 & value_2
        elif self.op == "OR" :
            value = value_1 | value_2
        elif self.op == "LSHIFT" :
            value = value_1 << value_2
        elif self.op == "RSHIFT" :
            value = value_1 >> value_2
        else :
            raise ValueError( f"Unknown binary operation: {self.op}" )
        self.out.set( value )
        return value

@dataclass
class UnaryGate :
    op: str
    in_: Signal
    out: Signal
    
    def solve( self ) -> int :
        value_in = self.in_.get()
        if self.op == "NOT" :
            value_out = MAX_VALUE ^ value_in
        else :
            raise ValueError( f"Unknown unary operation: {self.op}" )
        self.out.set( value_out )
        return value_out

@dataclass
class WireGate :
    in_: Signal
    out: Signal
    
    def solve( self) -> int :
        value = self.in_.get()
        self.out.set( value )
        return value

MAX_VALUE = 65535 # 2**16 - 1
Gate = Union[ BinaryGate, UnaryGate, WireGate ]
gates: dict[ str, Gate ] = dict()
signals: dict[ str, Signal ] = dict()

BINARY_GATE_RE = re.compile( r"(?P<in1>[a-z0-9]+) (?P<op>[A-Z]+) (?P<in2>[a-z0-9]+) -> (?P<out>[a-z]+)" )
UNARY_GATE_RE = re.compile( r"(?P<op>[A-Z]+) (?P<in_>[a-z0-9]+) -> (?P<out>[a-z]+)" )
WIRE_GATE_RE = re.compile( r"(?P<in_>[a-z0-9]+) -> (?P<out>[a-z]+)" )

def get_signal( wire: str ) -> Signal :
    global signals
    value = int( wire ) if wire.isdigit() else None
    if wire not in signals :
        signals[wire] = Signal( wire, value )
    return signals[wire]

def solve( wire: str ) -> int:
    if wire.isdigit() :
        return int( wire )
    gate = gates[wire]
    return gate.solve()

def parse_data( str_data: str, verbose: bool = False ) :
    global gates
    for line in str_data.strip().split( "\n" ) :
        match = BINARY_GATE_RE.match( line )
        if match is not None :
            op = match.group( "op" )
            in1 = match.group( "in1" )
            in2 = match.group( "in2" )
            out = match.group( "out" )
            gates[out] = BinaryGate( op, get_signal( in1 ), get_signal( in2 ), get_signal( out ) )
            if verbose:
                print( f"{out}: {gates[out]}" )
            continue
        match = UNARY_GATE_RE.match( line )
        if match is not None :
            op = match.group( "op" )
            in_ = match.group( "in_" )
            out = match.group( "out" )
            gates[out] = UnaryGate( op, get_signal( in_ ), get_signal( out ) )
            if verbose:
                print( f"{out}: {gates[out]}" )
            continue
        match = WIRE_GATE_RE.match( line )
        if match is not None :
            in_ = match.group( "in_" )
            out = match.group( "out" )
            gates[out] = WireGate( get_signal( in_ ), get_signal( out ) )
            if verbose:
                print( f"{out}: {gates[out]}" )
            continue
        raise ValueError( f"Invalid line: {line}" )
    print( f"{len(gates.keys())} gates parsed" )
    print( f"{len(signals.keys())} signals parsed" )

def do_problem( str_data: str, wires: str = None, override: str = None, verbose = False ) :
    parse_data( str_data, verbose )
    if wires is None :
        wires = " ".join( gates.keys() )
    for wire in wires.split() :
        print( f"{wire}: {solve( wire )}" )
    if override is not None :
        exit_wire = wires
        print( f"Overriding {override} with value from {exit_wire}..." )
        override_value = signals[exit_wire].get()
        for signal in signals.values() :
            signal.set( override_value if signal.wire == override else None )
        print( f"{exit_wire}: {solve( exit_wire )}" )
    print( f"END" )

def do_tests( i: int = None ) :
    str_data = get_file_content( get_test_file_path( i ) )
    do_problem( str_data, None, None, True )

def do_input() :
    str_data = get_file_content( get_input_file_path() )
    do_problem( str_data, "a", "b", False )

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
