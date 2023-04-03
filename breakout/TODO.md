# TODO

## Basic Functionality

### ToDo

- change the ball angle depending on where the bat is hit or dependent on bat velocity ('English')
- bug?: sometimes multiple bricks are destroyed (could be related to brick rebound handling)
- brick positioning per level (creeps down the screen)
- bug: sometimes the ball goes straight through the bricks (is this related to the reflection handling?)
- bug: ball/bat collisions: ball can get trapped in the bat collision surface and not bounce cleanly away
- add debug/test mode if started using RMB - lives = 1, bricks = 1, draw normals, pause game

### Done

- basic game
- lives
- scoring
- high score
- destroy bricks
- end of level/next level handling
- sound cues
- improved game state handling, delays are no longer required
- gradient-shaded text with transparency masking
- better rebound handling when hitting bricks
  - use vector reflection code
  - example https://replit.com/@Rabbid76/PyGame-BallBounceOffFrame#main.py
- brick shape should reflect collision box (or vice-versa)
- bugfix: new rebound handling sometimes does not return a valid brick edge and normal
  - eg collision_info: unknown dx: 43.0 dy: 0.0 theta: 0.0
  - [156.755, 195.348] [0.707107, 0.707107] 6
  - <rect(151, 189, 12, 12)> <rect(160, 180, 80, 30)>
  - left edge collision box was incorrect
  - also implemented default normal reflection on ball sprite
- bugfix: high score entry text position & cursor are misaligned (font was not monospace)
- color-fill for fonts, similar to https://www.dafont.com/press-start-2p.font

## Quality Improvements

- case handling for text input
- better sound cues
- improved graphics
- use a nicer palette
- add animations (e.g. when a brick is destroyed)
- find a free, arcade-stype monospace font

## Technical Debt

- improve the state machine
  - implement a state-table
  - define exit conditions using the state table
  - define valid state transitions using the state-table (using guards)
- implement pre and post state handlers when entring and exiting a state 
- implement entry and exit function handlers when transitioning 

## Find better sound effects

- Current: <https://www.freesoundslibrary.com/>
