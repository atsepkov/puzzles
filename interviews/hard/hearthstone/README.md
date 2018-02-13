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

**BONUS**: Change the program such that it takes any 2 30-card decks as input (that only use the cards mentioned in original decks, but in any other combination/quantity) and computes the highest possible attack value for them.
