<#
Create and push a Git tag and GitHub release using `gh`.
Usage:
  .\create_release.ps1 -Tag v1.0.0 -Title "v1.0.0" -Notes "Release notes"

Requirements:
 - Git installed and repository initialized
 - GitHub CLI (`gh`) installed and authenticated
#>
param(
    [Parameter(Mandatory=$true)][string]$Tag,
    [string]$Title = $Tag,
    [string]$Notes = "",
    [string]$Remote = "origin"
)

if (-not (Get-Command git -ErrorAction SilentlyContinue)) {
    Write-Error "git not found. Install git and run this script from the project root."
    exit 1
}
if (-not (Get-Command gh -ErrorAction SilentlyContinue)) {
    Write-Error "gh (GitHub CLI) not found. Install it and authenticate (gh auth login)."
    exit 1
}

# create tag
Write-Host "Creating tag $Tag"
git tag -a $Tag -m "$Title"

# push tag
Write-Host "Pushing tag to $Remote"
git push $Remote $Tag

# create GitHub release
Write-Host "Creating GitHub release $Title"
if ([string]::IsNullOrEmpty($Notes)) {
    gh release create $Tag --title "$Title" --draft --notes ""
} else {
    gh release create $Tag --title "$Title" --notes "$Notes"
}

Write-Host "Release created."
