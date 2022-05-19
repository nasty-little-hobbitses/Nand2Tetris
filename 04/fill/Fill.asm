// This file is part of www.nand2tetris.org
// and the book "The Elements of Computing Systems"
// by Nisan and Schocken, MIT Press.
// File name: projects/04/Fill.asm

// Runs an infinite loop that listens to the keyboard input.
// When a key is pressed (any key), the program blackens the screen,
// i.e. writes "black" in every pixel;
// the screen should remain fully black as long as the key is pressed. 
// When no key is pressed, the program clears the screen, i.e. writes
// "white" in every pixel;
// the screen should remain fully clear as long as no key is pressed.

// Put your code here.

(LOOP)
    @KBD //getting keyboard value and setting it to M
    D = M

    // if keyboard value > 0, ON, else OFF
    @ON
    D;JGT 

    @OFF
    0;JMP

(ON)
    @R0
    M = -1

    // BLACKEN.
    @BLACKEN
    0;JMP

(OFF)
    @R0
    M = 0

    // BLACKEN.
    @BLACKEN
    0;JMP

// Set the screen to R0 and loop.
(BLACKEN)
    @8191
    D = A
    @R1
    M = D

    (NEXT)
        @R1
        D = M
        @pixel
        M = D
        @SCREEN
        D = A
        @pixel
        M = M + D

        @R0
        D = M
        @pixel
        A = M
        M = D

        @R1
        D = M - 1
        M = D

        @NEXT
        D;JGE

    @LOOP // to keep the system running, infinite loop
    0;JMP