import logging
import random
from Utils import random_choices
from Item import ItemFactory
from ItemList import item_table
from decimal import Decimal, ROUND_HALF_UP


# Generates item pools and places fixed items based on settings.

plentiful_items = ([
    'Biggoron Sword',
    'Boomerang',
    'Lens of Truth',
    'Megaton Hammer',
    'Iron Boots',
    'Goron Tunic',
    'Zora Tunic',
    'Hover Boots',
    'Mirror Shield',
    'Fire Arrows',
    'Light Arrows',
    'Dins Fire',
    'Progressive Hookshot',
    'Progressive Strength Upgrade',
    'Progressive Scale',
    'Progressive Wallet',
    'Magic Meter',
    'Deku Stick Capacity', 
    'Deku Nut Capacity', 
    'Bow', 
    'Slingshot', 
    'Bomb Bag',
    'Double Defense'] +
    ['Heart Container'] * 8)

item_difficulty_max = {
    'vanilla': {},
    'plentiful': {
        'Piece of Heart': 3,
    },
    'balanced': {},
    'scarce': {
        'Bombchus': 3,
        'Bombchus (5)': 1,
        'Bombchus (10)': 2,
        'Bombchus (20)': 0,
        'Magic Meter': 1, 
        'Double Defense': 0, 
        'Deku Stick Capacity': 1, 
        'Deku Nut Capacity': 1, 
        'Bow': 2, 
        'Slingshot': 2, 
        'Bomb Bag': 2,
        'Heart Container': 0,
    },
    'minimal': {
        'Bombchus': 1,
        'Bombchus (5)': 1,
        'Bombchus (10)': 0,
        'Bombchus (20)': 0,
        'Magic Meter': 1, 
        'Nayrus Love': 1,
        'Double Defense': 0, 
        'Deku Stick Capacity': 0, 
        'Deku Nut Capacity': 0, 
        'Bow': 1, 
        'Slingshot': 1, 
        'Bomb Bag': 1,
        'Heart Container': 0,
        'Piece of Heart': 0,
    },
}

TriforceCounts = {
    'plentiful': Decimal(2.00),
    'balanced':  Decimal(1.50),
    'scarce':    Decimal(1.25),
    'minimal':   Decimal(1.00),
}

normal_bottles = [
    'Bottle',
    'Bottle with Milk',
    'Bottle with Red Potion',
    'Bottle with Green Potion',
    'Bottle with Blue Potion',
    'Bottle with Fairy',
    'Bottle with Fish',
    'Bottle with Bugs',
    'Bottle with Poe',
    'Bottle with Big Poe',
    'Bottle with Blue Fire']

dungeon_rewards = [
    'Kokiri Emerald',
    'Goron Ruby',
    'Zora Sapphire',
    'Forest Medallion',
    'Fire Medallion',
    'Water Medallion',
    'Shadow Medallion',
    'Spirit Medallion',
    'Light Medallion'
]

shopsanity_rupees = (
    ['Rupees (20)'] * 5 +
    ['Rupees (50)'] * 3 +
    ['Rupees (200)'] * 2)

min_shop_items = (
    ['Buy Deku Shield'] +
    ['Buy Hylian Shield'] +
    ['Buy Goron Tunic'] +
    ['Buy Zora Tunic'] +
    ['Buy Deku Nut (5)'] * 2 + ['Buy Deku Nut (10)'] +
    ['Buy Deku Stick (1)'] * 2 +
    ['Buy Deku Seeds (30)'] +
    ['Buy Arrows (10)'] * 2 + ['Buy Arrows (30)'] + ['Buy Arrows (50)'] +
    ['Buy Bombchu (5)'] + ['Buy Bombchu (10)'] * 2 + ['Buy Bombchu (20)'] +
    ['Buy Bombs (5) [25]'] + ['Buy Bombs (5) [35]'] + ['Buy Bombs (10)'] + ['Buy Bombs (20)'] +
    ['Buy Green Potion'] +
    ['Buy Red Potion [30]'] +
    ['Buy Blue Fire'] +
    ["Buy Fairy's Spirit"] +
    ['Buy Bottle Bug'] +
    ['Buy Fish'])

deku_scrubs_items = {
    'Buy Deku Shield': 'Deku Shield',
    'Buy Deku Nut (5)': 'Deku Nuts (5)',
    'Buy Deku Stick (1)': 'Deku Stick (1)',
    'Buy Bombs (5) [35]': 'Bombs (5)',
    'Buy Red Potion [30]': 'Recovery Heart',
    'Buy Green Potion': 'Rupees (5)',
    'Buy Arrows (30)': [('Arrows (30)', 3), ('Deku Seeds (30)', 1)],
    'Buy Deku Seeds (30)': [('Arrows (30)', 3), ('Deku Seeds (30)', 1)],
}

song_list = [
    'Zeldas Lullaby',
    'Eponas Song',
    'Suns Song',
    'Sarias Song',
    'Song of Time',
    'Song of Storms',
    'Minuet of Forest',
    'Prelude of Light',
    'Bolero of Fire',
    'Serenade of Water',
    'Nocturne of Shadow',
    'Requiem of Spirit']

trade_items = (
    'Pocket Egg',
    'Pocket Cucco',
    'Cojiro',
    'Odd Mushroom',
    'Poachers Saw',
    'Broken Sword',
    'Prescription',
    'Eyeball Frog',
    'Eyedrops',
    'Claim Check')

trade_item_options = (
    'pocket_egg',
    'pocket_cucco',
    'cojiro',
    'odd_mushroom',
    'poachers_saw',
    'broken_sword',
    'prescription',
    'eyeball_frog',
    'eyedrops',
    'claim_check')

junk_pool_base = [
    ('Bombs (5)',       8),
    ('Bombs (10)',      2),
    ('Arrows (5)',      8),
    ('Arrows (10)',     2),
    ('Deku Stick (1)',  5),
    ('Deku Nuts (5)',   5),
    ('Deku Seeds (30)', 5),
    ('Rupees (5)',      10),
    ('Rupees (20)',     4),
    ('Rupees (50)',     1),
]

pending_junk_pool = []
junk_pool = []

remove_junk_items = [junk[0] for junk in junk_pool_base] + [
    'Recovery Heart',
    'Arrows (30)',
    'Rupees (200)',
    'Deku Nuts (10)',
    'Bombs (20)',
    'Ice Trap',
]
remove_junk_set = set(remove_junk_items)

exclude_from_major = [ 
    'Deliver Letter',
    'Sell Big Poe',
    'Magic Bean',
    'Zeldas Letter',
    'Bombchus (5)',
    'Bombchus (10)',
    'Bombchus (20)',
    'Odd Potion',
    'Triforce Piece'
]

item_groups = {
    'Junk': remove_junk_items,
    'JunkSong': ('Prelude of Light', 'Serenade of Water'),
    'AdultTrade': trade_items,
    'Bottle': normal_bottles,
    'Spell': ('Dins Fire', 'Farores Wind', 'Nayrus Love'),
    'Shield': ('Deku Shield', 'Hylian Shield'),
    'Song': song_list,
    'NonWarpSong': song_list[0:6],
    'WarpSong': song_list[6:],
    'HealthUpgrade': ('Heart Container', 'Piece of Heart'),
    'ProgressItem': [name for (name, data) in item_table.items() if data[0] == 'Item' and data[1]],
    'MajorItem': [name for (name, data) in item_table.items() if (data[0] == 'Item' or data[0] == 'Song') and data[1] and name not in exclude_from_major],
    'DungeonReward': dungeon_rewards,

    'ForestFireWater': ('Forest Medallion', 'Fire Medallion', 'Water Medallion'),
    'FireWater': ('Fire Medallion', 'Water Medallion'),
}


def get_junk_item(count=1, pool=None, plando_pool=None):
    if count < 1:
        raise ValueError("get_junk_item argument 'count' must be greater than 0.")

    return_pool = []
    if pending_junk_pool:
        pending_count = min(len(pending_junk_pool), count)
        return_pool = [pending_junk_pool.pop() for _ in range(pending_count)]
        count -= pending_count

    if pool and plando_pool:
        jw_list = [(junk, weight) for (junk, weight) in junk_pool
                   if junk not in plando_pool or pool.count(junk) < plando_pool[junk].count]
        try:
            junk_items, junk_weights = zip(*jw_list)
        except ValueError:
            raise RuntimeError("Not enough junk is available in the item pool to replace removed items.")
    else:
        junk_items, junk_weights = zip(*junk_pool)
    return_pool.extend(random_choices(junk_items, weights=junk_weights, k=count))

    return return_pool


def replace_max_item(items, item, max):
    count = 0
    for i,val in enumerate(items):
        if val == item:
            if count >= max:
                items[i] = get_junk_item()[0]
            count += 1


def generate_itempool(world):
    junk_pool[:] = list(junk_pool_base)
    if world.settings.junk_ice_traps == 'on':
        junk_pool.append(('Ice Trap', 10))
    elif world.settings.junk_ice_traps in ['mayhem', 'onslaught']:
        junk_pool[:] = [('Ice Trap', 1)]

    # set up item pool
    (pool, placed_items) = get_pool_core(world)
    world.itempool = ItemFactory(pool, world)
    placed_locations = list(filter(lambda loc: loc.name in placed_items, world.get_locations()))
    for location in placed_locations:
        world.push_item(location, ItemFactory(placed_items[location.name], world))
        world.get_location(location).locked = True

    world.initialize_items()
    world.distribution.set_complete_itempool(world.itempool)


def try_collect_heart_container(world, pool):
    if 'Heart Container' in pool:
        pool.remove('Heart Container')
        pool.extend(get_junk_item())
        world.state.collect(ItemFactory('Heart Container'))
        return True
    return False


def try_collect_pieces_of_heart(world, pool):
    n = pool.count('Piece of Heart') + pool.count('Piece of Heart (Treasure Chest Game)')
    if n >= 4:
        for i in range(4):
            if 'Piece of Heart' in pool:
                pool.remove('Piece of Heart')
                world.state.collect(ItemFactory('Piece of Heart'))
            else:
                pool.remove('Piece of Heart (Treasure Chest Game)')
                world.state.collect(ItemFactory('Piece of Heart (Treasure Chest Game)'))
            pool.extend(get_junk_item())
        return True
    return False


def collect_pieces_of_heart(world, pool):
    success = try_collect_pieces_of_heart(world, pool)
    if not success:
        try_collect_heart_container(world, pool)


def collect_heart_container(world, pool):
    success = try_collect_heart_container(world, pool)
    if not success:
        try_collect_pieces_of_heart(world, pool)


def get_pool_core(world):
    pool = []
    placed_items = {}
    remain_shop_items = []
    ruto_bottles = 1

    if world.settings.zora_fountain == 'open':
        ruto_bottles = 0

    if world.settings.shopsanity not in ['off', '0']:
        pending_junk_pool.append('Progressive Wallet')

    if world.settings.item_pool_value == 'plentiful':
        pending_junk_pool.extend(plentiful_items)
        if world.settings.zora_fountain != 'open':
            ruto_bottles += 1
        if world.settings.shuffle_kokiri_sword:
            pending_junk_pool.append('Kokiri Sword')
        if world.settings.shuffle_ocarinas:
            pending_junk_pool.append('Ocarina')
        if world.settings.shuffle_beans and world.distribution.get_starting_item('Magic Bean') < 10:
            pending_junk_pool.append('Magic Bean Pack')
        if (world.settings.gerudo_fortress != "open"
                and world.settings.shuffle_hideoutkeys in ['any_dungeon', 'overworld', 'keysanity']):
            if 'Thieves Hideout' in world.settings.key_rings and world.settings.gerudo_fortress != "fast":
                pending_junk_pool.extend(['Small Key Ring (Thieves Hideout)'])
            else:
                pending_junk_pool.append('Small Key (Thieves Hideout)')
        if world.settings.shuffle_gerudo_card:
            pending_junk_pool.append('Gerudo Membership Card')
        if world.settings.shuffle_smallkeys in ['any_dungeon', 'overworld', 'keysanity']:
            for dungeon in ['Forest Temple', 'Fire Temple', 'Water Temple', 'Shadow Temple', 'Spirit Temple',
                            'Bottom of the Well', 'Gerudo Training Ground', 'Ganons Castle']:
                if dungeon in world.settings.key_rings:
                    pending_junk_pool.append(f"Small Key Ring ({dungeon})")
                else:
                    pending_junk_pool.append(f"Small Key ({dungeon})")
        if world.settings.shuffle_bosskeys in ['any_dungeon', 'overworld', 'keysanity']:
            for dungeon in ['Forest Temple', 'Fire Temple', 'Water Temple', 'Shadow Temple', 'Spirit Temple']:
                pending_junk_pool.append(f"Boss Key ({dungeon})")
        if world.settings.shuffle_ganon_bosskey in ['any_dungeon', 'overworld', 'keysanity']:
            pending_junk_pool.append('Boss Key (Ganons Castle)')
        if world.settings.shuffle_song_items == 'any':
            pending_junk_pool.extend(song_list)

    if world.settings.triforce_hunt:
        triforce_count = int((TriforceCounts[world.settings.item_pool_value] * world.settings.triforce_goal_per_world).to_integral_value(rounding=ROUND_HALF_UP))
        pending_junk_pool.extend(['Triforce Piece'] * triforce_count)

    # Use the vanilla items in the world's locations when appropriate.
    for location in world.get_locations():
        if location.vanilla_item is None:
            continue

        item = location.vanilla_item
        shuffle_item = None  # None for don't handle, False for place item, True for add to pool.

        # Always Placed Items
        if (location.vanilla_item in ['Zeldas Letter', 'Triforce', 'Scarecrow Song',
                                      'Deliver Letter', 'Time Travel', 'Bombchu Drop']
                or location.type == 'Drop'):
            shuffle_item = False

        # Gold Skulltula Tokens
        elif location.vanilla_item == 'Gold Skulltula Token':
            shuffle_item = (world.settings.tokensanity == 'all'
                            or (world.settings.tokensanity == 'dungeons' and location.dungeon)
                            or (world.settings.tokensanity == 'overworld' and not location.dungeon))

        # Shops
        elif location.type == "Shop":
            if world.settings.shopsanity == 'off':
                if world.settings.bombchus_in_logic and location.name in ['KF Shop Item 8', 'Market Bazaar Item 4', 'Kak Bazaar Item 4']:
                    item = 'Buy Bombchu (5)'
                shuffle_item = False
            else:
                remain_shop_items.append(item)

        # Business Scrubs
        elif location.type in ["Scrub", "GrottoScrub"]:
            if location.vanilla_item in ['Piece of Heart', 'Deku Stick Capacity', 'Deku Nut Capacity']:
                shuffle_item = not world.settings.item_pool_value == 'vanilla'
            elif world.settings.shuffle_scrubs == 'off':
                shuffle_item = False
            else:
                item = deku_scrubs_items[location.vanilla_item]
                if isinstance(item, list):
                    item = random.choices([i[0] for i in item], weights=[i[1] for i in item], k=1)[0]
                shuffle_item = True

        # Kokiri Sword
        elif location.vanilla_item == 'Kokiri Sword':
            shuffle_item = world.settings.shuffle_kokiri_sword and not world.settings.item_pool_value == 'vanilla'

        # Weird Egg
        elif location.vanilla_item == 'Weird Egg':
            if world.settings.skip_child_zelda:
                item = 'Recovery Heart'
                shuffle_item = False
            else:
                shuffle_item = world.settings.shuffle_weird_egg

        # Ocarinas
        elif location.vanilla_item == 'Ocarina':
            shuffle_item = world.settings.shuffle_ocarinas

        # Giant's Knife
        elif location.vanilla_item == 'Giants Knife':
            shuffle_item = world.settings.shuffle_medigoron_carpet_salesman

        # Bombchus
        elif location.vanilla_item in ['Bombchus', 'Bombchus (5)', 'Bombchus (10)', 'Bombchus (20)']:
            if world.settings.bombchus_in_logic:
                item = 'Bombchus'
            shuffle_item = not world.settings.item_pool_value == 'vanilla'
            if location.name == 'Wasteland Bombchu Salesman':
                shuffle_item = world.settings.shuffle_medigoron_carpet_salesman

        # Cows
        elif location.vanilla_item == 'Milk':
            if world.settings.shuffle_cows:
                item = get_junk_item()[0]
            shuffle_item = world.settings.shuffle_cows

        # Gerudo Card
        elif location.vanilla_item == 'Gerudo Membership Card':
            shuffle_item = world.settings.shuffle_gerudo_card and world.settings.gerudo_fortress != 'open'
            if world.settings.shuffle_gerudo_card and world.settings.gerudo_fortress == 'open':
                pending_junk_pool.append('Gerudo Membership Card')
                item = 'Recovery Heart'

        # Bottles
        elif location.vanilla_item in ['Bottle', 'Bottle with Milk', 'Rutos Letter']:
            if world.settings.item_pool_value == 'vanilla':
                pass
            elif ruto_bottles:
                item = 'Rutos Letter'
                ruto_bottles -= 1
            else:
                item = random.choice(normal_bottles)
            shuffle_item = not world.settings.item_pool_value == 'vanilla'

        # Magic Beans
        elif location.vanilla_item == 'Magic Bean':
            if world.settings.shuffle_beans:
                item = 'Magic Bean Pack' if world.distribution.get_starting_item('Magic Bean') < 10 else get_junk_item()[0]
                shuffle_item = True
            else:
                shuffle_item = False

        # Adult Trade Item
        elif location.vanilla_item == 'Pocket Egg':
            if world.settings.item_pool_value != 'vanilla':
                earliest_trade = trade_item_options.index(world.settings.logic_earliest_adult_trade)
                latest_trade = trade_item_options.index(world.settings.logic_latest_adult_trade)
                if earliest_trade > latest_trade:
                    earliest_trade, latest_trade = latest_trade, earliest_trade
                item = random.choice(trade_items[earliest_trade:latest_trade + 1])
                world.selected_adult_trade_item = item
                shuffle_item = True
            else:
                shuffle_item = False

        # Thieves' Hideout
        elif location.vanilla_item == 'Small Key (Thieves Hideout)':
            shuffle_item = world.settings.shuffle_hideoutkeys in ['any_dungeon', 'overworld', 'keysanity']
            if (world.settings.gerudo_fortress == 'open'
                    or world.settings.gerudo_fortress == 'fast' and location.name != 'Hideout Jail Guard (1 Torch)'):
                item = 'Recovery Heart'
                shuffle_item = False
            if shuffle_item and world.settings.gerudo_fortress == 'normal' and 'Thieves Hideout' in world.settings.key_rings:
                item = get_junk_item()[0] if 'Small Key Ring (Thieves Hideout)' in pool else 'Small Key Ring (Thieves Hideout)'

        # Dungeon Items
        elif location.dungeon is not None:
            dungeon = location.dungeon
            shuffle_setting = None
            dungeon_collection = None

            # Boss Key
            if location.vanilla_item == dungeon.item_name("Boss Key"):
                shuffle_setting = world.settings.shuffle_bosskeys if dungeon.name != 'Ganons Castle' else world.settings.shuffle_ganon_bosskey
                dungeon_collection = dungeon.boss_key
                if shuffle_setting == 'vanilla':
                    shuffle_item = False
            # Map or Compass
            elif location.vanilla_item in [dungeon.item_name("Map"), dungeon.item_name("Compass")]:
                shuffle_setting = world.settings.shuffle_mapcompass
                dungeon_collection = dungeon.dungeon_items
                if shuffle_setting == 'vanilla':
                    shuffle_item = False
            # Small Key
            elif location.vanilla_item == dungeon.item_name("Small Key"):
                shuffle_setting = world.settings.shuffle_smallkeys
                dungeon_collection = dungeon.small_keys
                if shuffle_setting == 'vanilla':
                    shuffle_item = False
                elif dungeon.name in world.settings.key_rings and not dungeon.small_keys:
                    item = dungeon.item_name("Small Key Ring")
                elif dungeon.name in world.settings.key_rings:
                    item = get_junk_item()[0]
                    shuffle_item = True
            # Any other item in a dungeon.
            elif location.type in ["Chest", "NPC", "Song", "Collectable", "Cutscene", "BossHeart"]:
                shuffle_item = not world.settings.item_pool_value == 'vanilla'

            # Handle dungeon item.
            if shuffle_setting is not None and not shuffle_item:
                dungeon_collection.append(ItemFactory(item))
                if shuffle_setting in ['remove', 'startwith', 'triforce']:
                    world.state.collect(dungeon_collection[-1])
                    item = get_junk_item()[0]
                    shuffle_item = True
                elif shuffle_setting in ['any_dungeon', 'overworld']:
                    dungeon_collection[-1].priority = True

        # The rest of the overworld items.
        elif location.type in ["Chest", "NPC", "Song", "Collectable", "Cutscene", "BossHeart"]:
            shuffle_item = not world.settings.item_pool_value == 'vanilla'

        # Now, handle the item as necessary.
        if shuffle_item:
            pool.append(item)
        elif shuffle_item is not None:
            placed_items[location.name] = item
    # End of Locations loop.

    if world.settings.shopsanity != 'off':
        pool.extend(min_shop_items)
        for item in min_shop_items:
            remain_shop_items.remove(item)

        shop_slots_count = len(remain_shop_items)
        shop_non_item_count = len(world.shop_prices)
        shop_item_count = shop_slots_count - shop_non_item_count

        pool.extend(random.sample(remain_shop_items, shop_item_count))
        if shop_non_item_count:
            pool.extend(get_junk_item(shop_non_item_count))

    # Extra rupees for shopsanity.
    if world.settings.shopsanity not in ['off', '0']:
        for rupee in shopsanity_rupees:
            if 'Rupees (5)' in pool:
                pool[pool.index('Rupees (5)')] = rupee
            else:
                pending_junk_pool.append(rupee)

    if world.settings.free_scarecrow:
        world.state.collect(ItemFactory('Scarecrow Song'))
    
    if world.settings.no_epona_race:
        world.state.collect(ItemFactory('Epona', event=True))

    if world.settings.shuffle_smallkeys == 'vanilla':
        # Logic cannot handle vanilla key layout in some dungeons
        # this is because vanilla expects the dungeon major item to be
        # locked behind the keys, which is not always true in rando.
        # We can resolve this by starting with some extra keys
        if world.dungeon_mq['Spirit Temple']:
            # Yes somehow you need 3 keys. This dungeon is bonkers
            world.state.collect(ItemFactory('Small Key (Spirit Temple)'))
            world.state.collect(ItemFactory('Small Key (Spirit Temple)'))
            world.state.collect(ItemFactory('Small Key (Spirit Temple)'))
        if 'shadow_temple' in world.settings.dungeon_shortcuts:
            # Reverse Shadow is broken with vanilla keys in both vanilla/MQ
            world.state.collect(ItemFactory('Small Key (Shadow Temple)'))
            world.state.collect(ItemFactory('Small Key (Shadow Temple)'))

    # Collect all small keys in vanilla item pool.
    if world.settings.item_pool_value == 'vanilla':
        small_keys = [item for dungeon in world.dungeons for item in dungeon.small_keys]
        for key in small_keys:
            world.state.collect(ItemFactory(key.name))

    if not world.keysanity and not world.dungeon_mq['Fire Temple']:
        world.state.collect(ItemFactory('Small Key (Fire Temple)'))

    if world.settings.shuffle_ganon_bosskey == 'on_lacs':
        placed_items['ToT Light Arrows Cutscene'] = 'Boss Key (Ganons Castle)'

    if world.settings.shuffle_ganon_bosskey in ['stones', 'medallions', 'dungeons', 'tokens']:
        placed_items['Gift from Sages'] = 'Boss Key (Ganons Castle)'
        pool.extend(get_junk_item())
    else:
        placed_items['Gift from Sages'] = 'Ice Trap'

    if world.settings.junk_ice_traps == 'off':
        replace_max_item(pool, 'Ice Trap', 0)
    elif world.settings.junk_ice_traps == 'onslaught':
        for item in [item for item, weight in junk_pool_base] + ['Recovery Heart', 'Bombs (20)', 'Arrows (30)']:
            replace_max_item(pool, item, 0)

    for item, maximum in item_difficulty_max[world.settings.item_pool_value].items():
        replace_max_item(pool, item, maximum)

    world.distribution.alter_pool(world, pool)

    # Make sure our pending_junk_pool is empty. If not, remove some random junk here.
    if pending_junk_pool:
        for item in set(pending_junk_pool):
            # Ensure pending_junk_pool contents don't exceed values given by distribution file
            if item in world.distribution.item_pool:
                while pending_junk_pool.count(item) > world.distribution.item_pool[item].count:
                    pending_junk_pool.remove(item)
                # Remove pending junk already added to the pool by alter_pool from the pending_junk_pool
                if item in pool:
                    count = min(pool.count(item), pending_junk_pool.count(item))
                    for _ in range(count):
                        pending_junk_pool.remove(item)

        remove_junk_pool, _ = zip(*junk_pool_base)
        # Omits Rupees (200) and Deku Nuts (10)
        remove_junk_pool = list(remove_junk_pool) + ['Recovery Heart', 'Bombs (20)', 'Arrows (30)', 'Ice Trap']

        junk_candidates = [item for item in pool if item in remove_junk_pool]
        while pending_junk_pool:
            pending_item = pending_junk_pool.pop()
            if not junk_candidates:
                raise RuntimeError("Not enough junk exists in item pool for %s to be added." % pending_item)
            junk_item = random.choice(junk_candidates)
            junk_candidates.remove(junk_item)
            pool.remove(junk_item)
            pool.append(pending_item)

    world.distribution.configure_starting_items_settings(world)
    world.distribution.collect_starters(world.state)

    return pool, placed_items
