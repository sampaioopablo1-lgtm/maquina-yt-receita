@echo off
title GRAVACAO - Receita Video Pipeline
cd /d "%~dp0"
echo.
echo =========================================================
echo   GRAVACAO - ligue o gravador de tela ANTES de continuar.
echo =========================================================
echo.
echo Este apaga o login guardado, para que a tela de permissao
echo apareca de novo - e ela que o revisor precisa ver.
echo.
pause
if exist token.json del token.json
call :acharpython
if errorlevel 1 goto :fim
set DEMO_UPLOAD=1
%PY% auditoria_demo.py
goto :fim

:acharpython
python --version >/dev/null 2>&1 && (set PY=python & exit /b 0)
py --version >/dev/null 2>&1 && (set PY=py & exit /b 0)
echo.
echo  *** PYTHON NAO ENCONTRADO - rode o 1-ENSAIO.bat primeiro ***
exit /b 1

:fim
echo.
pause
