# glance-mcp — just recipes (Windows-friendly; use `;` in PowerShell if chaining manually)

default:
    just --list

run serve:
    uv run glance-mcp --serve

stdio:
    uv run glance-mcp

lint check:
    uv run ruff check .
    uv run ruff format --check .

format fmt:
    uv run ruff format .

test:
    uv sync --extra dev
    uv run pytest tests -v

install:
    uv sync

install-web:
    cd web_sota
    npm install

web start:
    .\web_sota\start.ps1

clean:
    powershell -NoProfile -Command "Remove-Item -Recurse -Force -ErrorAction SilentlyContinue dist, build, .ruff_cache, .pytest_cache, web_sota/node_modules, web_sota/dist; Get-ChildItem -Recurse -Directory -Filter __pycache__ | Remove-Item -Recurse -Force -ErrorAction SilentlyContinue; Write-Host 'Cleaned.'"

health:
    curl.exe -s http://127.0.0.1:10776/health
