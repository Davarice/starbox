# StarBox
An engine for obsessive compulsives with an inability not to overthink such as myself to simulate a living universe for a science fiction TTRPG

**Very much in-development**

# Goals:
- [ ] A structured multi-level "board" around which "game pieces" can be moved
- [ ] An interface for the addition and seamless integration of new locations and pieces into the board
- [ ] A timekeeping function to increment and decrement time in the game world, and move orbiting pieces as appropriate
- [ ] Potentially: A web application allowing players to explore locations they have seen

# Program Structure:

## Bottom layer, section A: The Game Board
A mostly-static set of objects in memory, interconnected and tiered by way of attributes referencing each other
These objects integrate portions of AstroPy for their attributes, allowing for easy unit conversion and geometric operations

## Lower interface sublayer
A set of functions to manipulate elements of the game board such as creation of celestial bodies, as well as changing their positions to correspond with the passage of game time


