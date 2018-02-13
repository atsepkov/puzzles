Hearthstone
===========
Hearthstone is a turn-based online card game between 2 opponents, using constructed decks of 30 cards and a hero with unique power. Players use their limited mana crystals to cast spells and summon minions to attack the opponent. There are 3 types of cards in Hearthstone, but we only need to consider 2 types:

- minion (costs mana to play, stays in play until killed, has numeric attack and health)
- spell (costs mana to play, disappears after use, targets one or more minions or a hero, has permanent effect unless removed)

In 2018 a special event took place, called "Nefarian Rises", where instead of fighting each other the 2 players had to cooperate to take down a powerful boss together. The easiest way to take this boss down was by building a super-minion by having both players stack spells on top of the same minion until it becomes stronger than the boss.

Both the description of the event and decks each player starts out with can be found here (either link):
https://www.hearthpwn.com/news/4336-nefarian-rises-is-this-weeks-brawl-play
https://hearthstone.gamepedia.com/Nefarian_Rises!

While the minion only needs to be moderately strong to take down the boss (above 50 attack, 50 health), it is theoretically possible to build a minion much stronger using these decks. Write a program that computes and prints out the highest possible attack of such minion.

For simplicity of this question, let's assume the following (which deviates from actual Hearthstone rules):

- both players have access to their entire deck at all times and can play the cards in any order they wish
- the boss does not attack or use any skills (so no healing is necessary)
- once played, the card is discarded and can't be played again (unless another minion/spell returns the card to player's hand)
- player can play as many cards as they wish per turn but the total cost per turn can never exceed 10 mana crystals
- players alternate taking turns
- "battlecry" effect is triggered when the card is played
- "inspire" effect is triggered when player uses their hero power, hero power costs 2 mana and can only be used once per turn (assume hero power has no other effect)
- "deathrattle" effect is triggered when a minion dies (ignore it since there is no attacking)
- any random event can be assumed to produce the best possible result at the time it is played (i.e. copying a random spell can copy any spell that hasn't been played yet)
- your program only needs to account for the abilities of cards in these 2 decks, not any other Hearthstone cards

**BONUS**: In the real match, the boss can play Bamboozle card at any time at the end of player's turn, forcing players to swap hands. Since we do not differentiate between hand and deck in this puzzle, let's simplify this effect and as with other effects, assume best case scenario. At the end of player's turn, you may "simulate" the Bamboozle effect by giving between 0-10 unplayed cards (*your choice) from one player to another and vice-versa (the number of cards traded can be different for each player).

**BONUS 2**: Change the program such that it takes any 2 30-card decks as input (that only use the cards mentioned in original decks, but in any other combination/quantity) and computes the highest possible attack value for them.

For your reference, tables summarizing both decks are also included below. Cards with no `Stats` are spells, cards with numbers in `Stats` column are minions where the numbers represent `Attack/Health`. The `Cost` is in Mana Crystals. Player can use up to 10 Mana Crystals per turn. In the beginning of player's turn, their Mana Crystals replenish.

Priest
------

| Card Name             | Qty | Cost | Stats | Ability                                                                 |
| ---                   | --- | ---  | ---   | ---                                                                     |
| Shadow or Light?      | 2   | 2    |       | Choose One: Each player draws 2 cards; or Restore 8 Health to each hero |
| Main Tank             | 1   | 4    | 4/4   | Battlecry: Give all other minions +2/+2, except the Boss                |
| Raid Healer           | 1   | 4    | 0/7   | Whenever your hero is healed, also heal your teammate for that much     |
| Power Word: Glory     | 1   | 1    |       | Choose a minion. Whenever it attacks, restore 4 Health to your hero     |
| Inner Fire            | 1   | 1    |       | Change a minion's Attack to be equal to its Health                      |
| Mind Vision           | 1   | 1    |       | Put a copy of a random card in your opponent's hand into your hand      |
| Northshire Cleric     | 1   | 1    | 1/3   | Whenever a minion is healed, draw a card                                |
| Power Word: Shield    | 2   | 1    |       | Give a minion +2 Health, draw a card                                    |
| Convert               | 1   | 2    |       | Put a copy of an enemy minion into your hand                            |
| Divine Spirit         | 2   | 2    |       | Double a minion's Health                                                |
| Shrinkmeister         | 1   | 2    | 3/2   | Battlecry: Give a minion -2 Attack this turn                            |
| Shadowfiend           | 1   | 3    | 3/3   | Whenever you draw a card, reduce its Cost by 1                          |
| Thoughtsteal          | 1   | 3    |       | Copy 2 cards from your opponent's deck and put them into your hand      |
| Velen's Chosen        | 2   | 3    |       | Give a minion +2/+4 and Spell Damage +1                                 |
| Power Word: Tentacles | 2   | 5    |       | Give a minion +2/+6                                                     |
| Zombie Chow           | 1   | 1    | 2/3   | Deathrattle: Restore 5 Health to the enemy hero                         |
| Youthful Brewmaster   | 1   | 2    | 3/2   | Battlecry: Return a friendly minion from the battlefield to your hand   |
| Arcane Golem          | 1   | 3    | 4/4   | Battlecry: Give your opponent a Mana Crystal                            |
| Brann Bronzebeard     | 1   | 3    | 2/4   | Your Battlecries trigger twice                                          |
| Coldlight Oracle      | 1   | 3    | 2/2   | Battlecry: Each player draws 2 cards                                    |
| King Mukla            | 1   | 3    | 5/5   | Battlecry: Give your opponent 2 Bananas                                 |
| Refreshment Vendor    | 1   | 4    | 3/5   | Battlecry: Restore 4 Health to each hero                                |
| Corrupted Healbot     | 1   | 5    | 6/6   | Deathrattle: Restore 8 Health to the enemy hero                         |
| Cult Apothecary       | 1   | 5    | 4/4   | Battlecry: For each enemy minion, restore 2 Health to your hero         |
| Justicar Trueheart    | 1   | 6    | 6/3   | Battlecry: Replace your starting hero power with a better one           |

Shaman
------

| Card Name                 | Qty | Cost | Stats | Ability                                                                                  |
| ---                       | --- | ---  | ---   | ---                                                                                      |
| Dragonscale Warrior       | 1   | 3    | 3/4   | Whenever any player targets this minion with a spell, that player draws a card           |
| Main Tank                 | 1   | 4    | 4/4   | Battlecry: Give all other minions +2/+2, except the Boss                                 |
| Freewheeling Skulker      | 1   | 5    | 5/6   | At the end of your turn, switch sides                                                    |
| Intrepid Dragonstalker    | 1   | 5    | 3/3   | Whenever any player plays a card, gain +1/+1                                             |
| Ancestral Healing         | 1   | 0    |       | Restore a minion to full Health and give it Taunt                                        |
| Rockbiter Weapon          | 2   | 1    |       | Give a friendly character +3 Attack this turn                                            |
| Ancestral Spirit          | 2   | 2    |       | Give a minion "Deathrattle: Resummon this minion."                                       |
| Vitality Totem            | 1   | 2    | 0/3   | At the end of your turn, restore 4 Health to your hero                                   |
| Windfury                  | 2   | 2    |       | Give a minion Windfury                                                                   |
| Healing Wave              | 1   | 3    |       | Restore 7 Health. Reveal a minion in each deck. If yours costs more, restore 14 instead  |
| Windspeaker               | 1   | 4    | 3/3   | Battlecry: Give a friendly minion Windfury                                               |
| Bloodlust                 | 1   | 5    |       | Give your minions +3 Attack this turn                                                    |
| Al'Akir the Windlord      | 1   | 8    | 3/5   | Windfury, Charge, Divine Shield, Taunt                                                   |
| Nat, the Darkfisher       | 1   | 2    | 2/4   | At the start of your opponent's turn, they have a 50% chance to draw an extra card       |
| Arcane Golem              | 1   | 3    | 4/4   | Battlecry: Give your opponent a Mana Crystal                                             |
| Coldlight Oracle          | 1   | 3    | 2/2   | Battlecry: Each player draws 2 cards                                                     |
| Dancing Swords            | 1   | 3    | 4/4   | Deathrattle: Your opponent draws a card                                                  |
| Fjola Lightbane           | 1   | 3    | 3/4   | Whenever you target this minion with a spell, gain Divine Shield                         |
| Stoneskin Gargoyle        | 1   | 3    | 1/4   | At the start of your turn, restore this minion to full Health                            |
| Leeroy Jenkins            | 1   | 5    | 6/2   | Charge. Battlecry: Summon two 1/1 Whelps for your opponent                               |
| Validated Doomsayer       | 1   | 5    | 0/7   | At the start of your turn, set this minion's attack to 7                                 |
| Bolf Ramshield            | 1   | 6    | 3/9   | Whenever your hero takes damage, this minion takes it instead                            |
| Cairne Bloodhoof          | 1   | 6    | 4/5   | Deathrattle: Summon a 4/5 Baine Bloodhoof                                                |
| Mukla, Tyrant of the Vale | 1   | 6    | 5/5   | Battlecry: Add 2 Bananas to your hand                                                    |
| Sideshow Spelleater       | 1   | 6    | 6/5   | Battlecry: Copy your opponent's hero power                                               |
| The Skeleton Knight       | 1   | 6    | 7/4   | Deathrattle: Reveal a minion in each deck. If yours costs more, return this to your hand |
| Wobbling Runts            | 1   | 6    | 2/6   | Deathrattle: Summon three 2/2 runts                                                      |

Generated in Play
-----------------

| Card Name       | Qty | Cost | Stats | Ability             |
| ---             | --- | ---  | ---   | ---                 |
| Banana          |     | 1    |       | Give a minion +1/+1 |
| Baine Bloodhoof |     | 4    | 4/5   |                     |
