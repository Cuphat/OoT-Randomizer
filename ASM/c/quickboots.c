#include "gfx.h"
#include "quickboots.h"

static uint16_t pad_pressed_raw,
pad,
pad_pressed;

static _Bool display_active;

typedef struct {
    uint8_t age;
    uint16_t search;
    uint16_t repl;
}age_swap_table_t;

static age_swap_table_t age_swap_table[8] = {
    {1,0x05E8,0x0209},
    {1,0x05E9,0x0209},
    {1,0x05EA,0x0209},
    {1,0x05EB,0x0209},
    {1,0x0580,0x0205},
    {1,0x0581,0x0205},
    {1,0x0582,0x0205},
    {1,0x0583,0x0205}
};

void handle_quickboots() {
    uint16_t z_pad = z64_ctxt.input[0].raw.pad;
    pad_pressed_raw = (pad ^ z_pad) & z_pad;
    pad = z_pad;
    pad_pressed = 0;
    pad_pressed |= pad_pressed_raw;

    if (CAN_USE_QUICKBOOTS) {
        if (pad_pressed & DPAD_U) {
            z64_game.link_age = !z64_game.link_age;

            uint16_t entrance = z64_file.entrance_index;
            for (int i = 0; i < sizeof(age_swap_table) / sizeof(age_swap_table_t); i++) {
                if (z64_game.link_age == age_swap_table[i].age && age_swap_table[i].search == entrance) {
                    entrance = age_swap_table[i].repl;
                    break;
                }
            }
            z64_game.entrance_index = entrance;
            z64_game.scene_load_flag = 0x14;
        }
        if (pad_pressed & DPAD_L && z64_file.iron_boots) {
            if (z64_file.equip_boots == 2) z64_file.equip_boots = 1;
            else z64_file.equip_boots = 2;
            z64_UpdateEquipment(&z64_game, &z64_link);
        }

        if ((pad_pressed & DPAD_R) && z64_file.hover_boots) {
            if (z64_file.equip_boots == 3) z64_file.equip_boots = 1;
            else z64_file.equip_boots = 3;
            z64_UpdateEquipment(&z64_game, &z64_link);
        }
    }
    if (pad_pressed & DPAD_D) {
        display_active = !display_active;
    }
}

void draw_quickboots(z64_disp_buf_t *db) {
    if (CAN_USE_QUICKBOOTS && display_active) {
        gSPDisplayList(db->p++, setup_db.buf);
        gDPPipeSync(db->p++);
        gDPSetCombineMode(db->p++, G_CC_MODULATEIA_PRIM, G_CC_MODULATEIA_PRIM);
        gDPSetPrimColor(db->p++, 0, 0, 0xFF, 0xFF, 0xFF, 0xFF);

        sprite_load(db, &dpad_sprite, 0, 1);
        sprite_draw(db, &dpad_sprite, 0, 269, 60, 8, 8);

        sprite_load(db, &dpad_sprite, 1, 1);
        sprite_draw(db, &dpad_sprite, 0, 277, 60, 8, 8);

        sprite_load(db, &dpad_sprite, 2, 1);
        sprite_draw(db, &dpad_sprite, 0, 269, 68, 8, 8);

        sprite_load(db, &dpad_sprite, 3, 1);
        sprite_draw(db, &dpad_sprite, 0, 277, 68, 8, 8);

        if (z64_file.iron_boots) {
            sprite_load(db, &items_sprite, 69, 1);
            if (z64_file.equip_boots == 2) {
                sprite_draw(db, &items_sprite, 0, 257, 61, 12, 12);
            }
            else {
                sprite_draw(db, &items_sprite, 0, 258, 62, 10, 10);
            }
        }

        if (z64_file.hover_boots) {
            sprite_load(db, &items_sprite, 70, 1);
            if (z64_file.equip_boots == 3) {
                sprite_draw(db, &items_sprite, 0, 287, 61, 12, 12);
            }
            else {
                sprite_draw(db, &items_sprite, 0, 286, 62, 10, 10);
            }
        }

        gDPFullSync(db->p++);
        gSPEndDisplayList(db->p++);
    }
}

void quickboots_init() {
    pad_pressed_raw = 0;
    pad = 0;
    pad_pressed = 0;
    display_active = 1;
}