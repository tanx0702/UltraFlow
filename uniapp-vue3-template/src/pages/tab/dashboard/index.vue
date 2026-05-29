<template>
  <view class="min-h-screen bg-[#F8FAFC]">
    <!-- Skeleton State -->
    <view v-if="loading" class="px-32rpx pt-48rpx">
      <!-- Skeleton Header -->
      <view class="bg-[#1E293B] px-32rpx pb-24rpx pt-48rpx">
        <view class="flex items-center justify-between">
          <view>
            <view class="h-24rpx w-120rpx rounded bg-[#334155]" :style="{ opacity: shimmerOpacity }" />
            <view class="mt-8rpx h-36rpx w-160rpx rounded bg-[#334155]" :style="{ opacity: shimmerOpacity }" />
          </view>
        </view>
        <view class="mt-24rpx flex items-center rounded-20rpx bg-[#334155] p-24rpx">
          <view class="flex-shrink-0 rounded-full bg-[#475569]" style="width: 100rpx; height: 100rpx;" :style="{ opacity: shimmerOpacity }" />
          <view class="ml-20rpx flex-1">
            <view class="h-24rpx w-200rpx rounded bg-[#475569]" :style="{ opacity: shimmerOpacity }" />
            <view class="mt-8rpx h-36rpx w-120rpx rounded bg-[#475569]" :style="{ opacity: shimmerOpacity }" />
          </view>
        </view>
      </view>
      <!-- Skeleton Week Bar -->
      <view class="mt-24rpx flex justify-between px-16rpx">
        <view v-for="i in 7" :key="i" class="flex flex-col items-center">
          <view class="h-64rpx w-64rpx rounded-full bg-[#E2E8F0]" :style="{ opacity: shimmerOpacity }" />
          <view class="mt-8rpx h-20rpx w-32rpx rounded bg-[#E2E8F0]" :style="{ opacity: shimmerOpacity }" />
        </view>
      </view>
      <!-- Skeleton Cards -->
      <view class="mt-32rpx">
        <view v-for="i in 3" :key="i" class="mb-16rpx h-120rpx rounded-20rpx bg-white" :style="{ opacity: shimmerOpacity }" />
      </view>
    </view>

    <!-- Main Content -->
    <view v-else>
      <!-- Sticky Header -->
      <view class="sticky top-0 z-10 bg-[#1E293B] px-32rpx pb-40rpx pt-80rpx">
        <view class="flex items-center justify-between">
          <view>
            <view class="text-26rpx text-[#94A3B8]">{{ todayDate }}</view>
            <view class="mt-8rpx text-40rpx font-bold text-white">今日看板</view>
          </view>
        </view>

        <!-- Progress Ring + Stats -->
        <view class="mt-24rpx flex items-center rounded-20rpx bg-[#334155] p-24rpx">
          <!-- SVG Ring -->
          <view class="relative h-100rpx w-100rpx flex-shrink-0">
            <svg viewBox="0 0 100 100" class="h-full w-full -rotate-90">
              <circle
                cx="50" cy="50" r="42"
                fill="none"
                stroke="#475569"
                stroke-width="8"
              />
              <circle
                cx="50" cy="50" r="42"
                fill="none"
                :stroke="completionPercentage >= 100 ? '#F59E0B' : 'url(#progressGrad)'"
                stroke-width="8"
                stroke-linecap="round"
                :stroke-dasharray="2 * Math.PI * 42"
                :stroke-dashoffset="2 * Math.PI * 42 * (1 - completionPercentage / 100)"
                class="transition-all duration-500"
              />
              <defs>
                <linearGradient id="progressGrad" x1="0%" y1="0%" x2="100%" y2="0%">
                  <stop offset="0%" stop-color="#10B981" />
                  <stop offset="100%" stop-color="#0EA5E9" />
                </linearGradient>
              </defs>
            </svg>
            <view class="absolute inset-0 flex items-center justify-center">
              <text
                class="text-26rpx font-bold"
                :class="completionPercentage >= 100 ? 'text-[#F59E0B]' : 'text-[#34D399]'"
              >{{ completionPercentage }}%</text>
            </view>
          </view>

          <view class="ml-20rpx flex-1">
            <view class="text-24rpx text-[#94A3B8]">
              {{ smartMotivation }}
            </view>
            <view class="mt-8rpx flex items-baseline">
              <text class="text-44rpx font-bold text-white">{{ completedCount }}</text>
              <text class="text-26rpx text-[#94A3B8]">/{{ totalCount }} 项</text>
            </view>
          </view>
        </view>

        <!-- Gradient Progress Bar -->
        <view class="mt-16rpx h-8rpx overflow-hidden rounded-full bg-[#475569]">
          <view
            class="h-full rounded-full transition-all duration-500"
            style="background: linear-gradient(90deg, #10B981, #0EA5E9)"
            :style="{ width: `${completionPercentage}%` }"
          />
        </view>
      </view>

      <!-- Task List -->
      <view class="mx-32rpx mt-24rpx">
        <!-- Pending Tasks - Grouped by Time Period -->
        <view v-for="group in groupedTasks" :key="group.period" class="mb-24rpx">
          <view class="mb-12rpx flex items-center">
            <text class="text-26rpx font-medium text-[#64748B]">{{ group.label }}</text>
            <text class="ml-8rpx text-22rpx text-[#94A3B8]">{{ group.tasks.length }}项</text>
          </view>

          <view v-for="task in group.tasks" :key="task.habitId" class="mb-12rpx">
            <view class="relative overflow-hidden rounded-20rpx" style="height: 132rpx">
              <!-- Swipe Background -->
              <view
                class="absolute inset-0 flex items-center justify-start rounded-20rpx pl-32rpx"
                style="background-color: #10B981"
              >
                <text class="text-28rpx font-bold text-white">&#10003; 完成</text>
              </view>
              <!-- Card -->
              <view
                class="absolute inset-0 flex items-center rounded-20rpx bg-white px-24rpx py-20rpx shadow-sm"
                :style="{
                  transform: `translateX(${swipeStates[task.habitId] || 0}rpx)`,
                  opacity: swipeOpacities[task.habitId] ?? 1,
                  transition: swipeTransitions[task.habitId] ? 'transform 0.3s ease, opacity 0.3s ease' : 'none',
                }"
                @touchstart="(e) => onTouchStart(task.habitId, e)"
                @touchmove="(e) => onTouchMove(task.habitId, e)"
                @touchend="() => onTouchEnd(task.habitId)"
              >
                <!-- Icon -->
                <view
                  class="h-72rpx w-72rpx flex flex-shrink-0 items-center justify-center rounded-full"
                  :style="{ backgroundColor: (task.color || '#3B82F6') + '26' }"
                >
                  <text class="text-40rpx">{{ task.icon || '📋' }}</text>
                </view>
                <!-- Info -->
                <view class="ml-20rpx flex-1">
                  <view class="text-30rpx font-bold text-[#1E293B]">{{ task.name }}</view>
                  <view class="mt-4rpx text-24rpx text-[#94A3B8]">{{ task.target }} · {{ task.reminderTime }}</view>
                  <!-- Frequency badge -->
                  <view v-if="task.frequency !== 'daily'" class="mt-6rpx">
                    <text
                      class="rounded-full px-12rpx py-2rpx text-20rpx"
                      :class="freqBadgeStyle(task)"
                    >{{ freqBadge(task) }}</text>
                  </view>
                  <!-- Challenge progress bar -->
                  <view v-if="task.frequency === 'challenge' && task.targetDays" class="mt-6rpx">
                    <view class="h-6rpx overflow-hidden rounded-full bg-[#E2E8F0]">
                      <view
                        class="h-full rounded-full bg-[#F59E0B]"
                        :style="{ width: challengeProgress(task) + '%' }"
                      />
                    </view>
                    <text class="mt-2rpx text-20rpx text-[#94A3B8]">{{ challengeProgress(task) }}%</text>
                  </view>
                </view>
                <!-- Streak + Arrow -->
                <view class="ml-8rpx flex flex-col items-center">
                  <view
                    v-if="habitStreakMap[task.habitId] > 0"
                    class="mb-4rpx rounded-full bg-[#FFF7ED] px-10rpx py-2rpx"
                  >
                    <text class="text-22rpx font-medium text-[#F97316]">🔥 {{ habitStreakMap[task.habitId] }}</text>
                  </view>
                  <text class="text-28rpx text-[#CBD5E1]">›</text>
                </view>
              </view>
            </view>
          </view>
        </view>

        <!-- Empty State -->
        <view v-if="totalCount === 0" class="py-120rpx text-center">
          <text class="text-100rpx">📋</text>
          <view class="mt-24rpx text-28rpx text-[#94A3B8]">还没有习惯，去极律空间和 AI 教练聊聊吧</view>
          <view class="mt-32rpx flex justify-center">
            <view class="rounded-full bg-[#0EA5E9] px-48rpx py-16rpx" @tap="goToChat">
              <text class="text-26rpx font-medium text-white">去极律空间</text>
            </view>
          </view>
        </view>

        <!-- Completed Tasks -->
        <view v-if="habitStore.completedTasks.length > 0" class="mt-8rpx">
          <view class="mb-12rpx text-26rpx font-medium text-[#64748B]">已完成</view>
          <view v-for="task in habitStore.completedTasks" :key="task.habitId" class="mb-12rpx">
            <view
              class="flex items-center rounded-20rpx px-24rpx py-20rpx"
              :style="{ backgroundColor: (task.color || '#10B981') + '1A' }"
              @tap="goToHabitDetail(task.habitId)"
            >
              <view
                class="h-72rpx w-72rpx flex flex-shrink-0 items-center justify-center rounded-full"
                :style="{ backgroundColor: (task.color || '#10B981') + '26' }"
              >
                <text class="text-40rpx">{{ task.icon || '📋' }}</text>
              </view>
              <view class="ml-20rpx flex-1">
                <view class="text-28rpx font-medium text-[#1E293B]">{{ task.name }}</view>
                <view class="mt-2rpx text-22rpx text-[#94A3B8]">{{ task.target }}</view>
              </view>
              <view class="flex flex-col items-end">
                <view
                  v-if="habitStreakMap[task.habitId] > 0"
                  class="mb-4rpx rounded-full bg-[#FFF7ED] px-10rpx py-2rpx"
                >
                  <text class="text-22rpx text-[#F97316]">🔥 {{ habitStreakMap[task.habitId] }}</text>
                </view>
                <text v-if="task.completedAt" class="text-22rpx text-[#94A3B8]">
                  {{ formatCheckInTime(task.completedAt) }}
                </text>
              </view>
            </view>
          </view>
        </view>

        <!-- Celebration Banner -->
        <view
          v-if="completionPercentage >= 100 && totalCount > 0"
          class="mt-16rpx rounded-20rpx bg-gradient-to-r from-[#FFFBEB] to-[#FEF3C7] p-32rpx text-center"
        >
          <text class="text-48rpx">🎉</text>
          <view class="mt-8rpx text-28rpx font-bold text-[#D97706]">太棒了！今日目标全部完成！</view>
          <view class="mt-4rpx text-24rpx text-[#B45309]">坚持就是胜利，明天继续加油</view>
        </view>
      </view>

      <!-- Bottom safe area -->
      <view class="h-40rpx" />
    </view>
  </view>
</template>

<script setup lang="ts">
import type { DailyTask } from '@/store/modules/habit/types';
import useHabitStore from '@/store/modules/habit';
import useCheckInStore from '@/store/modules/checkin';
import { useAuth } from '@/composables';
import { isLogin } from '@/utils/auth';
import { onPullDownRefresh, onShow } from '@dcloudio/uni-app';
import { computed, onUnmounted, ref } from 'vue';

useAuth();
const habitStore = useHabitStore();
const checkInStore = useCheckInStore();

// ── Loading + Shimmer ──

const loading = ref(true);
const shimmerOpacity = ref(0.3);
let shimmerInterval: ReturnType<typeof setInterval> | null = null;

function startShimmer() {
  shimmerInterval = setInterval(() => {
    shimmerOpacity.value = shimmerOpacity.value === 0.3 ? 0.6 : 0.3;
  }, 800);
}

function stopShimmer() {
  if (shimmerInterval) {
    clearInterval(shimmerInterval);
    shimmerInterval = null;
  }
}

onUnmounted(() => stopShimmer());

// ── Date helpers ──

const todayDate = computed(() => {
  const date = new Date();
  const month = date.getMonth() + 1;
  const day = date.getDate();
  const weekDays = ['日', '一', '二', '三', '四', '五', '六'];
  const weekDay = weekDays[date.getDay()];
  return `${month}月${day}日 周${weekDay}`;
});

function formatCheckInTime(isoStr: string): string {
  const d = new Date(isoStr);
  return `${String(d.getHours()).padStart(2, '0')}:${String(d.getMinutes()).padStart(2, '0')}`;
}

// ── Progress ──

const completedCount = computed(() => habitStore.completedTasks.length);
const totalCount = computed(() => habitStore.dailyTasks.length);
const completionPercentage = computed(() => {
  if (totalCount.value === 0) return 0;
  return Math.round((completedCount.value / totalCount.value) * 100);
});

// ── Smart Motivation ──

const smartMotivation = computed(() => {
  if (habitStore.todayMotivation) return habitStore.todayMotivation;
  if (totalCount.value === 0) return '去创建第一个习惯吧';
  const pct = completionPercentage.value;
  const maxStreak = Math.max(0, ...habitStore.habits.map(h => h.streak));
  if (pct === 0 && maxStreak > 0) return `已连续坚持${maxStreak}天，别断了！`;
  if (pct === 0) return '新的一天，开始行动吧';
  if (pct < 50) return '好的开始是成功的一半';
  if (pct < 100) return '胜利在望，继续加油';
  return '全部完成，太棒了！';
});

// ── Data maps ──

const habitStreakMap = computed(() => {
  const map: Record<string, number> = {};
  for (const h of habitStore.habits) {
    map[h._id] = h.streak;
  }
  return map;
});

// ── Frequency helpers ──

function freqBadge(task: DailyTask): string {
  switch (task.frequency) {
    case 'weekly_days': return '每周固定';
    case 'weekly_count': return `每周${task.weeklyCount || '?'}次`;
    case 'challenge': return `${task.targetDays || '?'}天挑战`;
    default: return '';
  }
}

function freqBadgeStyle(task: DailyTask): string {
  switch (task.frequency) {
    case 'weekly_days': return 'bg-[#EFF6FF] text-[#3B82F6]';
    case 'weekly_count': return 'bg-[#F0FDF4] text-[#10B981]';
    case 'challenge': return 'bg-[#FFFBEB] text-[#D97706]';
    default: return '';
  }
}

function challengeProgress(task: DailyTask): number {
  if (!task.targetDays) return 0;
  const habit = habitStore.habits.find(h => h._id === task.habitId);
  const streak = habit?.streak ?? 0;
  return Math.min(Math.round((streak / task.targetDays) * 100), 100);
}

// ── Week Day Styling ──

function weekDayClass(day: { completed: boolean; isToday: boolean; checkInCount: number }) {
  if (day.completed) return 'bg-[#10B981] text-white';
  if (day.isToday) return 'border-2 border-[#0EA5E9] text-[#0EA5E9]';
  return 'bg-[#334155] text-[#64748B]';
}


// ── Time Period Grouping ──

interface TaskGroup {
  period: string;
  label: string;
  tasks: DailyTask[];
}

const groupedTasks = computed<TaskGroup[]>(() => {
  const groups: Record<string, DailyTask[]> = { morning: [], afternoon: [], evening: [], lateNight: [] };
  for (const task of habitStore.pendingTasks) {
    const hour = task.reminderTime ? parseInt(task.reminderTime.split(':')[0]) : 18;
    if (hour >= 6 && hour < 12) groups.morning.push(task);
    else if (hour >= 12 && hour < 18) groups.afternoon.push(task);
    else if (hour >= 18) groups.evening.push(task);
    else groups.lateNight.push(task);
  }
  for (const key of Object.keys(groups)) {
    groups[key].sort((a, b) => (a.reminderTime || '').localeCompare(b.reminderTime || ''));
  }
  const order = [
    { period: 'morning', label: '🌅 上午' },
    { period: 'afternoon', label: '🌤️ 下午' },
    { period: 'evening', label: '🌙 晚上' },
    { period: 'lateNight', label: '🌃 深夜' },
  ];
  return order
    .map(o => ({ ...o, tasks: groups[o.period] }))
    .filter(g => g.tasks.length > 0);
});

// ── Swipe + Tap ──

const swipeStates = ref<Record<string, number>>({});
const swipeOpacities = ref<Record<string, number>>({});
const swipeTransitions = ref<Record<string, boolean>>({});
const touchMoved = ref<Record<string, boolean>>({});
const touchStartX = ref(0);
const swipeThreshold = 160;

function onTouchStart(habitId: string, e: any) {
  touchStartX.value = e.touches[0].clientX;
  swipeTransitions.value[habitId] = false;
  touchMoved.value[habitId] = false;
}

function onTouchMove(habitId: string, e: any) {
  touchMoved.value[habitId] = true;
  const deltaX = (e.touches[0].clientX - touchStartX.value) * 2;
  const offset = Math.max(0, Math.min(deltaX, 500));
  swipeStates.value[habitId] = offset;
  swipeOpacities.value[habitId] = 1 - (offset / 500) * 0.7;
}

function onTouchEnd(habitId: string) {
  if (!touchMoved.value[habitId]) {
    goToHabitDetail(habitId);
    return;
  }

  const offset = swipeStates.value[habitId] || 0;
  if (offset > swipeThreshold) {
    swipeTransitions.value[habitId] = true;
    swipeStates.value[habitId] = 750;
    swipeOpacities.value[habitId] = 0;
    setTimeout(() => {
      handleComplete(habitId);
      swipeStates.value[habitId] = 0;
      swipeOpacities.value[habitId] = 1;
      swipeTransitions.value[habitId] = true;
      setTimeout(() => {
        swipeTransitions.value[habitId] = false;
      }, 300);
    }, 300);
  } else {
    swipeTransitions.value[habitId] = true;
    swipeStates.value[habitId] = 0;
    swipeOpacities.value[habitId] = 1;
    setTimeout(() => {
      swipeTransitions.value[habitId] = false;
    }, 300);
  }
}

// ── Navigation ──

function goToChat() {
  uni.switchTab({ url: '/pages/tab/chat/index' });
}

function goToHabitDetail(habitId: string) {
  uni.navigateTo({ url: `/pages/common/habit-detail/index?habitId=${habitId}` });
}

// ── Check-in ──

async function handleComplete(habitId: string) {
  try {
    await checkInStore.checkIn(habitId);
  } catch {
    const now = new Date();
    const dateStr = `${now.getFullYear()}-${String(now.getMonth() + 1).padStart(2, '0')}-${String(now.getDate()).padStart(2, '0')}`;
    checkInStore.todayCheckIns.push({
      _id: `mock_${Date.now()}`,
      habitId,
      userId: 'dev_user',
      checkInDate: dateStr,
      checkInTime: now.toISOString(),
      createdAt: now.toISOString(),
    });
  }
  habitStore.markTaskCompleted(habitId);
  uni.showToast({ title: '打卡成功', icon: 'success', duration: 1000 });
}

// ── Data Loading ──

async function loadAllData() {
  try {
    await habitStore.fetchTodayHabits();
  } catch {
    habitStore.generateDailyTasks();
  }

  try {
    await checkInStore.fetchTodayCheckIns();
  } catch {}

  try {
    await checkInStore.fetchWeekDayStatuses();
  } catch {}

  const checkedIds = checkInStore.todayCheckedHabitIds;
  for (const task of habitStore.dailyTasks) {
    if (checkedIds.includes(task.habitId)) {
      habitStore.markTaskCompleted(task.habitId);
    }
  }
}

// ── Lifecycle ──

onShow(async () => {
  if (!isLogin()) return;
  loading.value = true;
  startShimmer();
  await loadAllData();
  loading.value = false;
  stopShimmer();
});

onPullDownRefresh(async () => {
  await loadAllData();
  uni.stopPullDownRefresh();
});
</script>
