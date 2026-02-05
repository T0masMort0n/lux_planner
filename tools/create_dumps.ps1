Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

# ---------------------------
# Config (edit if you want)
# ---------------------------
# Folder that contains THIS script
$SCRIPT_DIR = Split-Path -Parent $MyInvocation.MyCommand.Path

# If this script is in ".../lux_planner/tools", then ROOT is the parent of tools.
# If it's not, ROOT is SCRIPT_DIR itself.
if ((Split-Path -Leaf $SCRIPT_DIR).ToLowerInvariant() -eq "tools") {
  $ROOT = Split-Path -Parent $SCRIPT_DIR
} else {
  $ROOT = $SCRIPT_DIR
}

$DUMPS_DIR = Join-Path $ROOT "dumps"

# Create dumps folder if it doesn't exist
if (-not (Test-Path -LiteralPath $DUMPS_DIR)) {
  New-Item -ItemType Directory -Path $DUMPS_DIR | Out-Null
}

$OUT_DIRS = Join-Path $DUMPS_DIR "PROJECT_DIRECTORIES.txt"
$OUT_DUMP = Join-Path $DUMPS_DIR "PROJECT_DUMP.txt"

Write-Host "ROOT resolved to: $ROOT"
Write-Host "DUMPS_DIR: $DUMPS_DIR"


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

function Should-SkipDumpFileByExt([string]$fullPath) {
  $lower = $fullPath.ToLowerInvariant()
  $skipExt = @(
    ".png",".jpg",".jpeg",".gif",".webp",".ico",".icns",
    ".mp3",".mp4",".mov",".mkv",".wav",".flac",
    ".zip",".7z",".rar",".exe",".dll",".pdb",
    ".pdf",
    ".db",".sqlite",".sqlite3"
  )
  foreach ($ext in $skipExt) {
    if ($lower.EndsWith($ext)) { return $true }
  }
  return $false
}

function Is-ProbablyBinary([byte[]]$bytes) {
  $limit = [Math]::Min($bytes.Length, 4096)
  for ($i=0; $i -lt $limit; $i++) {
    if ($bytes[$i] -eq 0) { return $true }
  }
  return $false
}

function Get-ChildrenSorted([string]$path) {
  $dirs  = @(Get-ChildItem -LiteralPath $path -Force -Directory |
    Where-Object { -not (Should-ExcludeDir $_.Name) } |
    Sort-Object Name)

  $files = @(Get-ChildItem -LiteralPath $path -Force -File |
    Where-Object { -not (Should-ExcludeFile $_.Name) } |
    Sort-Object Name)

  return @($dirs + $files)
}

function Get-RelativePath([string]$Base, [string]$Path) {
  $baseFull = [System.IO.Path]::GetFullPath($Base)
  if (-not $baseFull.EndsWith([System.IO.Path]::DirectorySeparatorChar)) {
    $baseFull += [System.IO.Path]::DirectorySeparatorChar
  }

  $pathFull = [System.IO.Path]::GetFullPath($Path)

  $baseUri = New-Object System.Uri($baseFull)
  $pathUri = New-Object System.Uri($pathFull)

  $relUri = $baseUri.MakeRelativeUri($pathUri)
  $rel = [System.Uri]::UnescapeDataString($relUri.ToString())

  return $rel -replace '/', '\'
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

function Collect-FilesInTraversalOrder([string]$path, [System.Collections.Generic.List[string]]$files) {
  $children = @(Get-ChildrenSorted $path)
  foreach ($child in $children) {
    if ($child.PSIsContainer) {
      Collect-FilesInTraversalOrder -path $child.FullName -files $files | Out-Null
    } else {
      if (-not (Should-SkipDumpFileByExt $child.FullName)) {
        [void]$files.Add($child.FullName)
      }
    }
  }
}

# ---------------------------
# Validate root
# ---------------------------
if (-not (Test-Path -LiteralPath $ROOT -PathType Container)) {
  throw "Root folder not found: $ROOT"
}

# ---------------------------
# 1) PROJECT_DIRECTORIES.txt
# ---------------------------
$lines = New-Object System.Collections.Generic.List[string]
Write-Tree -path $ROOT -prefix "" -isRoot $true -lines $lines

$utf8NoBom = New-Object System.Text.UTF8Encoding($false)
[System.IO.File]::WriteAllText($OUT_DIRS, ($lines -join "`r`n") + "`r`n", $utf8NoBom)
Write-Host "Wrote: $OUT_DIRS"

# ---------------------------
# 2) PROJECT_DUMP.txt
# ---------------------------
$files = New-Object System.Collections.Generic.List[string]
Collect-FilesInTraversalOrder -path $ROOT -files $files | Out-Null

$sb = New-Object System.Text.StringBuilder
$sb.AppendLine("# PROJECT_DUMP.txt") | Out-Null
$sb.AppendLine("# Root: $ROOT") | Out-Null
$sb.AppendLine("# Generated: $(Get-Date -Format 'yyyy-MM-dd HH:mm:ss')") | Out-Null
$sb.AppendLine("") | Out-Null

foreach ($full in $files) {
  $rel = Get-RelativePath $ROOT $full
  $sb.AppendLine("==== FILE: $rel ====") | Out-Null

  $bytes = [System.IO.File]::ReadAllBytes($full)
  if (Is-ProbablyBinary $bytes) {
    $sb.AppendLine("[Skipped: binary]") | Out-Null
    $sb.AppendLine("") | Out-Null
    continue
  }

  $text = ""
  try {
    $text = [System.IO.File]::ReadAllText($full, $utf8NoBom)
  } catch {
    try { $text = [System.IO.File]::ReadAllText($full) }
    catch { $text = "[Could not read file as text]" }
  }

  $sb.AppendLine($text.TrimEnd()) | Out-Null
  $sb.AppendLine("") | Out-Null
}

[System.IO.File]::WriteAllText($OUT_DUMP, $sb.ToString(), $utf8NoBom)
Write-Host "Wrote: $OUT_DUMP"
Write-Host "Dumped files: $($files.Count)"
