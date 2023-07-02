  AREA switch_arm64_masm, CODE, READONLY;
  GLOBAL slp_switch [FUNC]
  EXTERN slp_save_state_asm
  EXTERN slp_restore_state_asm

slp_switch    
    ; push callee saved registers to stack
    stp    x19, x20, [sp, #-16]!
    stp    x21, x22, [sp, #-16]!
    stp    x23, x24, [sp, #-16]!
    stp    x25, x26, [sp, #-16]!
    stp    x27, x28, [sp, #-16]!
    stp    x29, x30, [sp, #-16]!
    stp    d8, d9, [sp, #-16]!
    stp    d10, d11, [sp, #-16]!
    stp    d12, d13, [sp, #-16]!
    stp    d14, d15, [sp, #-16]!

    ; call slp_save_state_asm with stack pointer
    mov x0, sp
    bl    slp_save_state_asm

    ; early return for return value of 1 and -1
    cmp x0, #-1
    b.eq RETURN
    cmp x0, #1
    b.eq RETURN

    ; increment stack and frame pointer
    add sp, sp, x0
    add x29, x29, x0

    bl slp_restore_state_asm

    ; store return value for successful completion of routine
    mov x0, #0

RETURN
    ; pop registers from stack
    ldp d14, d15, [sp], #16
    ldp d12, d13, [sp], #16
    ldp d10, d11, [sp], #16
    ldp d8, d9, [sp], #16
    ldp x29, x30, [sp], #16
    ldp x27, x28, [sp], #16
    ldp x25, x26, [sp], #16
    ldp x23, x24, [sp], #16
    ldp x21, x22, [sp], #16
    ldp x19, x20, [sp], #16

    ret

    END
