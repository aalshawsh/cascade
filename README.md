# Cascade
Play cascade with yourself against a randomAgent or with a friend!
(note: i didnt create the game idea, COMP30024 staff team came up with it. I just felt like making it into a full fledged game)

## About
Cascade is a two player game, where one can either be red or blue. Game starts off with 2 players placing 4 towers and the goal is to eliminate all opponents towers.

## How to play
to run the game with 2 humanAgents run this: python3 -m myReferee myHumanAgent myHumanAgent

to run the game with 1 humanAgent and a randomAgent: python3 -m myReferee myHumanAgent myRandomAgent

if you want to add ur own agent you can just make sure it uses myReferee module

## Game mechanics:
Press on a green square to place towers, click on a tower u want to move, legal moves are highlighted in green. To turn cascade mode on click the CASCADE? button on the bottom right of the screen legal squares should be purple(Make sure to turn it off)

## Lastly
Game is not yet finished, it works but ill have to flush it out(add a way to replay without rerunning it over and over in the terminal, remove the green/red squares, and clean up code)

All game logic comes from the referee module which we modified to accommodate , we just added a way to communicate between referee and our game code(and a human agent if used). it uses threads to run the referee in a separate thread and the main thread is reserved for the actual game...

## acknowledgements
Like mentioned before I didn't come up with cascade, but everything else is me and team members work. All music and art created by me....

## contacts
If in the likely case it doesn't work shoot me an email at aalshawsh@student.unimelb.edu.au

