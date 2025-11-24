@echo off
REM Script para criar ambiente virtual e instalar dependências
REM Projeto: Análise ML - ENAP

echo ================================================================================
echo CRIANDO AMBIENTE VIRTUAL PARA PROJETO DE MACHINE LEARNING
echo ================================================================================

REM Criar ambiente virtual
echo.
echo 1. Criando ambiente virtual 'venv_ml'...
python -m venv venv_ml

if %ERRORLEVEL% NEQ 0 (
    echo ERRO: Falha ao criar ambiente virtual
    pause
    exit /b 1
)

echo    OK - Ambiente virtual criado!

REM Ativar ambiente virtual
echo.
echo 2. Ativando ambiente virtual...
call venv_ml\Scripts\activate.bat

REM Atualizar pip
echo.
echo 3. Atualizando pip...
python -m pip install --upgrade pip

REM Instalar dependências
echo.
echo 4. Instalando dependências...
echo    - pandas
echo    - numpy
echo    - matplotlib
echo    - seaborn
echo    - scikit-learn
echo    - xgboost
echo    - openpyxl

pip install pandas numpy matplotlib seaborn scikit-learn xgboost openpyxl

if %ERRORLEVEL% NEQ 0 (
    echo ERRO: Falha ao instalar dependências
    pause
    exit /b 1
)

echo.
echo ================================================================================
echo AMBIENTE VIRTUAL CONFIGURADO COM SUCESSO!
echo ================================================================================
echo.
echo Para usar o ambiente virtual:
echo   1. Ativar: venv_ml\Scripts\activate
echo   2. Executar scripts Python
echo   3. Desativar: deactivate
echo.
echo Pacotes instalados:
pip list
echo.
echo ================================================================================

pause
