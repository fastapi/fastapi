;
; stack switching code for MASM on x641
; Kristjan Valur Jonsson, sept 2005
;


;prototypes for our calls
slp_save_state_asm PROTO
slp_restore_state_asm PROTO


pushxmm MACRO reg
    sub rsp, 16
    .allocstack 16
    movaps [rsp], reg ; faster than movups, but we must be aligned
    ; .savexmm128 reg, offset  (don't know what offset is, no documentation)
ENDM
popxmm MACRO reg
    movaps reg, [rsp] ; faster than movups, but we must be aligned
    add rsp, 16
ENDM

pushreg MACRO reg
    push reg
    .pushreg reg
ENDM
popreg MACRO reg
    pop reg
ENDM


.code
slp_switch PROC FRAME
    ;realign stack to 16 bytes after return address push, makes the following faster
    sub rsp,8
    .allocstack 8

    pushxmm xmm15
    pushxmm xmm14
    pushxmm xmm13
    pushxmm xmm12
    pushxmm xmm11
    pushxmm xmm10
    pushxmm xmm9
    pushxmm xmm8
    pushxmm xmm7
    pushxmm xmm6

    pushreg r15
    pushreg r14
    pushreg r13
    pushreg r12

    pushreg rbp
    pushreg rbx
    pushreg rdi
    pushreg rsi

    sub rsp, 10h ;allocate the singlefunction argument (must be multiple of 16)
    .allocstack 10h
.endprolog

    lea rcx, [rsp+10h] ;load stack base that we are saving
    call slp_save_state_asm ;pass stackpointer, return offset in eax
    cmp rax, 1
    je EXIT1
    cmp rax, -1
    je EXIT2
    ;actual stack switch:
    add rsp, rax
    call slp_restore_state_asm
    xor rax, rax ;return 0

EXIT:

    add rsp, 10h
    popreg rsi
    popreg rdi
    popreg rbx
    popreg rbp

    popreg r12
    popreg r13
    popreg r14
    popreg r15

    popxmm xmm6
    popxmm xmm7
    popxmm xmm8
    popxmm xmm9
    popxmm xmm10
    popxmm xmm11
    popxmm xmm12
    popxmm xmm13
    popxmm xmm14
    popxmm xmm15

    add rsp, 8
    ret

EXIT1:
    mov rax, 1
    jmp EXIT

EXIT2:
    sar rax, 1
    jmp EXIT

slp_switch ENDP

END