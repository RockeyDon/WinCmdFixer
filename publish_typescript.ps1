<#
.SYNOPSIS
    Build, test and publish win-cmd-fixer (TypeScript) to npm.

.EXAMPLE
    .\publish_typescript.ps1                    # Build only
    .\publish_typescript.ps1 -Publish           # Build & publish to npm
    .\publish_typescript.ps1 -Publish -DryRun   # npm publish --dry-run
    .\publish_typescript.ps1 -Publish -Otp 123456   # Publish with 2FA OTP
#>

param(
    [switch]$Publish,
    [switch]$DryRun,
    [string]$Otp
)

Set-StrictMode -Version 1.0

$ROOT   = Split-Path -Parent $MyInvocation.MyCommand.Definition
$TS_DIR = Join-Path $ROOT "typescript"

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

$ErrorActionPreference = "Continue"
$npmVer = & npm.cmd --version 2>&1 | Select-Object -Last 1
$ErrorActionPreference = "Stop"
if (-not $npmVer) {
    Write-Host "npm is not installed or not in PATH." -ForegroundColor Red
    exit 1
}

# ---------------------------------------------------------------
# Install & Test
# ---------------------------------------------------------------

Push-Location $TS_DIR

Write-Step "Installing dependencies"
Invoke-Native "npm install" { & npm.cmd install --silent }

Write-Step "Running tests"
Invoke-Native "jest" { & npx.cmd jest --verbose }

# ---------------------------------------------------------------
# Clean & Build
# ---------------------------------------------------------------

Write-Step "Cleaning previous artifacts"
$tsDist = Join-Path $TS_DIR "dist"
if (Test-Path $tsDist) { Remove-Item $tsDist -Recurse -Force }

Write-Step "Compiling TypeScript"
Invoke-Native "tsc" { & npx.cmd tsc }

# ---------------------------------------------------------------
# Summary
# ---------------------------------------------------------------

Write-Host ""
Write-Host "============================================" -ForegroundColor Green
Write-Host "  TYPESCRIPT BUILD SUCCESSFUL" -ForegroundColor Green
Write-Host "============================================" -ForegroundColor Green
Write-Host "  Artifacts: $tsDist"
Write-Host ""

if (-not $Publish) {
    Write-Host "Dry run complete. To publish, re-run with -Publish" -ForegroundColor Yellow
    Pop-Location
    exit 0
}

# ---------------------------------------------------------------
# Publish
# ---------------------------------------------------------------

Write-Step "Publishing to npm"

# Build the argument list
$npmArgs = @("publish")
if ($DryRun) {
    Write-Host "Target: npm (dry-run)" -ForegroundColor Yellow
    $npmArgs += "--dry-run"
} else {
    Write-Host "Target: npm (production)" -ForegroundColor Yellow
}
if ($Otp) {
    $npmArgs += "--otp"
    $npmArgs += $Otp
}

Invoke-Native "npm publish" { & npm.cmd @npmArgs }

Pop-Location

Write-Host ""
Write-Host "============================================" -ForegroundColor Green
Write-Host "  TYPESCRIPT PUBLISH COMPLETE" -ForegroundColor Green
Write-Host "============================================" -ForegroundColor Green
