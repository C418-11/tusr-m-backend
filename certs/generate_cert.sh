#!/bin/bash

# 生成自签名证书的配置文件
CONFIG_FILE="openssl.cnf"

cat > "$CONFIG_FILE" <<EOF
[req]
prompt = no
default_bits = 2048
default_md = sha256
distinguished_name = dn
x509_extensions = v3_req

[dn]
CN = localhost

[v3_req]
keyUsage = digitalSignature, keyEncipherment, dataEncipherment
extendedKeyUsage = serverAuth
subjectAltName = @alt_names

[alt_names]
DNS.1 = localhost
IP.1 = 127.0.0.1
EOF

# 生成证书和密钥
openssl req \
  -x509 \
  -nodes \
  -newkey rsa:2048 \
  -keyout server.key \
  -out server.crt \
  -days 365 \
  -config "$CONFIG_FILE"

# 清理临时文件
rm "$CONFIG_FILE"

# 输出使用说明
echo -e "\n\033[32m证书生成成功！\033[0m"
echo -e "生成的证书文件：server.crt"
echo -e "生成的密钥文件：server.key\n"

echo -e "\033[33m请按照以下步骤使浏览器信任该证书：\033[0m"
echo "1. 将 server.crt 文件复制到Windows系统"
echo "2. 右键点击证书文件 -> 选择'安装证书'"
echo "3. 存储位置选择'本地计算机' -> 下一步"
echo "4. 选择'将所有证书放入下列存储' -> 浏览 -> 受信任的根证书颁发机构 -> 确定"
echo "5. 点击下一步 -> 完成 -> 确定"
echo -e "\n在Flask中使用的示例命令："
echo -e "\033[36mflask run --cert=server.crt --key=server.key\033[0m"