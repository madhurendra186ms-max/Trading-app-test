$serviceRoot = Split-Path -Parent $PSCommandPath
$python = Join-Path $serviceRoot ".venv\Scripts\python.exe"

Push-Location $serviceRoot
& $python -m uvicorn main:app --port 8005 --reload
Pop-Location
