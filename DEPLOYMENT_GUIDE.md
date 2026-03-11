# 博客部署完整指南

## 目录
- [服务器信息](#服务器信息)
- [前置准备](#前置准备)
- [部署步骤](#部署步骤)
- [域名解析配置](#域名解析配置)
- [SSL证书安装](#ssl证书安装)
- [测试验证](#测试验证)
- [常见问题解决](#常见问题解决)
- [维护建议](#维护建议)

---

## 服务器信息

### 服务器详情
- **服务器IP**：115.190.238.160
- **操作系统**：Ubuntu 24.04 LTS
- **用户名**：root
- **密码**：Qiuhe123
- **域名**：qiuheagent.top

### 网站信息
- **网站目录**：/var/www/qiuheagent.top
- **主域名**：qiuheagent.top
- **子域名**：www.qiuheagent.top

---

## 前置准备

### 本地环境准备
1. **确认文件位置**：
   - 网站文件：`/Users/qiuhe/Desktop/博客/index.html`
   - 资源文件：`/Users/qiuhe/Desktop/博客/logo.JPG`
   - 图标文件：`/Users/qiuhe/Desktop/博客/favicon.ico`、`favicon.jpg`

2. **检查SSH连接**：
   ```bash
   ssh root@115.190.238.160
   ```
   输入密码：Qiuhe123

3. **确认文件完整性**：
   ```bash
   ls -la /Users/qiuhe/Desktop/博客/
   ```
   确保以下文件存在：
   - index.html
   - logo.JPG
   - favicon.ico
   - favicon.jpg

---

## 部署步骤

### 步骤1：连接服务器

```bash
ssh root@115.190.238.160
```

输入密码：`Qiuhe123`

连接成功后会看到：
```
Welcome to Ubuntu 24.04 LTS (GNU/Linux 6.8.0-55-generic x86_64)
root@iv-7kwh2yqcinp7:~#
```

### 步骤2：安装Nginx和必要工具

```bash
apt update && apt install nginx curl certbot python3-certbot-nginx -y
```

**说明**：
- `apt update`：更新软件包列表
- `nginx`：Web服务器
- `curl`：HTTP客户端工具
- `certbot`：SSL证书申请工具
- `python3-certbot-nginx`：Certbot的Nginx插件

**预期输出**：
```
Hit:1 http://mirrors.ivolces.com/ubuntu noble InRelease
...
Reading package lists... Done
Building dependency tree... Done
...
0 upgraded, 0 newly installed, 0 to remove and 0 not upgraded.
```

### 步骤3：创建网站目录

```bash
mkdir -p /var/www/qiuheagent.top
```

**说明**：
- `-p` 参数：如果父目录不存在则自动创建
- 目录路径：/var/www/qiuheagent.top

**验证目录创建**：
```bash
ls -la /var/www/
```

### 步骤4：上传文件

#### 方法1：使用SCP逐个上传

```bash
# 上传主页文件
scp /Users/qiuhe/Desktop/博客/index.html root@115.190.238.160:/var/www/qiuheagent.top/

# 上传Logo文件
scp /Users/qiuhe/Desktop/博客/logo.JPG root@115.190.238.160:/var/www/qiuheagent.top/

# 上传图标文件
scp /Users/qiuhe/Desktop/博客/favicon.ico root@115.190.238.160:/var/www/qiuheagent.top/
scp /Users/qiuhe/Desktop/博客/favicon.jpg root@115.190.238.160:/var/www/qiuheagent.top/
```

#### 方法2：使用rsync批量上传（推荐）

```bash
rsync -avz --exclude='简历' --exclude='*.md' /Users/qiuhe/Desktop/博客/ root@115.190.238.160:/var/www/qiuheagent.top/
```

**参数说明**：
- `-a`：归档模式，保留文件属性
- `-v`：显示详细信息
- `-z`：压缩传输
- `--exclude='简历'`：排除简历文件夹
- `--exclude='*.md'`：排除所有md文件

**验证文件上传**：
```bash
ssh root@115.190.238.160 "ls -la /var/www/qiuheagent.top/"
```

### 步骤5：配置Nginx

#### 创建配置文件

```bash
nano /etc/nginx/sites-available/qiuheagent.top
```

#### 配置内容

```nginx
server {
    listen 80;
    server_name qiuheagent.top www.qiuheagent.top;
    root /var/www/qiuheagent.top;
    index index.html index.htm;

    # Gzip压缩
    gzip on;
    gzip_vary on;
    gzip_min_length 1024;
    gzip_types text/plain text/css text/xml text/javascript application/x-javascript application/xml+rss application/javascript application/json;

    # 安全头
    add_header X-Frame-Options "SAMEORIGIN" always;
    add_header X-Content-Type-Options "nosniff" always;
    add_header X-XSS-Protection "1; mode=block" always;
    add_header Referrer-Policy "strict-origin-when-cross-origin" always;

    # 静态资源缓存
    location ~* \.(jpg|jpeg|png|gif|ico|svg|webp)$ {
        expires 30d;
        add_header Cache-Control "public, immutable";
    }

    location ~* \.(css|js)$ {
        expires 7d;
        add_header Cache-Control "public, immutable";
    }

    location / {
        try_files $uri $uri/ =404;
    }

    # 禁止访问隐藏文件
    location ~ /\. {
        deny all;
        access_log off;
        log_not_found off;
    }
}
```

**配置说明**：
- `listen 80`：监听80端口（HTTP）
- `server_name`：指定域名
- `root`：网站根目录
- `index`：默认首页文件
- `gzip`：启用压缩，减少传输数据量
- `add_header`：添加安全响应头
- `location ~* \.(jpg|jpeg|png|gif|ico|svg|webp)$`：图片缓存30天
- `location ~* \.(css|js)$`：CSS/JS缓存7天
- `location ~ /\.`：禁止访问隐藏文件

保存文件：`Ctrl+O`，然后`Enter`，最后`Ctrl+X`退出

### 步骤6：启用配置

```bash
# 创建符号链接
ln -s /etc/nginx/sites-available/qiuheagent.top /etc/nginx/sites-enabled/

# 删除默认配置
rm -f /etc/nginx/sites-enabled/default

# 测试配置
nginx -t

# 重载Nginx
systemctl reload nginx
```

**预期输出**：
```
nginx: configuration file /etc/nginx/nginx.conf syntax is ok
nginx: configuration file /etc/nginx/nginx.conf test is successful
```

### 步骤7：测试HTTP访问

```bash
curl -I http://115.190.238.160
```

**预期输出**：
```
HTTP/1.1 200 OK
Server: nginx/1.24.0 (Ubuntu)
Content-Type: text/html
...
```

---

## 域名解析配置

### 在火山引擎控制台配置

#### 步骤1：登录火山引擎控制台
1. 访问：https://console.volcengine.com/
2. 登录您的账号
3. 搜索"DNS"或"域名服务"

#### 步骤2：选择域名
在域名列表中找到 `qiuheagent.top`，点击进入解析设置页面

#### 步骤3：添加解析记录

##### 记录1：主域名解析
- **主机记录**：`@`（或留空）
- **记录类型**：`A`
- **记录值**：`115.190.238.160`
- **TTL**：`600`（秒）
- **线路**：`默认`或`全网默认`

##### 记录2：www子域名解析
- **主机记录**：`www`
- **记录类型**：`A`
- **记录值**：`115.190.238.160`
- **TTL**：`600`（秒）
- **线路**：`默认`或`全网默认`

#### 步骤4：保存配置
点击"确定"或"保存"按钮

### 验证域名解析

#### 本地验证
```bash
# 查询主域名
nslookup qiuheagent.top

# 查询www子域名
nslookup www.qiuheagent.top

# 使用dig查询
dig qiuheagent.top +short
```

**预期输出**：
```
Name:   qiuheagent.top
Address: 115.190.238.160
```

#### 在线验证
访问：https://tool.chinaz.com/dns/
输入域名：`qiuheagent.top`

#### 服务器端验证
```bash
ssh root@115.190.238.160
nslookup qiuheagent.top
```

### DNS生效时间
- **最快**：10分钟
- **平均**：30分钟
- **最慢**：24小时

**建议**：配置后等待30分钟再进行后续操作

---

## SSL证书安装

### 前提条件
- 域名解析已生效
- 80端口可访问
- Nginx配置正确

### 安装SSL证书

#### 方法1：自动安装（推荐）

```bash
ssh root@115.190.238.160
certbot --nginx -d qiuheagent.top -d www.qiuheagent.top --non-interactive --agree-tos --email qiu_he@foxmail.com
```

**参数说明**：
- `--nginx`：使用Nginx插件
- `-d`：指定域名（可多次使用）
- `--non-interactive`：非交互模式
- `--agree-tos`：同意服务条款
- `--email`：指定邮箱地址

**预期输出**：
```
Successfully received certificate.
Certificate is saved at: /etc/letsencrypt/live/qiuheagent.top/fullchain.pem
Key is saved at:         /etc/letsencrypt/live/qiuheagent.top/privkey.pem
This certificate expires on 2026-06-07.
...
Congratulations! You have successfully enabled HTTPS on https://qiuheagent.top
```

#### 方法2：交互式安装

```bash
ssh root@115.190.238.160
certbot --nginx
```

按提示操作：
1. 输入邮箱地址
2. 同意服务条款
3. 选择域名
4. 选择是否重定向HTTP到HTTPS

### 配置自动续期

```bash
echo "0 0 * * * certbot renew --quiet --post-hook 'systemctl reload nginx'" | crontab -
```

**说明**：
- `0 0 * * *`：每天凌晨0点执行
- `certbot renew`：续期证书
- `--quiet`：静默模式
- `--post-hook`：续期后执行命令
- `systemctl reload nginx`：重载Nginx配置

### 验证SSL证书

```bash
# 查看证书信息
certbot certificates

# 查看证书文件
ls -la /etc/letsencrypt/live/qiuheagent.top/

# 测试HTTPS访问
curl -I https://qiuheagent.top
```

**预期输出**：
```
HTTP/1.1 200 OK
Server: nginx/1.24.0 (Ubuntu)
...
```

### 证书信息
- **证书颁发机构**：Let's Encrypt
- **证书类型**：DV（域名验证）
- **有效期**：90天
- **自动续期**：已配置
- **到期时间**：2026-06-07

---

## 测试验证

### 测试HTTP访问

```bash
curl -I http://qiuheagent.top
```

**预期结果**：
```
HTTP/1.1 301 Moved Permanently
Location: https://qiuheagent.top/
```

### 测试HTTPS访问

```bash
curl -I https://qiuheagent.top
```

**预期结果**：
```
HTTP/1.1 200 OK
Server: nginx/1.24.0 (Ubuntu)
Content-Type: text/html
...
```

### 测试网站内容

```bash
curl https://qiuheagent.top | head -20
```

**预期结果**：
```html
<!DOCTYPE html>
<html lang="zh-CN" class="scroll-smooth">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>丘壑 SuperAgent</title>
...
```

### 测试静态资源

```bash
# 测试Logo
curl -I https://qiuheagent.top/logo.JPG

# 测试Favicon
curl -I https://qiuheagent.top/favicon.ico
```

**预期结果**：
```
HTTP/1.1 200 OK
Content-Type: image/jpeg
Cache-Control: public, immutable
Expires: ...
```

### 浏览器测试
1. 打开浏览器
2. 访问：`https://qiuheagent.top`
3. 检查：
   - 页面正常显示
   - 地址栏显示锁图标
   - 证书有效
   - 所有资源加载正常

---

## 常见问题解决

### 问题1：域名解析不生效

**症状**：
```
nslookup qiuheagent.top
*** Can't find qiuheagent.top: No answer
```

**解决方案**：
1. 检查DNS记录配置是否正确
2. 等待更长时间（最长24小时）
3. 清除本地DNS缓存：
   ```bash
   # macOS
   sudo dscacheutil -flushcache; sudo killall -HUP mDNSResponder
   
   # Windows
   ipconfig /flushdns
   
   # Linux
   sudo systemctl restart nscd
   ```
4. 使用在线工具验证：https://tool.chinaz.com/dns/

### 问题2：SSL证书申请失败

**症状**：
```
Certbot failed to authenticate some domains
DNS problem: NXDOMAIN looking up A for qiuheagent.top
```

**解决方案**：
1. 确认域名解析已生效
2. 检查80端口是否开放：
   ```bash
   ufw status
   ```
3. 检查Nginx配置：
   ```bash
   nginx -t
   ```
4. 查看详细日志：
   ```bash
   cat /var/log/letsencrypt/letsencrypt.log
   ```

### 问题3：网站无法访问

**症状**：
```
curl: (7) Failed to connect to 115.190.238.160 port 80
```

**解决方案**：
1. 检查Nginx状态：
   ```bash
   systemctl status nginx
   ```
2. 重启Nginx：
   ```bash
   systemctl restart nginx
   ```
3. 检查防火墙：
   ```bash
   ufw status
   ufw allow 80/tcp
   ufw allow 443/tcp
   ```

### 问题4：文件上传失败

**症状**：
```
scp: /var/www/qiuheagent.top/: Permission denied
```

**解决方案**：
1. 检查目录权限：
   ```bash
   ssh root@115.190.238.160 "ls -la /var/www/"
   ```
2. 修改目录权限：
   ```bash
   ssh root@115.190.238.160 "chown -R www-data:www-data /var/www/qiuheagent.top"
   ```
3. 重新上传文件

### 问题5：SSL证书过期

**症状**：
```
SSL certificate has expired
```

**解决方案**：
1. 手动续期：
   ```bash
   ssh root@115.190.238.160
   certbot renew
   ```
2. 检查自动续期配置：
   ```bash
   crontab -l
   ```
3. 重载Nginx：
   ```bash
   systemctl reload nginx
   ```

---

## 维护建议

### 日常维护

#### 1. 定期检查网站状态
```bash
# 检查Nginx状态
systemctl status nginx

# 检查SSL证书
certbot certificates

# 检查磁盘空间
df -h
```

#### 2. 查看访问日志
```bash
# 访问日志
tail -f /var/log/nginx/access.log

# 错误日志
tail -f /var/log/nginx/error.log
```

#### 3. 定期更新系统
```bash
# 更新软件包
apt update && apt upgrade -y

# 清理无用包
apt autoremove -y
```

### 备份策略

#### 1. 备份网站文件
```bash
# 本地备份
rsync -avz root@115.190.238.160:/var/www/qiuheagent.top/ /Users/qiuhe/Desktop/博客/backup/

# 服务器端备份
ssh root@115.190.238.160 "tar -czf /var/www/qiuheagent.top_backup_$(date +%Y%m%d).tar.gz /var/www/qiuheagent.top/"
```

#### 2. 备份SSL证书
```bash
# 备份证书目录
ssh root@115.190.238.160 "tar -czf /etc/letsencrypt_backup_$(date +%Y%m%d).tar.gz /etc/letsencrypt/"
```

#### 3. 备份Nginx配置
```bash
# 备份配置文件
ssh root@115.190.238.160 "tar -czf /etc/nginx_backup_$(date +%Y%m%d).tar.gz /etc/nginx/"
```

### 性能优化

#### 1. 启用HTTP/2
在Nginx配置中添加：
```nginx
server {
    listen 443 ssl http2;
    ...
}
```

#### 2. 优化图片
- 使用WebP格式
- 压缩图片大小
- 添加响应式图片

#### 3. 启用CDN
- 将静态资源上传到CDN
- 配置CDN加速

### 安全加固

#### 1. 配置防火墙
```bash
# 允许SSH
ufw allow 22/tcp

# 允许HTTP
ufw allow 80/tcp

# 允许HTTPS
ufw allow 443/tcp

# 启用防火墙
ufw enable

# 查看状态
ufw status
```

#### 2. 禁用root SSH登录
```bash
# 编辑SSH配置
nano /etc/ssh/sshd_config

# 修改以下行
PermitRootLogin no

# 重启SSH服务
systemctl restart sshd
```

#### 3. 定期安全更新
```bash
# 安装安全更新
apt install unattended-upgrades -y

# 配置自动更新
dpkg-reconfigure -plow unattended-upgrades
```

### 监控告警

#### 1. 设置磁盘空间监控
```bash
# 创建监控脚本
cat > /root/check_disk.sh << 'EOF'
#!/bin/bash
DISK_USAGE=$(df / | tail -1 | awk '{print $5}' | sed 's/%//')
if [ $DISK_USAGE -gt 80 ]; then
    echo "磁盘使用率超过80%: $DISK_USAGE%" | mail -s "磁盘告警" qiu_he@foxmail.com
fi
EOF

chmod +x /root/check_disk.sh

# 添加到定时任务
echo "0 */6 * * * /root/check_disk.sh" | crontab -
```

#### 2. 设置网站可用性监控
```bash
# 创建监控脚本
cat > /root/check_website.sh << 'EOF'
#!/bin/bash
if ! curl -f -s https://qiuheagent.top > /dev/null; then
    echo "网站不可访问" | mail -s "网站告警" qiu_he@foxmail.com
fi
EOF

chmod +x /root/check_website.sh

# 添加到定时任务
echo "*/5 * * * * /root/check_website.sh" | crontab -
```

---

## 快速参考

### 常用命令

#### 服务器管理
```bash
# 连接服务器
ssh root@115.190.238.160

# 重启Nginx
systemctl restart nginx

# 重载Nginx配置
systemctl reload nginx

# 查看Nginx状态
systemctl status nginx

# 查看Nginx配置
nginx -t
```

#### 文件管理
```bash
# 上传文件
scp /path/to/file root@115.190.238.160:/var/www/qiuheagent.top/

# 批量上传
rsync -avz /local/path/ root@115.190.238.160:/remote/path/

# 查看远程文件
ssh root@115.190.238.160 "ls -la /var/www/qiuheagent.top/"
```

#### SSL证书管理
```bash
# 申请证书
certbot --nginx -d qiuheagent.top

# 续期证书
certbot renew

# 查看证书
certbot certificates

# 撤销证书
certbot revoke --cert-path /etc/letsencrypt/live/qiuheagent.top/cert.pem
```

#### 日志查看
```bash
# Nginx访问日志
tail -f /var/log/nginx/access.log

# Nginx错误日志
tail -f /var/log/nginx/error.log

# SSL证书日志
tail -f /var/log/letsencrypt/letsencrypt.log

# 系统日志
journalctl -u nginx -f
```

### 重要文件路径

#### 网站文件
- 网站根目录：`/var/www/qiuheagent.top`
- 主页文件：`/var/www/qiuheagent.top/index.html`
- Logo文件：`/var/www/qiuheagent.top/logo.JPG`
- 图标文件：`/var/www/qiuheagent.top/favicon.ico`

#### Nginx配置
- 主配置文件：`/etc/nginx/nginx.conf`
- 网站配置：`/etc/nginx/sites-available/qiuheagent.top`
- 启用配置：`/etc/nginx/sites-enabled/qiuheagent.top`

#### SSL证书
- 证书目录：`/etc/letsencrypt/live/qiuheagent.top/`
- 证书文件：`/etc/letsencrypt/live/qiuheagent.top/fullchain.pem`
- 私钥文件：`/etc/letsencrypt/live/qiuheagent.top/privkey.pem`

#### 日志文件
- Nginx访问日志：`/var/log/nginx/access.log`
- Nginx错误日志：`/var/log/nginx/error.log`
- SSL证书日志：`/var/log/letsencrypt/letsencrypt.log`

---

## 总结

### 部署清单
- [ ] 服务器连接正常
- [ ] Nginx安装完成
- [ ] 网站目录创建完成
- [ ] 文件上传完成
- [ ] Nginx配置完成
- [ ] 域名解析配置完成
- [ ] 域名解析生效
- [ ] SSL证书安装完成
- [ ] HTTPS访问正常
- [ ] 自动续期配置完成
- [ ] 备份策略配置完成

### 访问地址
- **HTTP**：http://qiuheagent.top
- **HTTPS**：https://qiuheagent.top
- **IP访问**：http://115.190.238.160

### 技术支持
- **Let's Encrypt**：https://letsencrypt.org/
- **Nginx文档**：https://nginx.org/en/docs/
- **Certbot文档**：https://certbot.eff.org/docs/

---

**文档版本**：1.0  
**最后更新**：2026-03-09  
**维护者**：丘壑
