# 论文选题系统

基于 Django 开发的论文选题管理系统，支持教师发布论文题目、学生选题申请、教师审批、管理员用户管理等功能。

## 快速启动（Docker）

```bash
cd label-00308

# 启动所有服务（数据库 + 后端）
docker-compose up -d --build

# 查看日志
docker-compose logs -f backend
```

等待启动完成后访问：http://localhost:8000/

## 本地开发

### 1. 启动 MySQL 数据库（Docker）

```bash
cd label-00308
docker-compose up -d db
```

等待 MySQL 启动完成（约10秒）。

### 2. 启动 Django 后端（本地）

```bash
cd backend

# 安装依赖
pip install -r requirements.txt

# 执行数据库迁移
python manage.py migrate

# 初始化测试数据
python manage.py init_data

# 启动开发服务器
python manage.py runserver 8081
```

## 题目

请使用Python Web开发基础教程Django版|微课版这本书的内容，运用该课本知识，使用pycharm制作一个选择论文题目系统的Web网页，要求：最少要有四个界面，包括登录界面，每个老师发布的论文题目介绍界面，选择老师论文题目的界面，老师同意学生选择的界面，要能使用数据库，连接数据库

## 测试账号

| 角色   | 用户名   | 密码     |
| ------ | -------- | -------- |
| 管理员 | admin    | admin123 |
| 教师   | teacher1 | 123456   |
| 教师   | teacher2 | 123456   |
| 教师   | teacher3 | 123456   |
| 学生   | student1 | 123456   |
| 学生   | student2 | 123456   |
| 学生   | student3 | 123456   |

## 功能模块

### 学生功能

- 浏览论文题目列表
- 查看题目详情
- 申请选题
- 查看我的申请记录
- 取消待审批的申请

### 教师功能

- 发布/编辑/删除论文题目
- 查看学生选题申请
- 通过/拒绝学生申请

### 管理员功能

- 系统数据统计面板
- 用户管理（添加/编辑/删除教师和学生）

## 技术栈

- **后端框架**: Django 4.2
- **数据库**: MySQL 8.0
- **前端**: Django Templates + CSS
- **部署**: Docker + Gunicorn

## 项目结构

```
label-00308/
├── backend/
│   ├── accounts/          # 用户认证与管理员模块
│   ├── topics/            # 论文题目模块
│   ├── selections/        # 选题管理模块
│   ├── templates/         # HTML 模板
│   ├── thesis_selection/  # Django 项目配置
│   ├── manage.py
│   ├── requirements.txt
│   ├── Dockerfile
│   └── entrypoint.sh
├── docker-compose.yml
├── .prettierignore
└── README.md
```

## 访问地址

| 环境        | 地址                   |
| ----------- | ---------------------- |
| Docker 部署 | http://localhost:8000/ |
| 本地开发    | http://localhost:8081/ |
