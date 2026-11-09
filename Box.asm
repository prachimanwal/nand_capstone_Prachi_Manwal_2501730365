// Box.asm
// Name: Prachi Manwal
// Roll No: 2501730365 (K = 65)
// Starts at row 65 (SCREEN + 32*65 = 16384 + 2080 = 18464)
// Height = 20 rows, Width = 16 * ((65 mod 4) + 1) = 32 pixels (2 words)

(LOOP)
    @KBD
    D=M
    @KEY_PRESSED
    D;JNE

(KEY_RELEASED)
    @color
    M=0
    @INIT_BOX
    0;JMP

(KEY_PRESSED)
    @color
    M=-1

(INIT_BOX)
    @SCREEN
    D=A
    @2080
    D=D+A
    @addr
    M=D

    @20
    D=A
    @rows
    M=D

(ROW_LOOP)
    @rows
    D=M
    @LOOP
    D;JEQ

    @color
    D=M

    @addr
    A=M
    M=D
    A=A+1
    M=D

    @32
    D=A
    @addr
    M=D+M

    @rows
    M=M-1
    @ROW_LOOP
    0;JMP
