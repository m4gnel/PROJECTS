<#
Wrapper script to create repo, push code, and optionally create a release.
Usage examples (PowerShell):
  # create repo and push
  .\push_all.ps1 -RepoName mobile_container -Private

  # create repo, push and create release v1.0.0
  .\push_all.ps1 -RepoName mobile_container -Private -CreateRelease -Tag v1.0.0 -Title "v1.0.0" -Notes "Initial release"

Requirements:
 - Run from project root (d:\project\FLUTTER)
 - Git and gh (GitHub CLI) installed and authenticated
#>
param(
    [Parameter(Mandatory=$true)][string]$RepoName,
    [switch]$Private,
    [switch]$CreateRelease,
    [string]$Tag = "v1.0.0",
    [string]$Title = "v1.0.0",
    [string]$Notes = "Initial release",
    [string]$RemoteName = "origin"
)

function Resolve-Command($cmd, [string[]]$fallbackPaths) {
    $command = Get-Command $cmd -ErrorAction SilentlyContinue
    if ($command) {
        return $command.Source
    }

    foreach ($path in $fallbackPaths) {
        if (Test-Path $path) {
            return $path
        }
    }

    return $null
}

$GitPath = Resolve-Command 'git' @(
    'C:\Program Files\Git\cmd\git.exe',
    'C:\Program Files\Git\bin\git.exe',
    'C:\Program Files\Git\mingw64\bin\git.exe'
)

$GhPath = Resolve-Command 'gh' @(
    'C:\Program Files\GitHub CLI\gh.exe',
    "$env:LOCALAPPDATA\Programs\GitHub CLI\gh.exe"
)

if (-not $GitPath) {
    Write-Error "git not found. Please install Git and ensure it is on PATH or in one of the standard install locations."
    exit 1
}

if (-not $GhPath) {
    Write-Error "gh not found. Please install GitHub CLI and ensure it is on PATH or in one of the standard install locations."
    exit 1
}

# Ensure git repo
if (-not (Test-Path .git)) {
    & "$GitPath" init
}

# Ensure .gitignore exists (we already added one but keep safe)
if (-not (Test-Path ".gitignore")) {
    Write-Host "No .gitignore found. Creating default .gitignore"
@"
.DS_Store
build/
.idea/
.vscode/
.dart_tool/
.packages
.pub/
"@ | Out-File -FilePath .gitignore -Encoding utf8
}

# Stage and commit
& "$GitPath" add -A
$status = & "$GitPath" status --porcelain
if (-not [string]::IsNullOrWhiteSpace($status)) {
    & "$GitPath" commit -m "chore: initial commit"
} else {
    Write-Host "No changes to commit."
}

# Create repo via gh
$vis = if ($Private) { "--private" } else { "--public" }
& "$GhPath" repo create $RepoName $vis --description "Mobile Container — Device Test Suite" --confirm

# Add remote
$remoteUrl = & "$GitPath" remote get-url $RemoteName 2>$null
if (-not $remoteUrl) {
    $owner = & "$GhPath" api user --jq .login
    & "$GitPath" remote add $RemoteName "git@github.com:$owner/$RepoName.git"
} else {
    Write-Host "Remote '$RemoteName' already exists: $remoteUrl"
}

# Push
& "$GitPath" branch -M main 2>$null
& "$GitPath" push -u $RemoteName main --force

$owner = & "$GhPath" api user --jq .login
Write-Host "Repository created and pushed: https://github.com/$owner/$RepoName"

if ($CreateRelease) {
    Write-Host "Creating release $Tag"
    & "$GitPath" tag -a $Tag -m "$Title"
    & "$GitPath" push $RemoteName $Tag
    & "$GhPath" release create $Tag --title "$Title" --notes "$Notes"
    Write-Host "Release $Tag created."
}
