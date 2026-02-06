Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"
$env:GIT_TERMINAL_PROMPT = "0"

function Run-Git {
    param(
        [Parameter(Mandatory = $true)]
        [string[]]$Args
    )

    if (-not $Args -or $Args.Count -eq 0) {
        throw "Run-Git was called with no arguments. Fix the call site."
    }

    $cmdLine = "git " + ($Args -join " ")
    Write-Host ("`n>> " + $cmdLine)

    # Git sometimes writes normal info/progress to stderr.
    # PowerShell can treat stderr as an error record, which would stop the script.
    # We temporarily suppress non-terminating errors and rely ONLY on exit code.
    $prevEap = $ErrorActionPreference
    $ErrorActionPreference = "Continue"

    $output = & git @Args 2>&1
    $exit = $LASTEXITCODE

    $ErrorActionPreference = $prevEap

    if ($output) {
        $output | ForEach-Object { Write-Host $_ }
    }

    if ($exit -ne 0) {
        throw ("Git command failed (exit $exit): " + $cmdLine)
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

function Ensure-Main-Exists-Locally {
    $branch = (& git branch --show-current).Trim()
    if (-not $branch) {
        # Detached HEAD or no branch context
        Run-Git @("checkout","-b","main")
        return
    }

    # If we're on a different branch, keep it; we'll switch later.
}

function Checkout-Main {
    $branch = (& git branch --show-current).Trim()
    if ($branch -ne "main") {
        # Ensure main exists locally; if not, create it from current HEAD.
        & git show-ref --verify --quiet refs/heads/main
        if ($LASTEXITCODE -ne 0) {
            Run-Git @("branch","main","HEAD")
        }
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

Ensure-Main-Exists-Locally
Checkout-Main

# -------- AUTO COMMIT --------
Run-Git @("add","-A")

& git diff --cached --quiet
$stagedHasChanges = ($LASTEXITCODE -ne 0)

if ($stagedHasChanges) {
    $tsCommit = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
    $msg = "Auto backup commit $tsCommit"
    Write-Host "Changes detected. Creating auto-backup commit..." -ForegroundColor Yellow
    Run-Git @("commit","-m",$msg)
} else {
    Write-Host "No local changes to commit."
}

# -------- SYNC WITH REMOTE (only if origin/main exists) --------
if (Remote-HasMain) {
    Run-Git @("pull","--ff-only","origin","main")
} else {
    Write-Host "origin/main not found yet - skipping pull."
}

# -------- CREATE BACKUP BRANCH --------
$ts = Get-Date -Format "yyyyMMdd-HHmmss"
$backupBranch = "backup/$ts"

Run-Git @("branch",$backupBranch,"HEAD")

# -------- PUSH BACKUP FIRST (hard stop if fails) --------
Run-Git @("push","origin",$backupBranch)

# Verify backup exists remotely
Run-Git @("ls-remote","--exit-code","--heads","origin",$backupBranch)

Write-Host "Backup branch created: $backupBranch" -ForegroundColor Green

# -------- PUSH MAIN --------
Run-Git @("push","-u","origin","main")

Write-Host ""
Write-Host "SUCCESS - Backup + Main pushed." -ForegroundColor Green
Write-Host "Remote backup branch: $backupBranch"
