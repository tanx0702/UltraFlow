# 前端编码规范与检查清单

> last_updated: 2026-05-30
> status: active

---

## 一、目录结构

```
src/
├── api/                    # API 层（按领域拆分）
│   ├── index.ts            # 统一导出
│   ├── ai/index.ts + types.ts
│   ├── habit/index.ts + types.ts
│   ├── checkin/index.ts + types.ts
│   ├── user/index.ts + types.ts
│   └── common/index.ts + types.ts
├── components/             # 公共组件（全项目通用）
│   ├── PageHeader/
│   ├── FreqBadge/
│   ├── EmptyState/
│   ├── ProgressRing/
│   ├── SwipeCard/
│   ├── HeatmapGrid/
│   └── Stepper/
├── composables/            # 组合式函数（业务逻辑复用）
│   ├── useAuth.ts
│   └── useDebounce.ts
├── constants/              # 常量定义
│   └── persona.ts
├── models/                 # 领域模型（单一真相源）
│   ├── habit.model.ts      # Habit, DailyTask, FrequencyType
│   ├── ai.model.ts         # ExtractedHabit, ChatMessage
│   ├── checkin.model.ts    # CheckInRecord, WeekDayStatus
│   └── user.model.ts       # CoachPersona, UserProfile
├── pages/
│   ├── tab/
│   │   ├── chat/
│   │   │   ├── index.vue           # 页面壳（< 200 行）
│   │   │   ├── components/         # 页面私有组件
│   │   │   │   ├── MessageBubble.vue
│   │   │   │   ├── HabitConfirmCard.vue
│   │   │   │   ├── EditHabitPopup.vue
│   │   │   │   └── ConflictModal.vue
│   │   │   └── composables/
│   │   │       └── useChat.ts
│   │   ├── dashboard/
│   │   │   ├── index.vue
│   │   │   ├── components/
│   │   │   │   ├── DashboardHeader.vue
│   │   │   │   ├── TaskGroup.vue
│   │   │   │   └── CelebrationBanner.vue
│   │   │   └── composables/
│   │   │       └── useDashboard.ts
│   │   ├── stats/
│   │   │   ├── index.vue
│   │   │   └── composables/useStats.ts
│   │   └── coach/
│   │       └── index.vue
│   └── common/
│       ├── login/
│       ├── habit-detail/
│       └── 404/
├── store/                  # Pinia 状态管理
│   ├── index.ts
│   └── modules/
│       ├── app/
│       ├── user/
│       ├── habit/
│       ├── ai/
│       └── checkin/
└── utils/
    ├── request/            # HTTP 请求封装（单例）
    ├── auth.ts
    ├── common.ts
    └── storage.ts
```

---

## 二、组件规范

### 2.1 语法规范

- [ ] 所有 `.vue` 文件使用 `<script setup lang="ts">`，禁止 Options API
- [ ] 所有组件使用 Composition API（`ref` / `computed` / `watch`）
- [ ] 公共组件放在 `src/components/`，页面私有组件放在 `pages/xxx/components/`

### 2.2 模板规范

- [ ] 所有标签使用 uni-app 组件：`<view>` `<text>` `<scroll-view>` `<image>` `<input>` `<picker>`
- [ ] 禁止 HTML 标签：`<div>` `<span>` `<img>` `<button>`（用 `<view>` 替代）
- [ ] 组件文件名 PascalCase：`FreqBadge.vue` `TaskGroup.vue`
- [ ] 页面文件名保持 uni-app 约定：`index.vue`

### 2.3 组件拆分原则

- 同一段模板在 2 个以上页面出现 → 提取到 `src/components/`
- 单个 `.vue` 文件超过 300 行 → 拆分模板/逻辑
- 一段 UI 有独立的交互逻辑（如滑动手势、弹窗）→ 独立组件
- 只用一次的简单 UI 块，放在页面里即可

### 2.4 组件通信

```vue
<!-- ✅ 通过 props 传入，emit 向父级通信 -->
<script setup lang="ts">
interface Props {
  frequency: FrequencyType;
  weeklyCount?: number;
}
const props = defineProps<Props>();
const emit = defineEmits<{ confirm: []; cancel: [] }>();
</script>

<!-- ❌ 组件内直接调 API 或操作 Store -->
<script setup lang="ts">
import useHabitStore from '@/store/modules/habit';
const store = useHabitStore(); // 不要这样做
</script>
```

---

## 三、TypeScript 规范

### 3.1 类型定义

- [ ] **单一真相源**：类型只在 `src/models/` 定义一次，API 和 Store 层引用
- [ ] API 类型文件只保留请求/响应专用类型，通用类型从 models re-export
- [ ] Store 类型文件只保留 State 接口，通用类型从 models re-export

```typescript
// ✅ src/api/habit/types.ts
import type { FrequencyType } from '@/models/habit.model';
export type { FrequencyType };
export type { Habit as HabitRes } from '@/models/habit.model';
export interface CreateHabitReq { ... }

// ✅ src/store/modules/habit/types.ts
export type { Habit, DailyTask } from '@/models/habit.model';
export interface HabitState { ... }

// ❌ 在 API 和 Store 各定义一份 Habit
```

### 3.2 禁止事项

```typescript
// ❌ 禁止：使用 any
const habit = msg.extractedHabit as any;

// ✅ 正确：具体类型断言
habit.frequency = editState.value as ExtractedHabit['frequency'];

// ✅ 正确：属性逐个赋值
if (editState.field === 'habitName') habit.habitName = editState.value;

// ❌ 禁止：空 catch 块
try { await api(); } catch {}

// ✅ 正确：至少记录错误
try { await api(); } catch (e) { console.error('[habit]', e); }
```

### 3.3 命名规范

| 类型 | 规范 | 示例 |
|------|------|------|
| 类型/接口 | PascalCase | `Habit`, `DailyTask`, `ChatMessage` |
| 模型文件 | `xxx.model.ts` | `habit.model.ts` |
| Composable | `use` 前缀 | `useAuth()`, `useDashboard()` |
| Store | `use` + `Store` 后缀 | `useHabitStore()` |
| 组件事件 | `on` 前缀 | `onConfirm`, `onCancel` |
| 常量文件 | camelCase | `persona.ts` |

---

## 四、样式规范

### 4.1 核心规则

- [ ] 强制 UnoCSS 原子化类名，**禁止 `<style>` 块**（关键帧动画除外）
- [ ] 禁止内联样式 `style="..."`（动态计算值除外，如 `transform: translateX(${x}rpx)`）
- [ ] 使用 `rpx` 单位：`px-32rpx` `text-28rpx` `rounded-20rpx`
- [ ] 颜色使用硬编码方括号语法：`bg-[#1E293B]` `text-[#94A3B8]`

### 4.2 常用色值速查

| 用途 | 色值 | UnoCSS |
|------|------|--------|
| 深色头部 | `#1E293B` | `bg-[#1E293B]` |
| 头部卡片 | `#334155` | `bg-[#334155]` |
| 页面背景 | `#F8FAFC` | `bg-[#F8FAFC]` |
| 主色（蓝） | `#0EA5E9` | `bg-[#0EA5E9]` `text-[#0EA5E9]` |
| 主色深 | `#0284C7` | `bg-[#0284C7]` |
| 成功绿 | `#10B981` | `bg-[#10B981]` `text-[#10B981]` |
| 警告黄 | `#F59E0B` | `bg-[#F59E0B]` `text-[#F59E0B]` |
| 危险红 | `#EF4444` | `bg-[#EF4444]` `text-[#EF4444]` |
| 正文深 | `#1E293B` | `text-[#1E293B]` |
| 正文中 | `#64748B` | `text-[#64748B]` |
| 正文浅 | `#94A3B8` | `text-[#94A3B8]` |
| 禁用色 | `#CBD5E1` | `text-[#CBD5E1]` |
| 边框色 | `#E2E8F0` | `border-[#E2E8F0]` |

### 4.3 说明

`unocss-preset-weapp` 不支持自定义 `theme.colors` 配置，因此不使用语义化 token（如 `bg-bg-header`），直接使用硬编码色值。

---

## 五、状态管理规范

### 5.1 Setup Store 语法

- [ ] 所有 store 使用 Setup Store 语法（`defineStore('x', () => {...})`），禁止 Options API
- [ ] 选择性持久化，不全量 `persist: true`

```typescript
// ✅ 正确
const useHabitStore = defineStore('habit', () => {
  const habits = ref<Habit[]>([]);
  const activeHabits = computed(() => habits.value.filter(h => h.status === 'active'));

  async function fetchHabits() {
    habits.value = await HabitApi.getHabits();
  }

  return { habits, activeHabits, fetchHabits };
}, {
  persist: { pick: ['habits'] },
});

// ❌ 错误：Options API
const useHabitStore = defineStore('habit', {
  state: () => ({ habits: [] }),
  actions: { async fetchHabits() { ... } },
  persist: true,
});
```

### 5.2 持久化策略

| Store | 持久化字段 | 不持久化 |
|-------|-----------|----------|
| `habit` | `habits`, `todayMotivation` | `dailyTasks`（每次从 API 重新生成） |
| `ai` | `messages`（限制最近 50 条） | `isTyping`, `currentExtractedHabit` |
| `checkin` | 不持久化 | 全部（每次刷新重新拉取） |
| `user` | 全部 | — |
| `app` | 不持久化 | — |

### 5.3 Store 职责边界

| Store | 负责 | 不负责 |
|-------|------|--------|
| `habit` | 习惯列表、今日任务、增删改查 | 打卡逻辑（→ checkin） |
| `ai` | 消息列表、发送状态 | 习惯持久化（→ habit） |
| `checkin` | 打卡记录、统计数据 | 任务列表（→ habit） |
| `user` | 登录态、用户资料、教练人设 | 习惯数据（→ habit） |

### 5.4 响应式更新

```typescript
// ❌ 直接 mutate 对象属性（可能不触发响应式）
lastAI.habitConfirmed = true;

// ✅ 通过替换触发响应式
const idx = messages.value.findIndex(m => m.id === msgId);
if (idx !== -1) {
  messages.value[idx] = { ...messages.value[idx], habitConfirmed: true };
}
```

---

## 六、Composable 规范

### 6.1 何时提取 Composable

- 页面逻辑超过 100 行 → 提取到 `pages/xxx/composables/useXxx.ts`
- 多个页面共享的逻辑 → 提取到 `src/composables/`

### 6.2 Composable 结构

```typescript
// pages/tab/dashboard/composables/useDashboard.ts
export function useDashboard() {
  // 1. Store 引用
  const habitStore = useHabitStore();

  // 2. 响应式状态
  const loading = ref(true);

  // 3. 计算属性
  const completedCount = computed(() => habitStore.completedTasks.length);

  // 4. 方法
  async function loadData() { ... }

  // 5. 返回
  return { loading, completedCount, loadData };
}
```

---

## 七、API 请求层规范

### 7.1 单例模式

- [ ] `src/utils/request/index.ts` 中 axios 实例只创建一次
- [ ] 拦截器只注册一次
- [ ] 禁止每次请求都 `axios.create()`

### 7.2 调用规范

```typescript
// ✅ 通过 api 模块
import { AIApi } from '@/api';
const res = await AIApi.sendMessage({ message: content });

// ❌ 直接调 request
import { post } from '@/utils/request';
post('/api/ai/chat', { data: { message: content } });
```

### 7.3 错误处理

```typescript
// ✅ 页面/组件层处理错误
try {
  await habitStore.pauseHabit(habitId);
  uni.showToast({ title: '已暂停', icon: 'success' });
} catch (e) {
  console.error('[coach] pauseHabit failed', e);
  uni.showToast({ title: '操作失败', icon: 'none' });
}

// ❌ 空 catch 块吞掉错误
try { await api(); } catch {}
```

---

## 八、页面交互规范

- [ ] Loading 状态：显示骨架屏或加载指示器，禁止完全空白
- [ ] Empty 状态：列表为空时显示引导文案和操作按钮
- [ ] 成功反馈：关键操作使用 `uni.showToast` + `uni.vibrateShort`
- [ ] 乐观更新：切换人设、开关提醒等先更新 UI 再调 API，失败后回滚
- [ ] 骨架屏：使用 shimmer 动画（opacity 在 0.3/0.6 之间切换，800ms 间隔）

---

## 九、禁止事项

- [ ] 禁止 `console.log`（用 `console.error` 或移除）
- [ ] 禁止 `as any` 类型断言
- [ ] 禁止空 `catch {}` 块
- [ ] 禁止引入新依赖除非任务明确要求
- [ ] 禁止修改 `.gitignore` / `.env` 文件
- [ ] 禁止在页面中直接调 `uni.request`（通过 api 模块）
- [ ] 禁止在 Store 中操作 DOM 或调 `uni.showToast`
- [ ] 禁止在组件内直接调 API（通过 props/emit 或 composable）

---

## 十、提交规范

```
feat(chat): 新增习惯确认卡片组件
fix(dashboard): 修复骨架屏 shimmer 动画
refactor(types): 统一类型定义到 models/
style(coach): 修复死链，复用 FreqBadge 组件
chore: 清理 console.log 和未使用的类型
```

---

## 十一、检查清单（PR 合并前）

- [ ] `npx vue-tsc --noEmit` — 零类型错误
- [ ] 全局搜索 `console.log` — 无调试日志
- [ ] 全局搜索 `as any` — 无 any 类型断言
- [ ] 全局搜索 `catch {}` — 无空 catch 块
- [ ] 页面 < 200 行，组件 < 200 行，composable < 150 行
- [ ] 新增类型只在 `models/` 定义一次
- [ ] Store 使用 Setup Store 语法
- [ ] 颜色使用硬编码色值 `bg-[#xxx]`
