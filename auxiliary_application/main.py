##
#@package auxiliary_application
#@file main.py
#@brief Main application logic for the auxiliary application.
#
#This script initializes the GUI and manages application flow.
#
from .gui import Gui


if __name__ == "__main__":
    ##
    # @var gui
    # @brief The main graphical user interface object of the application.
    # @details Creates an instance of the Gui class and starts the main event loop.
    # @see Gui
    gui = Gui()
    gui.mainloop()
