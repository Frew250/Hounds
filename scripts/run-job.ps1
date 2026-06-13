[CmdletBinding()]
param(
    [Parameter(ValueFromRemainingArguments = $true)]
    [string[]]$Arguments
)

$RootProjectDir = (Resolve-Path (Join-Path $PSScriptRoot "..\..\..")).Path
$ClientSlug = Split-Path -Leaf (Split-Path -Parent $PSScriptRoot)
$RootScript = Join-Path $RootProjectDir "scripts\run-job.ps1"
$env:AGENTIC_OS_DIR = $RootProjectDir

$ForwardedArguments = @()
if ($Arguments) {
    $ForwardedArguments += $Arguments
}
$ForwardedArguments += @("--client", $ClientSlug)

& $RootScript @ForwardedArguments
