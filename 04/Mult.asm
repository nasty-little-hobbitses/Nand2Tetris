// This file is part of www.nand2tetris.org
// and the book "The Elements of Computing Systems"
// by Nisan and Schocken, MIT Press.
// File name: projects/04/Mult.asm

// Multiplies R0 and R1 and stores the result in R2.
// (R0, R1, R2 refer to RAM[0], RAM[1], and RAM[2], respectively.)
//
// This program only needs to handle arguments that satisfy
// R0 >= 0, R1 >= 0, and R0*R1 < 32768.

// Put your code here.

@R2 //setting R2 to 0
M = 0

@R0
D = M
@STEP
D;JGT //if R0 > 0, else END

@END
0;JMP


(STEP)
    @R2 //setting R2 to M
    D = M

    @R1 // adding R1 val to R2
    D = D + M

    @R2 // storing value in R2
    M = D

    // Reduce R0 by 1.
    @R0 
    D = M - 1
    M = D

    @STEP // continue iteration if R0 > 0
    D;JGT

(END)
    @END
    0;JMP // to keep system running hence infinite loop