param(
  [Parameter(Mandatory=$false)]
  [string]$Root = (Get-Location).Path,

  [Parameter(Mandatory=$false)]
  [string]$OutFile = $null
)

Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

function Should-ExcludeDir([string]$name) {
  $exclude = @(
    ".git", ".idea", ".vscode",
    "__pycache__", ".pytest_cache", ".mypy_cache",
    ".venv", "venv", "env",
    "node_modules", "dist", "build", ".ruff_cache"
  )
  return $exclude -contains $name
}

function Should-ExcludeFile([string]$name) {
  $exclude = @(
    "PROJECT_DUMP.txt", "PROJECT_DIRECTORIES.txt"
  )
  return $exclude -contains $name
}

function Get-ChildrenSorted([string]$path) {
  $dirs  = @(Get-ChildItem -LiteralPath $path -Force -Directory | Where-Object { -not (Should-ExcludeDir $_.Name) } | Sort-Object Name)
  $files = @(Get-ChildItem -LiteralPath $path -Force -File      | Where-Object { -not (Should-ExcludeFile $_.Name) } | Sort-Object Name)
  return @($dirs + $files)
}

function Write-Tree([string]$path, [string]$prefix, [bool]$isRoot, [System.Collections.Generic.List[string]]$lines) {
  $name = Split-Path -Leaf $path
  if ($isRoot) { $lines.Add("$name/") }

  $children = @(Get-ChildrenSorted $path)
  $n = $children.Length

  for ($i = 0; $i -lt $n; $i++) {
    $child = $children[$i]
    $isLast = ($i -eq $n - 1)

    $branch = if ($isLast) { "\-- " } else { "|-- " }
    $nextPrefix = if ($isLast) { "$prefix    " } else { "$prefix|   " }

    if ($child.PSIsContainer) {
      $lines.Add("$prefix$branch$($child.Name)/")
      Write-Tree -path $child.FullName -prefix $nextPrefix -isRoot $false -lines $lines
    } else {
      $lines.Add("$prefix$branch$($child.Name)")
    }
  }
}

# Normalize Root to a single directory path (prevents the “many paths glued together” bug)
$Root = [string]$Root
$Root = ($Root -split "(`r`n|`n|`r)")[0].Trim()

if (-not (Test-Path -LiteralPath $Root -PathType Container)) {
  throw "Root folder not found: $Root"
}

if (-not $OutFile) {
  $OutFile = Join-Path $Root "PROJECT_DIRECTORIES.txt"
}

$lines = New-Object System.Collections.Generic.List[string]
Write-Tree -path $Root -prefix "" -isRoot $true -lines $lines

$utf8NoBom = New-Object System.Text.UTF8Encoding($false)
[System.IO.File]::WriteAllText($OutFile, ($lines -join "`r`n") + "`r`n", $utf8NoBom)

Write-Host "Wrote: $OutFile"
