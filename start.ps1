Param([switch]$Headless)

# --- SOTA Headless Standard ---
if ($Headless -and ($Host.UI.RawUI.WindowTitle -notmatch 'Hidden')) {
    Start-Process pwsh -ArgumentList '-NoProfile', '-File', $PSCommandPath, '-Headless' -WindowStyle Hidden
    exit
}
$WindowStyle = if ($Headless) { 'Hidden' } else { 'Normal' }
# ------------------------------

$env:FASTMCP_LOG_LEVEL = 'WARNING'
# glance-mcp Start - Standards-Compliant SOTA
Write-Host 'Starting glance-mcp...' -ForegroundColor Cyan

Set-Location $PSScriptRoot
Write-Host 'Starting Standardized Fullstack Hybrid...' -ForegroundColor Green
# Launch backend Hidden by default to prevent console spam
Start-Process pwsh -ArgumentList '-NoProfile', '-Command', 'uv run -m glance_mcp' -WindowStyle Hidden
Set-Location web_sota
npm run dev