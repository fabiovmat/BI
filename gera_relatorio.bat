@echo off
chcp 65001 >nul

title Gerando Relatório - Projeto Shaolin

echo.
echo Iniciando geração do relatório...
echo.

REM Simulação da barra de carregamento
setlocal enabledelayedexpansion
set "bar="

for %%A in (1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20) do (
    set "bar=!bar!█"
    <nul set /p=!bar!
    timeout /nobreak /delay 1 >nul
    cls
    echo Gerando relatório... Aguarde.
    echo !bar!
)

echo.
echo Executando script Python...
python gera_relatorio_shao.py

echo.
echo Relatório gerado com sucesso!
pause
