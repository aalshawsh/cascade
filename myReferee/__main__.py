# COMP30024 Artificial Intelligence, Semester 1 2026
# Project Part B: Game Playing Agent

from .main import main
import sys
import threading
from .main import main
from .cascade import Cascade
from .options import get_options


if __name__ == "__main__":
    
    options = vars(get_options())

    # pass in name of player agent classes
    cascade = Cascade(options["player1_loc"],options["player2_loc"])

    # display start screen
    cascade._start_menu_loop()

    # start seperate thread for referee program
    referee_thread = threading.Thread(
        target=main,
        args=(cascade,)
    )
    referee_thread.daemon = True
    referee_thread.start()
    
    # render the game in the main thread
    cascade._render_loop()

    sys.exit(0)

