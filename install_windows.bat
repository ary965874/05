@echo off
echo Installing Enhanced Movie Bot Dependencies for Windows...
echo ========================================================

echo.
echo Step 1: Installing core dependencies without tgcrypto...
pip install -r requirements.txt

echo.
echo Step 2: Attempting to install tgcrypto (optional for better performance)...
echo Note: If this fails, the bot will still work without it.

rem Try different methods to install tgcrypto
echo Trying pre-compiled wheel...
pip install --only-binary=all tgcrypto 2>nul
if %errorlevel% equ 0 (
    echo ✓ tgcrypto installed successfully!
    goto :test_installation
)

echo Trying from PyPI with no cache...
pip install --no-cache-dir tgcrypto 2>nul
if %errorlevel% equ 0 (
    echo ✓ tgcrypto installed successfully!
    goto :test_installation
)

echo Trying with user install...
pip install --user tgcrypto 2>nul
if %errorlevel% equ 0 (
    echo ✓ tgcrypto installed successfully!
    goto :test_installation
)

echo ! tgcrypto installation failed - bot will work without it (slower encryption)

:test_installation
echo.
echo Step 3: Testing installation...
python simple_test.py

echo.
echo Installation complete!
echo =====================
echo.
echo Next steps:
echo 1. Run: python bot.py
echo 2. Test movie search in your connected group
echo 3. Verify subtitle functionality
echo.
echo Note: Bot works without tgcrypto, just with slower encryption.
pause