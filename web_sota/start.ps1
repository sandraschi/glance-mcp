Param([switch]$Headless)

# --- SOTA Headless Standard ---
if ($Headless -and ($Host.UI.RawUI.WindowTitle -notmatch 'Hidden')) {
    Start-Process pwsh -ArgumentList '-NoProfile', '-File', $PSCommandPath, '-Headless' -WindowStyle Hidden
    exit
}
$WindowStyle = if ($Headless) { 'Hidden' } else { 'Normal' }
# ------------------------------

# glance-mcp â€” backend 10776 + Vite 10777 (fleet adjacent ports)
$ErrorActionPreference = "Stop"
$root = Split-Path -Parent $PSScriptRoot
Set-Location $root

foreach ($p in 10776, 10777) {
    Get-NetTCPConnection -LocalPort $p -ErrorAction SilentlyContinue |
        ForEach-Object { Stop-Process -Id $_.OwningProcess -Force -ErrorAction SilentlyContinue }
}

Start-Process -FilePath "uv" -ArgumentList "run", "glance-mcp", "--serve" -WorkingDirectory $root -WindowStyle Hidden
Start-Sleep -Seconds 2

Set-Location $PSScriptRoot
if (-not (Test-Path "node_modules")) {
    npm install
}
Start-Process "http://127.0.0.1:10777/"
npm run dev

