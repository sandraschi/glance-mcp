# Per-repo fleet start config for glance-mcp
# Edit ports/backend target here - start.ps1 is fleet-standard.
@{
    Name         = 'glance-mcp'
    BackendPort  = 10776
    FrontendPort = 10777
    HealthPath   = '/health'
    WebRoot      = 'web_sota'
    Backend = @{
        Kind = 'none'
    }
    Frontend = @{
        Kind = 'none'
    }
}
