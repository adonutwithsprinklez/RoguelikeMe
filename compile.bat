pyinstaller --onefile --clean ^
    --additional-hooks-dir=src/ ^
    --noconsole ^
    -n "Roguelike Me" ^
    src/main.py

xcopy /s /y /f src\res dist\res
pause