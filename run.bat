@ECHO OFF
SET PYTHONPATH=..;core
REM Add following to %VIRTUAL_ENV%\Scripts\activate.bat
REM SET "TCL_LIBRARY=C:\python35\tcl\tcl8.5"
python -m janggi.gui.main %*
