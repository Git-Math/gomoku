# gomoku
[Gomoku](https://en.wikipedia.org/wiki/Gomoku) board game with a graphic interface and AI.  

The AI is an implementaton of [alpha beta pruning](https://en.wikipedia.org/wiki/Alpha%E2%80%93beta_pruning) algorithm with optimizations in order to play well and fast.

## Rules
The rules of the gomoku with some additional rules to make the game more fair:
- Capture (As in the Ninuki-renju or Pente variants) : You can remove a pair of your opponent’s stones from the board by flanking them with your own stones (See the appendix). This rule adds a win condition : If you manage to capture ten of your opponent’s stones, you win the game
- Game-ending capture : A player that manages to align five stones only wins if the opponent can not break this alignment by capturing a pair, or if he has already lost four pairs and the opponent can capture one more, therefore winning by capture. There is no need for the game to go on if there is no possibility of this happening
- No double-threes : It is forbidden to play a move that introduces two free-three alignments, which would guarantee a win by alignment

## In game options
- Play against AI
- Change the level of the AI from 1 to 10
- Request help from the AI with the help button
- Play against another player
- Change the pieces colors
- Enable/Disable the no double-threes rule

## How to run
From the root of the repository run `python3 gomoku.py`.

![gomoku_menu](https://github.com/Git-Math/gomoku/assets/11985913/dfdb72cc-0d71-4c9a-98c2-5c8a8708605d)

![gomoku_partie](https://github.com/Git-Math/gomoku/assets/11985913/c6f9db67-7fb6-493e-bab8-a68b06f9d6a8)
