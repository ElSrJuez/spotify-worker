
# spotify-worker setup script (git-root aware)
# 1. Find git repo root
# 2. Check for .venv, create if missing
# 3. Activate .venv
# 4. Install requirements
# 5. Print usage hints

$gitRoot = (& git rev-parse --show-toplevel).Trim()
if (-not $gitRoot) {
	Write-Host "[ERROR] Could not determine git repo root. Are you in a git repo?"
	exit 1
}

$venvPath = Join-Path $gitRoot ".venv"
$venvActivate = Join-Path $venvPath "Scripts\Activate.ps1"
$requirements = Join-Path $gitRoot "requirements.txt"

Write-Host "[spotify-worker setup] Checking for .venv at $venvPath..."
if (!(Test-Path -Path $venvPath)) {
	Write-Host "[spotify-worker setup] Creating virtual environment (.venv)..."
	python -m venv $venvPath
} else {
	Write-Host "[spotify-worker setup] .venv already exists."
}

Write-Host "[spotify-worker setup] Activating .venv..."
if (Test-Path $venvActivate) {
	& $venvActivate
	Write-Host "[spotify-worker setup] .venv activated."
} else {
	Write-Host "[ERROR] Could not find .venv activation script at $venvActivate"
	exit 1
}

Write-Host "[spotify-worker setup] Installing requirements from $requirements..."
python -m pip install --upgrade pip
python -m pip install -r $requirements

Write-Host "[spotify-worker setup] Setup complete!"
Write-Host ""
Write-Host "To run the app, activate your virtual environment with:"
Write-Host "    $venvActivate"
Write-Host "Then run:"
Write-Host "    python playlist-worker.py"
