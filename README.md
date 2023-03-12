# Featherblog
一个集成了chatGPT-api等实用小工具的个人博客（开发中）

## 介绍
一个基于Flask开发的简单的博客系统，集成了多种实用工具
* 支持markdown编辑、显示的博客文章与评论系统
* 能够存储用户历史消息、显示Tex公式的ChatGPT聊天页面
* 在线聊天室（待开发）

部署实例演示：<http://www.featherwriting.blog>

## 使用组件
### 前端
* Bootstrap 4.0 及其前端模板 Boomerang UI Kit
* Markdown编辑器 SimpleMDE
* Tex公式编译器 MathJax
### 后端
* SQLite及SQLalchemy
* OpenAI库
* Flask框架及其扩展

## 安装
git到本地并运行__init__.py即可使用，在服务器部署可以配合mod_wsgi与Apache使用

注意：若要使用chatgpt功能，请在chat.py中填写自己的api_key与organization（见openai官网）
