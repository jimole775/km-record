@echo off
setlocal

REM Step 1: 定义项目路径和GitHub仓库地址
set PROJECT_PATH=D:\km-record-ui\
set GITHUB_URL=https://github.com/jimole775/km-record-ui.git

REM Step 2: 检查目标文件夹是否存在，如果存在则删除
if exist %PROJECT_PATH% (
  echo 目标文件夹已存在，正在删除...
  rmdir /S /Q %PROJECT_PATH%
)
echo 正在创建UI项目目录...
mkdir %PROJECT_PATH%

REM Step 3: 使用git clone拉取项目
echo 正在克隆UI项目...
git clone %GITHUB_URL% %PROJECT_PATH%

REM Step 4: 进入项目目录
D:
cd %PROJECT_PATH%

REM Step 5: 安装npm依赖

echo 正在安装依赖...
npm i

REM Step 6: 运行项目
echo 依赖安装完成，正在启动项目...
npm run start

pause
