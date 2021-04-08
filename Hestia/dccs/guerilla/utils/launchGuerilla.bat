:: This batch file setup de environement to use the Hestia.

:: Define the Hestia main folder.
set HESTIA=C:\Users\ldepoix\Documents\DEV\Hestia
:: Set the python path to find PySide and the Hestia.
set PYTHONPATH=%HESTIA%\venv27_win64\Lib\site-packages;%HESTIA%
:: Set the python dll path.
set GUERILLA_PYTHON_LIBRARY=C:\Windows\System32\python27.dll
:: Set the Hestia guerilla configuration file to add the custom command.
set GUERILLA_USR_CONF=%HESTIA%\Hestia\dccs\guerilla\utils\guerilla.conf
:: Set the installation folder of guerilla.
set GUERILLA="C:\Program Files\Guerilla Render"

:: Launch Guerilla
"C:\Program Files\Guerilla Render\guerilla.exe"