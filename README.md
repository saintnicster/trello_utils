#Introduction 
These are the utilities that the ISSoW group uses to maintain our team management tools.  Currently, we put our ServiceNow tickets into a private Trello board.

#Getting Started
1.	The Pyhton code here was developed on Python 3.6.1.  This is NOT the version found in the COP Software Store.
2.	When setting up the python environment,  you will need these modules via PIP.
    * py-trello
    * pyperclip
    * cx-Freeze

#Build and Test
Building the exe files is done by navigating inside the `python-tools` directory, then running `python .\setup.py build`.  This will generate the folder `python-tools\build\combo`.  Two executables, along with the python framework will be generated and can be run on a machine that doesn't have python installed natively
