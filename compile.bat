pyinstaller --onefile --clean ^
    --additional-hooks-dir=src/ ^
    --noconsole ^
    -n "Roguelike Me" ^
    src/engine.py

xcopy /s /y /f src\res dist\res
pause