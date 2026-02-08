Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

# -------- Config --------
$outFile = "AI_CONTEXT_SNAPSHOT.txt"

# Limit repo map scope (adjust if you want more)
$mapRoots = @("src", "AI_BRAIN")

# Only include these file types in REPO_MAP (keeps it compact)
$mapIncludeExtensions = @(".py", ".md", ".txt", ".sql", ".json", ".qss", ".yaml", ".yml")

# -------- Helpers --------
function Require-GitRepo {
    git rev-parse --is-inside-work-tree *> $null
    if ($LASTEXITCODE -ne 0) { throw "Run this script from the root of a git repository." }
}

function Get-RepoMeta {
    $hash   = (git rev-parse HEAD).Trim()
    $branch = (git rev-parse --abbrev-ref HEAD).Trim()
    $dirty  = (git status --porcelain)
    $dirtyFlag = if ($dirty) { "DIRTY (uncommitted changes present)" } else { "CLEAN" }

    return [PSCustomObject]@{
        Hash  = $hash
        Branch = $branch
        State = $dirtyFlag
        When = (Get-Date).ToString("yyyy-MM-dd HH:mm:ss zzz")
    }
}

function Normalize-RelPath([string]$fullPath) {
    $root = (Get-Location).Path.TrimEnd('\') + '\'
    return $fullPath.Replace($root, "").Replace('\', '/')
}

function Build-RepoMap([string[]]$roots, [string[]]$exts) {
    $lines = New-Object System.Collections.Generic.List[string]

    foreach ($r in $roots) {
        if (-not (Test-Path $r)) { continue }

        $lines.Add("## $r/")
        $files = Get-ChildItem -Path $r -Recurse -File -Force |
            Where-Object { $exts -contains $_.Extension.ToLowerInvariant() } |
            Sort-Object FullName

        foreach ($f in $files) {
            $rel = Normalize-RelPath $f.FullName
            $lines.Add($rel)
        }
        $lines.Add("")
    }

    if ($lines.Count -eq 0) {
        $lines.Add("(No matching files found under configured roots.)")
    }

    return $lines
}

function Build-ImportIndex([string]$root) {
    $lines = New-Object System.Collections.Generic.List[string]

    if (-not (Test-Path $root)) {
        $lines.Add("(src/ not found; import index skipped.)")
        return $lines
    }

    $pyFiles = Get-ChildItem -Path $root -Recurse -File -Filter *.py -Force |
        Sort-Object FullName

    foreach ($f in $pyFiles) {
        $rel = Normalize-RelPath $f.FullName

        # Pull only actual import statements at line start.
        # (Keeps it readable; avoids matching "import" in strings/comments mid-line.)
        $imports = Get-Content -LiteralPath $f.FullName -ErrorAction Stop |
            ForEach-Object { $_.TrimEnd() } |
            Where-Object { $_ -match '^(from\s+\S+\s+import\s+|import\s+\S+)' }

        if ($imports.Count -gt 0) {
            $lines.Add("### $rel")
            foreach ($line in $imports) { $lines.Add($line) }
            $lines.Add("")
        }
    }

    if ($lines.Count -eq 0) {
        $lines.Add("(No Python import statements found under src/.)")
    }

    return $lines
}

# -------- Main --------
Require-GitRepo
$meta = Get-RepoMeta

$repoMapLines = Build-RepoMap -roots $mapRoots -exts $mapIncludeExtensions
$importLines  = Build-ImportIndex -root "src"

# Write one file, consistently formatted
$header = @()
$header += "=============================="
$header += "AI CONTEXT SNAPSHOT"
$header += "=============================="
$header += "Timestamp : $($meta.When)"
$header += "Branch    : $($meta.Branch)"
$header += "HEAD hash : $($meta.Hash)"
$header += "Repo state: $($meta.State)"
$header += ""

$sections = @()
$sections += "=============================="
$sections += "REPO MAP (filtered)"
$sections += "=============================="
$sections += $repoMapLines
$sections += ""
$sections += "=============================="
$sections += "IMPORT INDEX (src/**/*.py)"
$sections += "=============================="
$sections += $importLines
$sections += ""

($header + $sections) | Out-File -FilePath $outFile -Encoding UTF8 -Force

Write-Host "Wrote: $outFile" -ForegroundColor Green
Write-Host "HEAD:  $($meta.Hash)  ($($meta.State))"
