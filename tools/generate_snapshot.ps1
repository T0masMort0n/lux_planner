Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

# Output file name
$outFileName = "AI_CONTEXT_SNAPSHOT.txt"

# --- Find repo root from wherever we are (tools/ is fine) ---
$repoRoot = (& git rev-parse --show-toplevel 2>$null).Trim()
if (-not $repoRoot) {
    throw "Not inside a git repository (git rev-parse --show-toplevel failed)."
}

Push-Location $repoRoot
try {
    # --- Repo metadata ---
    $hash   = (git rev-parse HEAD).Trim()
    $branch = (git rev-parse --abbrev-ref HEAD).Trim()
    $dirty  = (git status --porcelain)
    $state  = if ($dirty) { "DIRTY (uncommitted changes present)" } else { "CLEAN" }
    $when   = (Get-Date).ToString("yyyy-MM-dd HH:mm:ss zzz")

    # --- Resolve AI BRAIN directory (supports "AI BRAIN" and fallback) ---
    $aiBrainDir = Join-Path $repoRoot "AI BRAIN"
    if (-not (Test-Path -LiteralPath $aiBrainDir)) {
        $fallback = Join-Path $repoRoot "AI_BRAIN"
        if (Test-Path -LiteralPath $fallback) {
            $aiBrainDir = $fallback
        } else {
            # Create the intended folder name if neither exists
            New-Item -ItemType Directory -Path $aiBrainDir | Out-Null
        }
    }

    $outPath = Join-Path $aiBrainDir $outFileName

    # --- REPO MAP: use git so paths are relative to repo root (lux_planner/) ---
    # This lists tracked files only (respects .gitignore)
    $repoMap = & git ls-files
    if (-not $repoMap -or $repoMap.Count -eq 0) {
        $repoMap = @("(No tracked files returned by git ls-files.)")
    }

    # --- IMPORT INDEX: use git grep for fast, consistent import discovery ---
    # Output format: path:lineNumber:importLine (paths are relative to repo root)
    $importIndex = & git grep -nE '^(from\s+\S+\s+import\s+|import\s+\S+)' -- "*.py"
    if (-not $importIndex -or $importIndex.Count -eq 0) {
        $importIndex = @("(No Python import lines found via git grep.)")
    }

@"
==============================
AI CONTEXT SNAPSHOT
==============================
Timestamp : $when
Repo root : lux_planner/
Branch    : $branch
HEAD hash : $hash
Repo state: $state

==============================
REPO MAP (git ls-files; relative to lux_planner/)
==============================
$($repoMap -join "`r`n")

==============================
IMPORT INDEX (git grep; relative to lux_planner/)
==============================
$($importIndex -join "`r`n")
"@ | Out-File -FilePath $outPath -Encoding UTF8 -Force

    Write-Host "Wrote snapshot to: $outPath" -ForegroundColor Green
    Write-Host "HEAD: $hash ($state)" -ForegroundColor Green
}
finally {
    Pop-Location
}
