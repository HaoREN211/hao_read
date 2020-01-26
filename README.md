# hao_read

### 使用pipreqs导出工程依赖的包
```commandline
pipreqs ./ --encoding=utf8 --force
```

### 创建虚拟环境并指定PYTHON版本
```commandline
virtualenv venv --python=python3.7
```

### 进入虚拟环境
```commandline
source venv/bin/activate
```

### 退出虚拟环境
```commandline
deactivate
```

### MySQL创建UTF8数据库
```sql
CREATE DATABASE IF NOT EXISTS hao_read DEFAULT CHARSET utf8 COLLATE utf8_general_ci;
```