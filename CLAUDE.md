# 极律 (UltraFlow) — 项目导航

AI 习惯养成教练。FastAPI 后端 + uni-app (Vue 3) 微信小程序前端，DeepSeek API 驱动 AI 对话。

## 快速导航

| 你想做什么 | 去哪里看 |
|-----------|---------|
| 了解产品功能和交互 | `docs/prd/ultraflow-prd.md` |
| 了解后端编码规范和检查清单 | `docs/conventions/backend.md` |
| 了解前端编码规范和检查清单 | `docs/conventions/frontend.md` |
| 了解 AI Prompt 和对话流程 | `backend/app/services/ai.py` |
| 了解数据库模型和索引 | `backend/app/core/database.py` |
| 了解 API 接口定义 | `backend/app/api/` 目录下各文件 |
| 了解前端状态管理 | `uniapp-vue3-template/src/store/modules/` |
| 了解前端页面实现 | `uniapp-vue3-template/src/pages/` |

## 项目结构

```
backend/                          # FastAPI Python 后端
├── main.py                       # 入口：CORS、路由注册、静态文件
├── app/
│   ├── api/                      # API 路由层
│   │   ├── user.py               #   认证、用户信息、人设切换
│   │   ├── habit.py              #   习惯 CRUD、暂停/恢复
│   │   ├── checkin.py            #   打卡、热力图、周统计
│   │   ├── ai.py                 #   AI 对话、习惯确认
│   │   └── common.py             #   文件上传
│   ├── services/ai.py            # AI 核心：Prompt、LLM 调用、输出解析
│   ├── models/                   # Pydantic 模型
│   │   ├── user.py               #   LoginByCodeResponse, UserProfile
│   │   ├── habit.py              #   HabitResponse, CheckInResponse, WeeklyStats
│   │   └── ai.py                 #   ChatResponse, HabitCardData
│   └── core/
│       ├── config.py             #   配置（DeepSeek API、MongoDB URL、JWT Secret）
│       ├── database.py           #   MongoDB 连接和索引
│       └── deps.py               #   依赖注入（get_current_user）
│
uniapp-vue3-template/             # uni-app (Vue 3) 微信小程序前端
├── src/
│   ├── pages/tab/                # 4 个 Tab 页面
│   │   ├── dashboard/            #   今日看板：任务列表、滑动打卡
│   │   ├── chat/                 #   AI 对话：创建习惯、确认卡片
│   │   ├── stats/                #   成长轨迹：热力图、排行榜
│   │   └── coach/                #   教练配置：人设、习惯管理
│   ├── store/modules/            # Pinia 状态管理（全部 persist）
│   │   ├── ai/                   #   AI 对话状态
│   │   ├── habit/                #   习惯列表 + 今日任务
│   │   ├── checkin/              #   打卡记录（含 Mock 数据）
│   │   └── user/                 #   用户认证和偏好
│   ├── api/                      # API 请求层（uni.request 封装）
│   └── pages.json                # 路由和 TabBar 配置
```

## 技术栈速查

| 层 | 技术 |
|----|------|
| 后端框架 | FastAPI (Python 3.13), async/await |
| 数据库 | MongoDB (Motor 异步驱动) |
| AI 模型 | DeepSeek v4-flash (`openai` SDK, response_format: json_object) |
| 前端框架 | Vue 3 + TypeScript, Composition API + `<script setup>` |
| 跨端 | uni-app (Vite 5), 微信小程序 |
| 状态管理 | Pinia + pinia-plugin-persistedstate |
| CSS | UnoCSS 原子化类名 |
| 样式规范 | 禁止 `<style>` 块，禁止 HTML 标签，只用 uni-app 组件 |

## 硬性规则（每次生成代码必须遵守）

1. **后端**：所有 API 接口的 Request/Response 必须使用 Pydantic BaseModel
2. **后端**：所有 API 接口统一返回 `ApiResponse[T]` 格式，禁止裸 dict
3. **后端**：所有数据库/网络操作必须 `async/await`
4. **前端**：所有组件使用 `<script setup>` + Composition API，禁止 Options API
5. **前端**：所有组件使用 UnoCSS 原子化类名，禁止 `<style>` 块
6. **前端**：所有标签使用 uni-app 组件（`<view>` `<text>` `<scroll-view>`），禁止 HTML 标签
7. **前后端分离**：后端不返回 HTML，前端不直接访问数据库
8. **安全**：AI 输出必须经过 `validate_extracted_habit()` 校验，不可直接入库

##  Git 提交规范

**提交必须带有提交类型，并且有详细的说明，禁止提交无意义的 msg**
- feat: 提交新功能，如 feat: 创作中心二期创作学院
- fix: 修复了 bug，如 fix: 【评论】Android--特殊昵称会造成评论被裁 #29358
- docs: 只修改了文档
- style: 调整代码格式，未修改代码逻辑（比如修改空格、格式化、缺少分号等）
- refactor: 代码重构，既没修复 bug 也没有添加新功能
- perf: 性能优化，提高性能的代码更改
- test: 添加或修改代码测试
- chore: 对构建流程或辅助工具和依赖库（如文档生成等）的更改
- typo: 修改输错的单词，语句等

## 补充规则

- 默认写零注释。只在 WHY 不明显的场景写一行。
- 不引入未要求的依赖或抽象。
- 编辑范围仅限任务相关文件，不顺手重构。
- 有疑问先确认，不要自己猜。

> 详细的编码规范和检查清单见 `docs/conventions/backend.md` 和 `docs/conventions/frontend.md`。
