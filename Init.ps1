if (Test-Path .venv)
{
    Write-Host "'.venv' Ŀ¼�Ѵ��ڣ�����������ʼ����"

    # �������⻷��
    Write-Host "���ڼ������⻷��..."
    .\.venv\Scripts\Activate.ps1
    if ($? -ne $true)
    {
        Write-Host "���⻷������ʧ�ܡ�"
        exit 1
    }
}
else
{
    # �������⻷��
    Write-Host "���ڴ������⻷��..."
    python -m venv .venv
    if ($LASTEXITCODE -ne 0)
    {
        Write-Host "���⻷������ʧ�ܡ�"
        exit $LASTEXITCODE
    }

    # �������⻷��
    Write-Host "���ڼ������⻷��..."
    .\.venv\Scripts\Activate.ps1
    if ($LASTEXITCODE -ne 0)
    {
        Write-Host "���⻷������ʧ�ܡ�"
        exit $LASTEXITCODE
    }

    # ��װ����
    Write-Host "���ڰ�װ����..."
    python.exe -m pip install --upgrade pip
    pip install --force-reinstall -r requirements.txt
    if ($LASTEXITCODE -ne 0)
    {
        Write-Host "������װʧ�ܡ�"
        exit $LASTEXITCODE
    }
}

if (Test-Path instance)
{
    Write-Host "'instance' Ŀ¼�Ѵ��ڣ����� Flask ��ʼ����"
}
else
{
    # ��ʼ�� Flask
    Write-Host "���ڳ�ʼ�� Flask..."
    flask init
    if ($LASTEXITCODE -ne 0)
    {
        Write-Host "Flask ��ʼ��ʧ�ܡ�"
        exit $LASTEXITCODE
    }
}

Write-Host "��Ŀ��ʼ����ɡ�"
