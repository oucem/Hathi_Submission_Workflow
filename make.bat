@echo off


if [%1] == []               goto main
if "%1" == "install-dev"    goto install-dev
if "%1" == "gui"            goto gui
if "%1" == "test"           goto test

EXIT /B 0

:main
    call :install-dev
    call :gui
goto :eof
if
:gui
setlocal
    echo Converting Qt .ui files into Python files
    for %%f in (
     ui/*.ui ) do (
        echo  %%~nf
        pyuic5 ui\%%f -o hsw\ui\%%~nf.py

    )
endlocal
goto :eof

:install-dev
    echo Installing development requirements
    pip install -r requirements.txt
goto :eof

:test
    python setup.py test
goto :eof