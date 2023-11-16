@echo off
setlocal enabledelayedexpansion

set "type=%~1"
set "data1=%~2"
set "num=%~3"
set "params=%*"

for /f "tokens=2-3* delims= " %%a in ("%params%") do (
    set "data2=%%c"
echo %data2%
)

echo %type%
echo %data1%
echo %num%
echo %data2%
(
echo %type%
echo %data1%
echo %num%
echo %data2%
) | adb shell /vendor/bin/vehicletest

endlocal
pause