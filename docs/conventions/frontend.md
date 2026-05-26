# 前端编码规范与检查清单

> last_updated: 2026-05-26
> status: active

---

## 一、组件规范

### 1.1 语法规范

- [ ] 所有 `.vue` 文件使用 `<script setup lang="ts">`，禁止 Options API
- [ ] 所有组件使用 Composition API（`ref` / `computed` / `watch` / `onMounted`）
- [ ] 页面级组件放在 `src/pages/`，公共组件放在 `src/components/`

### 1.2 模板规范

- [ ] 所有标签使用 uni-app 组件：`<view>` `<text>` `<scroll-view>` `<image>` `<input>` `<picker>` 等
- [ ] 禁止 HTML 标签：`<div>` `<span>` `<img>` `<input type="...">` `<button>`（用 `<view>` 替代 `<button>`）
- [ ] 禁止写法：`<button open-type="...">`，用 uni-app 的 `<button>` 组件

### 1.3 样式规范

- [ ] 强制 UnoCSS 原子化类名，**禁止 `<style>` 块和 `<style scoped>` 块**
- [ ] 禁止内联样式 `style="..."`（`rpx` 动态计算的除外）
- [ ] 使用 `rpx` 单位：`px-32rpx` `text-28rpx` `rounded-20rpx`
- [ ] 颜色使用 UnoCSS 类名或方括号语法：`text-[#1E293B]` `bg-[#F8FAFC]`

**正确示例：**

```vue
<template>
  <view class="flex h-screen flex-col bg-[#F8FAFC]">
    <view class="bg-[#1E293B] px-32rpx pb-24rpx pt-80rpx">
      <text class="text-32rpx font-bold text-white">标题</text>
    </view>
    <view class="flex-1 p-24rpx">
      <text class="text-28rpx leading-[1.6] text-[#0EA5E9]">内容</text>
    </view>
  </view>
</template>
```

**错误示例（禁止）：**

```vue
<!-- ❌ 使用了 div 和 style -->
<template>
  <div style="display: flex; background: #f8fafc;">
    <span class="title">标题</span>
  </div>
</template>
<style scoped>
.title { font-size: 28rpx; }
</style>
```

---

## 二、状态管理

### 2.1 Pinia Store 规范

- [ ] 所有 store 使用 `defineStore` with Options API 风格（与现有一致）
- [ ] 所有 store 必须 `persist: true`
- [ ] 异步操作在 `actions` 中通过 `async/await` 实现
- [ ] Store 文件放在 `src/store/modules/` 下，每个模块一个目录

### 2.2 类型定义

- [ ] Store 的 state/返回类型定义在 `types.ts` 中
- [ ] API 请求/响应类型定义在 `src/api/types/` 或 `store/modules/xxx/types.ts`
- [ ] 禁止使用 `any`，用具体类型或 `unknown`

### 2.3 Store 结构示例

```
src/store/modules/ai/
├── index.ts          # defineStore 定义
└── types.ts          # AIState, AIMessage, ExtractedHabit
```

---

## 三、API 请求层

### 3.1 规范

- [ ] 所有请求通过 `src/api/` 下的模块发起，不直接在页面中调 `uni.request`
- [ ] 使用统一的请求拦截器（`src/api/interceptors/`）
- [ ] 响应解包适配 `ApiResponse<T>` 格式：取 `res.data` 而非裸 `res`

### 3.2 API 模块结构

```
src/api/
├── index.ts          # apiClient 实例
├── modules/
│   ├── user.ts       # 认证、用户信息
│   ├── habit.ts      # 习惯 CRUD
│   ├── checkin.ts    # 打卡
│   ├── ai.ts         # AI 对话
│   └── common.ts     # 文件上传
└── types/
    └── common.ts     # ApiResponse<T>
```

### 3.3 API 调用规范

```typescript
// ✅ 正确：通过 api 模块
import { AIApi } from '@/api';
const res = await AIApi.sendMessage({ message: content });

// ❌ 错误：直接调 uni.request
uni.request({ url: '...', method: 'POST', data: {...} });
```

---

## 四、路由和页面

### 4.1 页面配置

- [ ] 所有页面在 `src/pages.json` 中注册
- [ ] 需要登录的页面添加 `"needLogin": true`
- [ ] Tab 页面不设置 `needLogin`（Tab 页通过 router interceptor 处理）

### 4.2 页面交互规范

- [ ] Loading 状态：至少显示一个简单的加载状态（如 typing indicator），禁止完全空白
- [ ] Empty 状态：列表为空时显示引导文案（如"还没有习惯，去跟教练聊聊吧"）
- [ ] Error 状态：使用 `uni.showToast({ title: '...', icon: 'none' })` 提示
- [ ] 成功反馈：关键操作（打卡、创建习惯）使用 `uni.showToast` + `uni.vibrateShort`
- [ ] 乐观更新：切换人设、开关提醒等操作先更新 UI 再调 API，失败后回滚

---

## 五、禁止事项

- [ ] 禁止 `console.log`（用结构化日志或移除）
- [ ] 禁止删除已有代码的 `TODO` 标记（表示已知待做项）
- [ ] 禁止引入新依赖（npm/pip）除非任务明确要求
- [ ] 禁止修改 `.gitignore` / `.env` 文件
- [ ] 禁止在 `localStorage` / `uni.storage` 中存敏感信息（token 除外）
- [ ] 禁止生成无用的文档（README、CHANGELOG）除非用户明确要求
