# 博客部署指南

## 部署到火山引擎Ubuntu服务器

### 1. 连接服务器
```bash
ssh root@115.190.238.160
```

### 2. 安装Nginx和必要工具
```bash
apt update && apt install nginx curl certbot python3-certbot-nginx -y
```

### 3. 创建网站目录
```bash
mkdir -p /var/www/qiuheagent.top
```

### 4. 上传文件
```bash
scp /Users/qiuhe/Desktop/博客/index.html root@115.190.238.160:/var/www/qiuheagent.top/
scp /Users/qiuhe/Desktop/博客/logo.JPG root@115.190.238.160:/var/www/qiuheagent.top/
scp /Users/qiuhe/Desktop/博客/favicon.ico root@115.190.238.160:/var/www/qiuheagent.top/
scp /Users/qiuhe/Desktop/博客/favicon.jpg root@115.190.238.160:/var/www/qiuheagent.top/
```

或者使用rsync一次性上传所有文件:
```bash
rsync -avz --exclude='简历' --exclude='*.md' /Users/qiuhe/Desktop/博客/ root@115.190.238.160:/var/www/qiuheagent.top/
```

### 5. 配置Nginx
```bash
nano /etc/nginx/sites-available/qiuheagent.top
```

添加以下内容:
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

### 6. 启用配置
```bash
ln -s /etc/nginx/sites-available/qiuheagent.top /etc/nginx/sites-enabled/
rm -f /etc/nginx/sites-enabled/default
nginx -t && systemctl reload nginx
```

### 7. 配置域名解析
在域名管理控制台添加A记录:
- 主机记录: @, 记录值: 115.190.238.160
- 主机记录: www, 记录值: 115.190.238.160

### 8. 安装SSL证书
```bash
certbot --nginx -d qiuheagent.top -d www.qiuheagent.top
```

### 9. 配置自动续期
```bash
echo "0 0 * * * certbot renew --quiet --post-hook 'systemctl reload nginx'" | crontab -
```

### 10. 测试访问
访问: https://qiuheagent.top

---

## 性能优化建议

### 1. 启用HTTP/2
在Nginx配置的server块中添加:
```nginx
listen 443 ssl http2;
```

### 2. 优化图片
- 使用WebP格式替代JPEG/PNG
- 压缩图片文件大小
- 添加响应式图片

### 3. CDN加速
- 将静态资源(CSS、JS、图片)上传到CDN
- 使用CDN加速外部资源加载

### 4. 预加载关键资源
在index.html的<head>中添加:
```html
<link rel="preload" href="logo.JPG" as="image">
```

---

## 安全加固建议

### 1. 配置防火墙
```bash
ufw allow 22/tcp
ufw allow 80/tcp
ufw allow 443/tcp
ufw enable
```

### 2. 禁用root SSH登录
```bash
nano /etc/ssh/sshd_config
# 修改: PermitRootLogin no
systemctl restart sshd
```

### 3. 定期更新系统
```bash
apt update && apt upgrade -y
```

---

## 自动化部署脚本

创建deploy.sh脚本:
```bash
#!/bin/bash
SERVER_IP="115.190.238.160"
REMOTE_DIR="/var/www/qiuheagent.top"

echo "开始部署..."
rsync -avz --exclude='简历' --exclude='*.md' /Users/qiuhe/Desktop/博客/ root@$SERVER_IP:$REMOTE_DIR/
echo "部署完成!"
```

使用方法:
```bash
chmod +x deploy.sh
./deploy.sh
```

---

## 监控和日志

### 查看Nginx访问日志
```bash
tail -f /var/log/nginx/access.log
```

### 查看Nginx错误日志
```bash
tail -f /var/log/nginx/error.log
```
