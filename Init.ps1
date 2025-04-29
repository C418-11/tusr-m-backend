# 1. 创建虚拟环境
python -m venv .venv
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }

# 2. 激活虚拟环境
.\.venv\Scripts\Activate.ps1
if (-not $?) { exit 1 }

# 3. 安装依赖
pip install --force-reinstall -r requirements.txt
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }

# 4. 初始化 Flask
flask init
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
