@'
Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

function Run-Git {
    param([string[]]$Args)
    Write-Host ("`n>> git " + ($Args -join " "))
    & git @Args
    if ($LASTEXITCODE -ne 0) {
        throw ("Git command failed: git " + ($Args -join " "))
    }
}

function Assert-InRepo {
    & git rev-parse --is-inside-work-tree *> $null
    if ($LASTEXITCODE -ne 0) {
        throw "Run this script from inside the git repo root."
    }
}

function Ensure-RemoteOrigin {
    $remoteUrl = (& git remote get-url origin 2>$null)
    if (-not $remoteUrl) {
        throw "Remote 'origin' is not set."
    }
    Write-Host "origin -> $remoteUrl"
}

function Ensure-OnMain {
    $branch = (& git branch --show-current).Trim()
    if ($branch -ne "main") {
        Write-Host "Switching to main..."
        Run-Git @("checkout","main")
    }
}

function Remote-HasMain {
    & git ls-remote --exit-code --heads origin main *> $null
    return ($LASTEXITCODE -eq 0)
}

# ---------------- START ----------------
Assert-InRepo
Ensure-RemoteOrigin

Run-Git @("fetch","origin")
Ensure-OnMain

# -------- AUTO COMMIT --------
Run-Git @("add","-A")

& git diff --cached --quiet
$stagedHasChanges = ($LASTEXITCODE -ne 0)

if ($stagedHasChanges) {
    $tsCommit = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
    $msg = "Auto backup commit $tsCommit"
    Write-Host "Changes detected. Creating auto-backup commit..." -ForegroundColor Yellow
    Run-Git @("commit","-m",$msg)
}
else {
    Write-Host "No local changes to commit."
}

# -------- SYNC WITH REMOTE (only if origin/main exists) --------
if (Remote-HasMain) {
    Run-Git @("pull","--ff-only","origin","main")
}
else {
    Write-Host "origin/main not found yet — skipping pull."
}

# -------- CREATE BACKUP BRANCH --------
$ts = Get-Date -Format "yyyyMMdd-HHmmss"
$backupBranch = "backup/$ts"

Run-Git @("branch",$backupBranch,"HEAD")

# -------- PUSH BACKUP FIRST (hard stop if fails) --------
Run-Git @("push","origin",$backupBranch)

& git ls-remote --exit-code --heads origin $backupBranch *> $null
if ($LASTEXITCODE -ne 0) {
    throw "Backup branch '$backupBranch' not found on remote after push. ABORTING."
}

Write-Host "Backup branch created: $backupBranch" -ForegroundColor Green

# -------- PUSH MAIN --------
Run-Git @("push","-u","origin","main")

Write-Host ""
Write-Host "SUCCESS — Backup + Main pushed." -ForegroundColor Green
Write-Host "Remote backup branch: $backupBranch"
'@ | Set-Content -LiteralPath .\tools\backup_and_push.ps1 -Encoding utf8
