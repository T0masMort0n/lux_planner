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

function Should-SkipDumpFile([string]$fullPath) {
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
  $dirs  = @(Get-ChildItem -LiteralPath $path -Force -Directory | Where-Object { -not (Should-ExcludeDir $_.Name) } | Sort-Object Name)
  $files = @(Get-ChildItem -LiteralPath $path -Force -File      | Where-Object { -not (Should-ExcludeFile $_.Name) } | Sort-Object Name)
  return @($dirs + $files)
}

function Collect-FilesInTraversalOrder([string]$path, [System.Collections.Generic.List[string]]$files) {
  $children = @(Get-ChildrenSorted $path)
  foreach ($child in $children) {
    if ($child.PSIsContainer) {
      Collect-FilesInTraversalOrder -path $child.FullName -files $files
    } else {
      if (-not (Should-SkipDumpFile $child.FullName)) {
        $files.Add($child.FullName)
      }
    }
  }
}

# Normalize Root
$Root = [string]$Root
$Root = ($Root -split "(`r`n|`n|`r)")[0].Trim()

if (-not (Test-Path -LiteralPath $Root -PathType Container)) {
  throw "Root folder not found: $Root"
}

if (-not $OutFile) {
  $OutFile = Join-Path $Root "PROJECT_DUMP.txt"
}

# Collect files in EXACT same order as directories tree traversal
$files = New-Object System.Collections.Generic.List[string]
Collect-FilesInTraversalOrder -path $Root -files $files

$sb = New-Object System.Text.StringBuilder
$sb.AppendLine("# PROJECT_DUMP.txt")
$sb.AppendLine("# Root: $Root")
$sb.AppendLine("# Generated: $(Get-Date -Format 'yyyy-MM-dd HH:mm:ss')")
$sb.AppendLine("")

foreach ($full in $files) {
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

  # Convert URI slashes to Windows slashes
  return $rel -replace '/', '\'
}


  $sb.AppendLine("==== FILE: $rel ====")

  $bytes = [System.IO.File]::ReadAllBytes($full)
  if (Is-ProbablyBinary $bytes) {
    $sb.AppendLine("[Skipped: binary]")
    $sb.AppendLine("")
    continue
  }

  $text = ""
  try {
    $utf8NoBom = New-Object System.Text.UTF8Encoding($false)
    $text = [System.IO.File]::ReadAllText($full, $utf8NoBom)
  } catch {
    try { $text = [System.IO.File]::ReadAllText($full) }
    catch { $text = "[Could not read file as text]" }
  }

  $sb.AppendLine($text.TrimEnd())
  $sb.AppendLine("")
}

$utf8NoBomOut = New-Object System.Text.UTF8Encoding($false)
[System.IO.File]::WriteAllText($OutFile, $sb.ToString(), $utf8NoBomOut)

Write-Host "Wrote: $OutFile"
Write-Host "Dumped files: $($files.Count)"
