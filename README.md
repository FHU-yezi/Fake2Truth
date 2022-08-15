# Fake2Truth

向光而行。

# 部署

推荐使用 Docker Compose 部署。

您需要启动一个 MongoDB 服务，运行在 `27017` 端口上，同时将其加入名为 `mongodb` 的 Docker 网络。

克隆项目存储库：

```bash
git clone https://github.com/FHU-yezi/Fake2Truth.git
```

进入目录：

```bash
cd Fake2Truth
```

启动服务：
```
docker compose up -d
```

服务默认在 `8604` 端口启动，如需更改，请编辑 `config.yaml` 文件。