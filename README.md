# PokerNow Robot
## Install
```
$ pip3 -r requirement.txt
$ python3 robot_main.py --game-id ${POKERNOW_GAME_ID}
```

## Version 1.0: Auto-fold in preflop
We can define the preflop play range in poker_game.py
For example:
```
self._preflop_fold_range = PokerRange(
    'A2s+ K2s+ Q2s+ J7s+ T6s+ 96s+ 85s+ 74s+ 63s+ 52s+ 42s+ 32s+ A2o+ K9o+ Q9o+ J9o+ T9o+ 22+ 27s')
```
