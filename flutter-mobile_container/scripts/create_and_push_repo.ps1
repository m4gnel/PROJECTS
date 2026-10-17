<#
Creates a GitHub repository using the GitHub CLI (`gh`) and pushes the current project.
Usage:
  .\create_and_push_repo.ps1 -RepoName my-repo -Private -Description "My repo"

Requirements:
 - Install Git: https://git-scm.com/
 - Install GitHub CLI: https://cli.github.com/ and run `gh auth login` first
 - Run this script from the project root (d:\project\FLUTTER) in PowerShell
#>
param(
    [Parameter(Mandatory=$true)][string]$RepoName,
    [switch]$Private,
    [string]$Description = "Mobile Container - Device Test Suite",
    [string]$RemoteName = "origin"
)

function Ensure-GitInitialized {
    if (-not (Test-Path .git)) {
        Write-Host "Initializing git repository..."
        git init
    } else {
        Write-Host "Git repository already initialized."
    }
}

function Ensure-Commit {
    git add -A
    $status = git status --porcelain
    if (-not [string]::IsNullOrWhiteSpace($status)) {
        Write-Host "Creating initial commit..."
        git commit -m "chore: initial commit"
    } else {
        Write-Host "No changes to commit."
    }
}

function Create-GHRepo {
    $vis = if ($Private) { "--private" } else { "--public" }
    Write-Host "Creating repository on GitHub: $RepoName ($vis)"
    gh repo create $RepoName $vis --description "$Description" --confirm
}

function Add-Remote-And-Push {
    $remoteUrl = git remote get-url $RemoteName 2>$null
    if (-not $remoteUrl) {
        Write-Host "Adding remote '$RemoteName' and pushing..."
        git remote add $RemoteName git@github.com:$(gh api user --jq .login)/$RepoName.git 2>$null
    } else {
        Write-Host "Remote '$RemoteName' already exists."
    }
    git branch -M main 2>$null
    git push -u $RemoteName main --force
}

# Script execution
Ensure-GitInitialized
Ensure-Commit

# Create repo via gh
if (-not (Get-Command gh -ErrorAction SilentlyContinue)) {
    Write-Error "GitHub CLI (gh) not found. Install it and authenticate (gh auth login), then re-run this script."
    exit 1
}

Create-GHRepo
Add-Remote-And-Push

Write-Host "Done. Repository created and pushed. Visit: https://github.com/$(gh api user --jq .login)/$RepoName"