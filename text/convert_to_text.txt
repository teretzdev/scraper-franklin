@echo off
mkdir text 2>nul
for %%a in (*) do copy "%%a" "text\%%~na.txt"

