<#
.SYNOPSIS
    Build, test and publish win-cmd-fixer (Python) to PyPI.

.EXAMPLE
    .\publish_python.ps1                        # Build only
    .\publish_python.ps1 -Publish               # Build & publish to PyPI
    .\publish_python.ps1 -Publish -TestPyPI     # Build & publish to TestPyPI
#>

param(
    [switch]$Publish,
    [switch]$TestPyPI
)

Set-StrictMode -Version 1.0

$ROOT        = Split-Path -Parent $MyInvocation.MyCommand.Definition
$PY_DIR      = Join-Path $ROOT "python"
$VENV_PY     = Join-Path $ROOT ".venv\Scripts\python.exe"
$ROOT_README = Join-Path $ROOT "README.md"

# ---------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------

function Write-Step($msg) {
    Write-Host ""
    Write-Host "====== $msg ======" -ForegroundColor Cyan
}

function Assert-ExitCode($stepName) {
    if ($LASTEXITCODE -ne 0) {
        Write-Host "FAILED: $stepName (exit code $LASTEXITCODE)" -ForegroundColor Red
        exit 1
    }
}

function Invoke-Native {
    param([string]$Step, [scriptblock]$Cmd)
    $prev = $ErrorActionPreference
    $ErrorActionPreference = "Continue"
    & $Cmd 2>&1 | ForEach-Object { "$_" } | Write-Host
    $ErrorActionPreference = $prev
    Assert-ExitCode $Step
}

# ---------------------------------------------------------------
# Pre-flight
# ---------------------------------------------------------------

Write-Step "Pre-flight checks"

if (-not (Test-Path $VENV_PY)) {
    Write-Host "Python venv not found at $VENV_PY" -ForegroundColor Red
    Write-Host "Please create it first:  python -m venv .venv" -ForegroundColor Yellow
    exit 1
}

# ---------------------------------------------------------------
# Test
# ---------------------------------------------------------------

Write-Step "Running tests"
Push-Location $PY_DIR
Invoke-Native "pytest" { & $VENV_PY -m pytest tests\ --tb=short -q }
Pop-Location

# ---------------------------------------------------------------
# Build tools
# ---------------------------------------------------------------

Write-Step "Ensuring build tools"
Invoke-Native "pip install" { & $VENV_PY -m pip install --quiet --upgrade build twine }

# ---------------------------------------------------------------
# Clean & Build
# ---------------------------------------------------------------

Write-Step "Cleaning previous artifacts"
$pyDist     = Join-Path $PY_DIR "dist"
$pyBuildDir = Join-Path $PY_DIR "build"
$pyEggInfo  = Join-Path $PY_DIR "src\win_cmd_fixer.egg-info"
$pyReadme   = Join-Path $PY_DIR "README.md"
if (Test-Path $pyDist)     { Remove-Item $pyDist     -Recurse -Force }
if (Test-Path $pyBuildDir) { Remove-Item $pyBuildDir -Recurse -Force }
if (Test-Path $pyEggInfo)  { Remove-Item $pyEggInfo  -Recurse -Force }

if (Test-Path $ROOT_README) {
    Copy-Item $ROOT_README $pyReadme -Force
    Write-Host "Copied README.md into python/"
}

Write-Step "Building sdist + wheel"
Push-Location $PY_DIR
Invoke-Native "python build" { & $VENV_PY -m build }
Pop-Location

if (Test-Path $pyReadme) { Remove-Item $pyReadme -Force }

Write-Step "Checking package with twine"
Invoke-Native "twine check" { & $VENV_PY -m twine check (Join-Path $pyDist "*") }

# ---------------------------------------------------------------
# Summary
# ---------------------------------------------------------------

Write-Host ""
Write-Host "============================================" -ForegroundColor Green
Write-Host "  PYTHON BUILD SUCCESSFUL" -ForegroundColor Green
Write-Host "============================================" -ForegroundColor Green
Write-Host "  Artifacts: $pyDist"
Write-Host ""

if (-not $Publish) {
    Write-Host "Dry run complete. To publish, re-run with -Publish" -ForegroundColor Yellow
    exit 0
}

# ---------------------------------------------------------------
# Publish
# ---------------------------------------------------------------

Write-Step "Publishing to PyPI"

# Force UTF-8 to avoid rich/twine UnicodeEncodeError on GBK terminals
$env:PYTHONIOENCODING = "utf-8"

if ($TestPyPI) {
    Write-Host "Target: TestPyPI" -ForegroundColor Yellow
    Invoke-Native "twine upload" { & $VENV_PY -m twine upload --repository testpypi (Join-Path $pyDist "*") }
} else {
    Write-Host "Target: PyPI (production)" -ForegroundColor Yellow
    Invoke-Native "twine upload" { & $VENV_PY -m twine upload --repository pypi (Join-Path $pyDist "*") }
}

$env:PYTHONIOENCODING = $null

Write-Host ""
Write-Host "============================================" -ForegroundColor Green
Write-Host "  PYTHON PUBLISH COMPLETE" -ForegroundColor Green
Write-Host "============================================" -ForegroundColor Green
