# 项目介绍

这是一个前后端分离的宝宝辅食Web项目。

# 技术栈

### Vue 3

**Vue 3** 是一个用于构建用户界面的渐进式 JavaScript 框架，是 Vue.js 的更新版本，提供了多项改进和新功能。以下是一些关键点：

- **组合式 API**：提供了一种更灵活和可重用的方式来组织组件逻辑。
- **性能提升**：相比 Vue 2，渲染速度更快，内存使用更优化。
- **新组件**：引入了新的内置组件如 Fragments、Teleport 和 Suspense，提供了高级渲染技术。
- **更小的包体积**：通过优化，Vue 运行时的体积更小。
- **TypeScript 支持**：增强了 TypeScript 的集成，使在 Vue 应用中使用 TypeScript 更加方便。
- **基于 Proxy 的响应式系统**：用 ES6 的 Proxy 取代了之前基于 Object.defineProperty 的响应式系统，带来了更好的性能和更多功能。

### Element Plus

**Element Plus** 是一个基于 Vue 3 的组件库，旨在提供一套可定制的 UI 组件，用于构建现代 Web 应用。它是为 Vue 2 构建的 Element UI 的继任者。主要特点包括：

- **全面的组件**：提供丰富的组件如表单、表格、通知和对话框等。
- **可定制的主题**：允许对主题进行广泛的自定义，以匹配应用程序的设计。
- **国际化支持**：内置了对多语言的支持，方便进行国际化开发。
- **易于使用**：简单直观的 API 和详细的文档，使开发过程更加轻松。

### FastAPI

**FastAPI** 是一个用于构建 API 的现代、快速（高性能）Web 框架，基于 Python 3.6+ 类型提示。它的设计目标是让开发者可以快速开发具有高性能和高可维护性的 API。主要特点包括：

- **高性能**：速度与 Node.js 和 Go 相当（基于 Starlette 和 Pydantic）。
- **简单易用**：通过类型提示和自动生成的文档，极大地简化了开发过程。
- **自动生成文档**：支持自动生成交互式 API 文档（OpenAPI 和 JSON Schema）。
- **类型安全**：利用 Python 的类型提示，提供端到端的类型安全。
- **异步支持**：内置对异步编程的支持，可以处理高并发请求。

### SQLite3

**SQLite3** 是一个自给自足的、无服务器的、配置零的、事务性的 SQL 数据库引擎。与传统的客户端-服务器数据库引擎不同，SQLite 嵌入到最终应用程序中，直接读写普通的磁盘文件。主要特点包括：

- **轻量级**：整个数据库引擎被打包成一个小型的库，可以嵌入到各种应用中。
- **无服务器**：不需要独立的服务器进程，数据库文件可以直接在应用中打开和访问。
- **事务性**：支持 ACID 事务，保证数据的完整性和一致性。
- **跨平台**：支持多种操作系统和平台，包括 Windows、Linux、macOS 等。
- **高效**：在嵌入式环境中表现出色，适合移动应用和小型设备使用。

# 功能

==具体功能见演示视频==

- 用户登录
- 个人页面
- 添加食材页面
- 历史页面
  - 修改菜品数据
  - 搜索
  - 收藏显示
  - 删除菜品
  - 点击图片显示食材信息

# How to use

## python

在/fast文件目录下

```
conda create -n web python=3.9
conda activate web
pip install -r requirements.txt
python init.py
python main.py
```

## Vue

在/dish-vue文件目录下

```
npm run serve
```

## 用户密码

用户名：zhangsan

密码：123456

ps:其他用户也设置了 但是是空数据

