#!/usr/bin/env python3

import time
from collections import namedtuple
import re
from typing import Callable

def get_test_file_path( i = None ) :
    return "tests.txt" if i is None else f"tests_{i}.txt"

def get_input_file_path() :
    return "input.txt"

def get_file_content( file_path ) :
    with open( file_path, 'r' ) as f :
        data = f.read()
    return data

class Computer:
    def __init__( self, A: int, B: int, C: int, program: str ) :
        self.a: int = A
        self.b: int = B
        self.c: int = C
        self.__program: tuple[int] = tuple( int(s) for s in program.split( "," ) )
        self.__output: list[int] = []
        self.__curser: int = 0

    @property
    def program( self ) -> str:
        """The program string of instructions and operands, joined with commas"""
        return ",".join( str(i) for i in self.__program )

    @property
    def output( self ) -> str:
        """The output string produced by out instructions, joined with commas"""
        return ",".join( str(i) for i in self.__output )

    @property
    def is_running( self ) -> bool :
        """True if the program is still running, False otherwise"""
        # nota: we must always be able to read 2 values at the end of the program
        return self.__curser >= 0 and self.__curser < len( self.__program ) - 1

    @property
    def is_halted( self ) -> bool :
        """True if the program is halted, False otherwise"""
        return not self.is_running

    def print( self ) :
        print()
        print( "*** Computer ***" )
        print()
        print( f"Register A: {self.a}" )
        print( f"Register B: {self.b}" )
        print( f"Register C: {self.c}" )
        print()
        print( f"Program: {self.program}" )
        print()
        print( f"State: {'HALTED' if self.is_halted else 'RUNNING'}, curser @{self.__curser}" )
        print( f"Output: {self.output}" )
        print()

    def run_program( self, verbose = False ) -> str :
        """
        Run the program recorded in the computer and returns its output

        Args:
            verbose (bool, optional): prints additionnal messages, for debug purposes. Defaults to False.

        Returns:
            str: the output of the program
            (if the program outputs multiple values, they are separated by commas)
        """
        print( f"Starting program, starting curser @{self.__curser} ..." )
        while self.is_running :
            instruction, operand = self.read()
            if verbose :
                print( f"Reading: Instruction = {instruction}, Operand = {operand}" )
            self.execute( instruction, operand )
            if verbose :
                print( f"Curser @{self.__curser}, Output length: {len(self.__output)}" )
        print( f"Program halted with curser @{self.__curser}, Output length: {len(self.__output)}" )
        return self.output

    def read( self ) -> tuple[ int, int ]:
        """
        Reads the instruction and operand at the curser place in the program,
        then advance the curser to the next instruction

        Returns:
            tuple[ int, int ]: the instruction and its operand
        """
        if self.is_running :
            self.__curser += 2
            return ( self.__program[ self.__curser - 2 ], self.__program[ self.__curser - 1 ] )
        else :
            return ( None, None )

    def execute( self, instruction: int, operand: int ) -> None :
        """
        Execute the instruction from the program, with its operand

        Args:
            instruction (int): the instruction to execute
            operand (int): the operand to pass to the instruction as its argument
        """
        self.__get_method( instruction )( operand )

    def __get_method( self, instruction: int ) -> Callable[ [ 'Computer', int ], None ] :
        """
        Returns the method to call to execute the instruction
        
        Warning: the method will need to be called with "self" as its 1st argument

        Raises:
            ValueError: Error if the instruction is not an integer between 0 and 7

        Returns:
            ((Computer, int) -> None): the method to call to execute the instruction
        """
        methods = ( self.adv, self.bxl, self.bst, self.jnz, self.bxc, self.out, self.bdv, self.cdv )
        if instruction < 0 or instruction >= len( methods ) :
            raise ValueError( f"Invalid instruction value {instruction}" )
        return methods[ instruction ]

    def __combo( self, combo_operand: int ) -> int :
        """
        The value of a combo operand can be found as follows:
            - Combo operands 0 through 3 represent literal values 0 through 3.
            - Combo operand 4 represents the value of register A.
            - Combo operand 5 represents the value of register B.
            - Combo operand 6 represents the value of register C.

        Args:
            operand (int): _description_

        Raises:
            ValueError: Error if the operand is not an integer between 0 and 6
            (Combo operand 7 is reserved and will not appear in valid programs)

        Returns:
            int: the "literal" operand value to use as argument for the instruction
        """
        if combo_operand == 4 :
            return self.a
        elif combo_operand == 5 :
            return self.b
        elif combo_operand == 6 :
            return self.c
        elif combo_operand in ( 0, 1, 2, 3 ) :
            return combo_operand
        else :
            raise ValueError( f"Invalid value {combo_operand} for combo operand" )

    def __divide_a( self, literal_operand: int ) -> int :
        """
        Performs division.
            - The numerator is the value in the A register.
            - The denominator is found by raising 2 to the power of the "literal" operand.

        Args:
            literal_operand (int): "literal" operand

        Returns:
            int: the result of the division operation, truncated to an integer
        """
        return self.a >> literal_operand

    def __xor_b( self, literal_operand: int ) -> int :
        """
        Returns the result of a binary XOR between regster B and "literal" operand

        Args:
            literal_operand (int): "literal" operand

        Returns:
            int: the result of the binary XOR operation
        """
        return self.b ^ literal_operand

    def __mod_8( self, literal_operand: int ) -> int :
        """
        Calculates the value of its "literal" operand modulo 8 (thereby keeping only its lowest 3 bits)

        Args:
            literal_operand (int): "literal" operand

        Returns:
            int: the result of the 
        """
        return literal_operand & 7

    def adv( self, operand: int ) -> None :
        """
        Instruction (opcode 0)

        Performs division.
            - The numerator is the value in the A register.
            - The denominator is found by raising 2 to the power of the instruction's combo operand.
            - The result of the division operation is truncated to an integer
                and then written to the A register

        Args:
            operand (int): combo operand
        """
        self.a = self.__divide_a( self.__combo( operand ) )

    def bxl( self, operand: int ) -> None :
        """
        Instruction (opcode 1)

        Calculates the bitwise XOR of register B and the instruction's "literal" operand,
        then stores the result in register B

        Args:
            operand (int): "literal" operand
        """
        self.b = self.__xor_b( operand )

    def bst( self, operand: int ) -> None :
        """
        Instruction (opcode 2)

        Calculates the value of its combo operand modulo 8 (thereby keeping only its lowest 3 bits),
        then writes that value to the B register

        Args:
            operand (int): combo operand
        """
        self.b = self.__mod_8( self.__combo( operand ) )

    def jnz( self, operand: int ) -> None :
        """
        Instruction (opcode 3)

        Does nothing if the A register is 0.

        However, if the A register is not zero:
        it jumps by setting the instruction pointer to the value of its literal operand

        If this instruction jumps, the instruction pointer is not increased by 2 after this instruction.

        Args:
            operand (int): the next instruction new address
        """
        if self.a != 0 :
            self.__curser = operand

    def bxc( self, operand: int ) -> None :
        """
        Instruction (opcode 4)

        Calculates the bitwise XOR of register B and register C,
        then stores the result in register B.

        Args:
            operand (int): For legacy reasons, this instruction reads an operand but ignores it.
        """
        self.b = self.__xor_b( self.c )

    def out( self, operand: int ) -> None :
        """
        Instruction (opcode 5)

        Calculates the value of its combo operand modulo 8, then outputs that value

        Args:
            operand (int): combo operand
        """
        self.__output.append( self.__mod_8( self.__combo( operand ) ) )

    def bdv( self, operand: int ) -> None :
        """
        Instruction (opcode 6)

        Performs division.
            - The numerator is the value in the A register.
            - The denominator is found by raising 2 to the power of the instruction's combo operand.
            - The result of the division operation is truncated to an integer
                and then written to the B register

        Args:
            operand (int): combo operand
        """
        self.b = self.__divide_a( self.__combo( operand ) )

    def cdv( self, operand: int ) -> None :
        """
        Instruction (opcode 7)

        Performs division.
            - The numerator is the value in the A register.
            - The denominator is found by raising 2 to the power of the instruction's combo operand.
            - The result of the division operation is truncated to an integer
                and then written to the C register

        Args:
            operand (int): combo operand
        """
        self.c = self.__divide_a( self.__combo( operand ) )

REGISTER_RE = re.compile( r"Register (?P<name>\w+): (?P<value>\d+)" )
PROGRAM_RE = re.compile( r"Program: (?P<program>[0-7](?:,[0-7])*)" )

def parse_data( str_data: str, verbose: bool = False ) :
    setup = {}
    for i, line in enumerate( str_data.split( "\n" ) ) :
        if verbose :
            print( f"Line #{i}: {line}" )
        match = REGISTER_RE.match( line )
        if match is not None :
            name = match.groupdict()[ "name" ]
            value = int( match.groupdict()[ "value" ] )
            if verbose :
                print( f"Register {name}: {value}" )
            setup[ name ] = value
            continue
        match = PROGRAM_RE.match( line )
        if match is not None :
            program = match.groupdict()[ "program" ]
            if verbose :
                print( f"Program: {program}" )
            setup[ "program" ] = program
            continue
    computer = Computer( **setup )
    computer.print()
    return computer

def do_problem( str_data: str, verbose = False ) :
    computer = parse_data( str_data, verbose )
    output = computer.run_program( verbose )
    if verbose :
        computer.print()
    print( f"Program output: {output}" )
    print( f"END" )

def do_tests( i = None ) :
    str_data = get_file_content( get_test_file_path( i ) )
    do_problem( str_data, True )

def do_input() :
    str_data = get_file_content( get_input_file_path() )
    do_problem( str_data, False )

def test_computer() :
    computer = Computer( 15, 0, 0, "1,6" )
    computer.print()
    computer.bdv( 2 )
    computer.cdv( 3 )
    computer.adv( 1 )
    print( f"computer.a = {computer.a}" )
    computer.print()
    

def main() :
    start = time.time()
    #test_computer()
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
