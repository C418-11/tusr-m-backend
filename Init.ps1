if (Test-Path .venv)
{
    Write-Host "'.venv' 目录已存在，跳过环境初始化。"

    # 激活虚拟环境
    Write-Host "正在激活虚拟环境..."
    .\.venv\Scripts\Activate.ps1
    if ($? -ne $true)
    {
        Write-Host "虚拟环境激活失败。"
        exit 1
    }
}
else
{
    # 创建虚拟环境
    Write-Host "正在创建虚拟环境..."
    python -m venv .venv
    if ($LASTEXITCODE -ne 0)
    {
        Write-Host "虚拟环境创建失败。"
        exit $LASTEXITCODE
    }

    # 激活虚拟环境
    Write-Host "正在激活虚拟环境..."
    .\.venv\Scripts\Activate.ps1
    if ($LASTEXITCODE -ne 0)
    {
        Write-Host "虚拟环境激活失败。"
        exit $LASTEXITCODE
    }

    # 安装依赖
    Write-Host "正在安装依赖..."
    python.exe -m pip install --upgrade pip
    pip install --force-reinstall -r requirements.txt
    if ($LASTEXITCODE -ne 0)
    {
        Write-Host "依赖安装失败。"
        exit $LASTEXITCODE
    }
}

if (Test-Path instance)
{
    Write-Host "'instance' 目录已存在，跳过 Flask 初始化。"
}
else
{
    # 初始化 Flask
    Write-Host "正在初始化 Flask..."
    flask init
    if ($LASTEXITCODE -ne 0)
    {
        Write-Host "Flask 初始化失败。"
        exit $LASTEXITCODE
    }
}

Write-Host "项目初始化完成。"
