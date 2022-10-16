potion_shop_fix:
    addiu   sp, sp, -0x20
    sw      v0, 0x08(sp)
    sw      s0, 0x0C(sp)
    sw      v1, 0x10(sp)
    sw      a0, 0x14(sp)
    sw      a1, 0x18(sp)
    sw      ra, 0x1C(sp)

    jal     SaveFile_TradeItemIsTraded
    ori     a0, $zero, 0x30
    or      t9, v0, $zero

    lw      v0, 0x08(sp)
    lw      s0, 0x0C(sp)
    lw      v1, 0x10(sp)
    lw      a0, 0x14(sp)
    lw      a1, 0x18(sp)
    lw      ra, 0x1C(sp)
    jr      ra
    addiu   sp, sp, 0x20