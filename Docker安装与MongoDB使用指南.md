# Docker 安装与 MongoDB 使用指南 (Windows)

## 一、安装 Docker Desktop

### 1. 前提条件

Docker Desktop for Windows 需要：
- **Windows 11**（你已满足）
- **开启虚拟化**（大部分电脑默认已开启）

检查虚拟化是否开启：
1. 按 `Ctrl + Shift + Esc` 打开任务管理器
2. 切换到"性能"标签 → "CPU"
3. 查看右下角"虚拟化"是否显示"已启用"

如果未启用，需要进 BIOS 开启（重启电脑按 F2/DEL 进 BIOS，找 Intel VT-x 或 AMD-V 选项）。

### 2. 下载安装

1. 访问官网：https://www.docker.com/products/docker-desktop/
2. 点击 "Download for Windows" 下载安装包
3. 双击运行安装程序
4. 安装时勾选 **"Use WSL 2 instead of Hyper-V"**（推荐）
5. 安装完成后重启电脑

### 3. 首次启动

1. 从桌面或开始菜单启动 Docker Desktop
2. 等待左下角显示绿色 **"Engine running"** 表示启动成功
3. 可能会要求登录 Docker Hub，可以跳过（点右上角 X）

### 4. 验证安装

打开终端（PowerShell 或 Git Bash），运行：

```bash
docker --version
```

应该看到类似输出：
```
Docker version 27.x.x, build xxxxxxx
```

运行测试容器：
```bash
docker run hello-world
```

看到 "Hello from Docker!" 表示安装成功。

---

## 二、用 Docker 启动 MongoDB

### 1. 拉取 MongoDB 镜像

```bash
docker pull mongo
```

这会下载最新的 MongoDB 官方镜像（约 500MB）。

### 2. 启动 MongoDB 容器

```bash
docker run -d -p 27017:27017 --name mongodb mongo
```

参数说明：
| 参数 | 含义 |
|------|------|
| `-d` | 后台运行（detached） |
| `-p 27017:27017` | 把容器的 27017 端口映射到本机的 27017 |
| `--name mongodb` | 给容器起个名字叫 "mongodb" |
| `mongo` | 使用的镜像名称 |

### 3. 验证运行状态

```bash
docker ps
```

应该看到 `mongodb` 容器，状态为 `Up`。

---

## 三、常用 Docker 命令

### 容器管理

```bash
# 查看运行中的容器
docker ps

# 查看所有容器（包括已停止的）
docker ps -a

# 停止 MongoDB
docker stop mongodb

# 启动已停止的 MongoDB
docker start mongodb

# 重启 MongoDB
docker restart mongodb

# 删除容器（需先停止）
docker stop mongodb
docker rm mongodb
```

### 查看日志

```bash
# 查看 MongoDB 日志
docker logs mongodb

# 实时跟踪日志
docker logs -f mongodb
```

### 进入容器内部

```bash
# 进入 MongoDB 的 shell
docker exec -it mongodb mongosh
```

进入后可以执行 MongoDB 命令：
```javascript
// 查看所有数据库
show dbs

// 切换到 ultraflow 数据库
use ultraflow

// 查看当前数据库的集合
show collections

// 查询 users 集合的数据
db.users.find()

// 退出
exit
```

---

## 四、配合你的后端项目使用

### 1. 启动 MongoDB

```bash
docker start mongodb
```

### 2. 启动后端

```bash
cd d:/极律/fontend/backend
uvicorn main:app --reload --port 8001
```

### 3. 验证连接

访问 http://localhost:8001/docs 查看 API 文档，能正常加载说明数据库已连接。

### 4. 停止服务

```bash
# 停止后端：在终端按 Ctrl + C

# 停止 MongoDB（可选，不占资源）
docker stop mongodb
```

---

## 五、数据持久化（可选但推荐）

默认情况下，删除容器数据会丢失。用 `-v` 挂载卷可以持久化数据：

```bash
# 先删除旧容器
docker stop mongodb
docker rm mongodb

# 用数据卷重新创建
docker run -d -p 27017:27017 -v mongo-data:/data/db --name mongodb mongo
```

这样即使删除容器，数据仍然保存在 `mongo-data` 卷中。

---

## 六、常见问题

### Q: docker 命令提示权限不足？
用管理员身份运行 PowerShell。

### Q: 端口 27017 被占用？
查看谁在占用：
```bash
netstat -ano | findstr 27017
```
停掉占用进程，或改映射端口：
```bash
docker run -d -p 27018:27017 --name mongodb mongo
```
然后修改 `.env` 中的 `MONGODB_URL=mongodb://localhost:27018`。

### Q: Docker Desktop 启动很慢？
首次启动需要初始化 WSL 2，耐心等待 1-2 分钟。后续启动会快很多。

### Q: 下载镜像很慢？
配置国内镜像加速：
1. 打开 Docker Desktop → Settings（齿轮图标）
2. 左侧选 Docker Engine
3. 在 JSON 中添加：
```json
{
  "registry-mirrors": [
    "https://mirror.ccs.tencentyun.com",
    "https://docker.m.daocloud.io"
  ]
}
```
4. 点 Apply & Restart
