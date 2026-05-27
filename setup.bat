@echo off
echo ============================================
echo  iNextLabs Newsletter — Setup
echo ============================================
echo.
echo Setting up folder structure...

:: Create folders
mkdir "2026-05" 2>nul
mkdir "_template" 2>nul

:: Move May 2026 files into 2026-05/
move /Y "2026-05-index.html"            "2026-05\index.html"            >nul 2>&1
move /Y "2026-05-whatsapp-calling.html" "2026-05\whatsapp-calling.html" >nul 2>&1

:: Move template files into _template/
move /Y "_template-newsletter.html"     "_template\newsletter.html"     >nul 2>&1
move /Y "_template-feature-detail.html" "_template\feature-detail.html" >nul 2>&1

echo Done! Your structure is now:
echo.
echo   NewsLetters/
echo     2026-05/
echo       index.html              ^<-- Open this in browser to view May newsletter
echo       whatsapp-calling.html   ^<-- WhatsApp Calling feature detail page
echo     _template/
echo       newsletter.html         ^<-- Copy to new month folder to start fresh
echo       feature-detail.html     ^<-- Copy for each new feature detail page
echo.
echo HOW TO CREATE A NEW MONTH:
echo   1. Copy _template\newsletter.html     to  2026-06\index.html
echo   2. Copy _template\feature-detail.html to  2026-06\feature-name.html
echo   3. Edit the EDIT markers in each file
echo.
echo ============================================
pause
