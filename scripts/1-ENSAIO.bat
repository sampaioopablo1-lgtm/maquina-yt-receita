@echo off
title ENSAIO - Receita Video Pipeline
cd /d "%~dp0"
echo.
echo =========================================================
echo   ENSAIO - so testa o login. Nada e enviado ao YouTube.
echo =========================================================
echo.
call :acharpython
if errorlevel 1 goto :fim
echo Instalando as bibliotecas (so demora na primeira vez)...
%PY% -m pip install --quiet --upgrade google-auth-oauthlib google-api-python-client
echo.
set DEMO_UPLOAD=0
%PY% auditoria_demo.py
goto :fim

:acharpython
python --version >/dev/null 2>&1 && (set PY=python & exit /b 0)
py --version >/dev/null 2>&1 && (set PY=py & exit /b 0)
echo.
echo  *** PYTHON NAO ENCONTRADO ***
echo.
echo  Vou abrir a pagina de download. Ao instalar, MARQUE a caixinha
echo  "Add python.exe to PATH" na primeira tela do instalador.
echo  Depois feche esta janela e clique aqui de novo.
echo.
start https://www.python.org/downloads/
exit /b 1

:fim
echo.
pause
