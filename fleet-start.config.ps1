# Per-repo fleet start config for glance-mcp
# Edit ports/backend target here - start.ps1 is fleet-standard.
@{
    Name         = 'glance-mcp'
    BackendPort  = 10776
    FrontendPort = 10777
    HealthPath   = '/api/health'
    WebRoot      = 'web_sota'
    Backend = @{
        Kind          = 'uvicorn'
        UvicornTarget = 'web_sota.backend.server:app'
        SyncExtras    = @('dev')
        SyncOnStart   = $true
        Env           = @{ WEB_PORT = '10776' }
    }
    Frontend = @{
        Kind           = 'vite-npm'
        PackageManager = 'npm'
    }
}
