# 1. 激活 Python 虚拟环境
.\.venv\Scripts\Activate.ps1
if (-not $?) {
    exit 1
}

# 2. 启动 Flask 应用
Clear-Host
python .\app.py
if ($LASTEXITCODE -ne 0) {
    exit $LASTEXITCODE
}