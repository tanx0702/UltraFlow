<template>
  <view class="min-h-screen bg-[#F8FAFC]">
    <!-- Header -->
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
            {{ progressMessage }}
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

    <!-- AI Daily Motivation -->
    <view class="mx-32rpx mt-24rpx rounded-16rpx bg-gradient-to-r from-[#F0F9FF] to-[#ECFEFF] p-24rpx shadow-sm">
      <view class="flex items-center">
        <text class="text-32rpx">☀️</text>
        <text class="ml-12rpx flex-1 text-26rpx text-[#64748B]">{{ motivationText }}</text>
      </view>
    </view>

    <!-- Task List -->
    <view class="mx-32rpx mt-32rpx">
      <!-- Pending Tasks -->
      <view v-if="habitStore.pendingTasks.length > 0">
        <view class="mb-16rpx flex items-center justify-between">
          <text class="text-26rpx font-medium text-[#94A3B8]">待完成</text>
          <text class="text-22rpx text-[#CBD5E1]">点击查看详情 · 右滑打卡</text>
        </view>
        <view v-for="task in habitStore.pendingTasks" :key="task.habitId" class="mb-16rpx">
          <!-- Swipe Container -->
          <view class="relative overflow-hidden rounded-20rpx" style="height: 144rpx">
            <!-- Green Background (revealed on swipe) -->
            <view
              class="absolute inset-0 flex items-center justify-start rounded-20rpx pl-32rpx"
              style="background-color: #10B981"
            >
              <text class="text-28rpx font-bold text-white">&#10003; 完成</text>
            </view>
            <!-- Swipeable Card -->
            <view
              class="absolute inset-0 rounded-20rpx bg-white p-24rpx shadow-sm"
              :style="{
                transform: `translateX(${swipeStates[task.habitId] || 0}rpx)`,
                opacity: swipeOpacities[task.habitId] ?? 1,
                transition: swipeTransitions[task.habitId] ? 'transform 0.3s ease, opacity 0.3s ease' : 'none',
              }"
              @touchstart="(e) => onTouchStart(task.habitId, e)"
              @touchmove="(e) => onTouchMove(task.habitId, e)"
              @touchend="() => onTouchEnd(task.habitId)"
            >
              <view class="flex items-center justify-between">
                <view class="flex flex-1 items-center">
                  <!-- Check circle icon -->
                  <view
                    class="h-56rpx w-56rpx flex items-center justify-center rounded-full border-2"
                    :class="todayCheckedMap[task.habitId] ? 'border-[#10B981] bg-[#10B981]' : 'border-[#CBD5E1]'"
                  >
                    <text v-if="todayCheckedMap[task.habitId]" class="text-28rpx text-white">✓</text>
                  </view>
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
                    <view v-if="task.frequency === 'challenge' && task.targetDays" class="mt-8rpx">
                      <view class="h-6rpx overflow-hidden rounded-full bg-[#E2E8F0]">
                        <view
                          class="h-full rounded-full bg-[#F59E0B]"
                          :style="{ width: challengeProgress(task) + '%' }"
                        />
                      </view>
                      <text class="mt-4rpx text-20rpx text-[#94A3B8]">{{ challengeProgress(task) }}%</text>
                    </view>
                  </view>
                </view>
                <!-- Streak badge + chevron -->
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
      </view>

      <!-- Empty State -->
      <view v-if="habitStore.pendingTasks.length === 0 && habitStore.completedTasks.length === 0" class="py-120rpx text-center">
        <text class="text-100rpx">📋</text>
        <view class="mt-24rpx text-28rpx text-[#94A3B8]">还没有习惯，去极律空间和 AI 教练聊聊吧</view>
        <view class="mt-32rpx flex justify-center">
          <view
            class="rounded-full bg-[#0EA5E9] px-48rpx py-16rpx"
            @tap="goToChat"
          >
            <text class="text-26rpx font-medium text-white">去极律空间</text>
          </view>
        </view>
      </view>

      <!-- Completed Tasks -->
      <view v-if="habitStore.completedTasks.length > 0" class="mt-32rpx">
        <view class="mb-16rpx text-26rpx font-medium text-[#94A3B8]">已完成</view>
        <view v-for="task in habitStore.completedTasks" :key="task.habitId" class="mb-16rpx">
          <view
            class="rounded-20rpx p-24rpx"
            style="background-color: #10B981"
            @tap="goToHabitDetail(task.habitId)"
          >
            <view class="flex items-center justify-between">
              <view class="flex flex-1 items-center">
                <view class="h-56rpx w-56rpx flex items-center justify-center rounded-full bg-white/20">
                  <text class="text-28rpx text-white">✓</text>
                </view>
                <view class="ml-20rpx">
                  <view class="text-30rpx font-bold text-white">{{ task.name }}</view>
                  <view class="mt-4rpx text-24rpx text-white/80">{{ task.target }}</view>
                </view>
              </view>
              <view class="flex flex-col items-end">
                <view
                  v-if="habitStreakMap[task.habitId] > 0"
                  class="mb-4rpx rounded-full bg-white/20 px-10rpx py-2rpx"
                >
                  <text class="text-22rpx text-white">🔥 {{ habitStreakMap[task.habitId] }}</text>
                </view>
                <text class="text-26rpx text-white">✅ 已完成</text>
              </view>
            </view>
            <view v-if="task.completedAt" class="mt-8rpx text-22rpx text-white/70">
              今天 {{ formatCheckInTime(task.completedAt) }} 打卡
            </view>
          </view>
        </view>
      </view>
    </view>

    <!-- 100% Celebration -->
    <view v-if="completionPercentage >= 100 && totalCount > 0" class="mx-32rpx mt-24rpx rounded-16rpx bg-[#FFFBEB] p-24rpx text-center">
      <text class="text-32rpx">🎉</text>
      <text class="ml-8rpx text-26rpx font-medium text-[#D97706]">太棒了！今日目标全部完成！</text>
    </view>

    <!-- Bottom safe area -->
    <view class="h-40rpx" />
  </view>
</template>

<script setup lang="ts">
import type { DailyTask } from '@/store/modules/habit/types';
import useHabitStore from '@/store/modules/habit';
import useCheckInStore from '@/store/modules/checkin';
import { useAuth } from '@/composables';
import { isLogin } from '@/utils/auth';
import { onShow } from '@dcloudio/uni-app';
import { computed, ref } from 'vue';

useAuth();
const habitStore = useHabitStore();
const checkInStore = useCheckInStore();

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

const progressMessage = computed(() => {
  if (totalCount.value === 0) return '新的一天，开始吧！';
  const pct = completionPercentage.value;
  if (pct === 0) return '新的一天，开始吧！';
  if (pct < 50) return '好的开始是成功的一半！';
  if (pct < 100) return '胜利在望，继续加油！';
  return '全部完成，太棒了！';
});

// ── Motivation ──

const motivationText = computed(() => {
  if (habitStore.todayMotivation) return habitStore.todayMotivation;
  return '今天也要加油鸭！';
});

// ── Data maps ──

const habitStreakMap = computed(() => {
  const map: Record<string, number> = {};
  for (const h of habitStore.habits) {
    map[h._id] = h.streak;
  }
  return map;
});

const todayCheckedMap = computed(() => {
  const map: Record<string, boolean> = {};
  for (const c of checkInStore.todayCheckIns) {
    map[c.habitId] = true;
  }
  return map;
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
    // Pure tap → navigate to detail
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

// ── Lifecycle ──

onShow(async () => {
  if (!isLogin()) return;

  try {
    await habitStore.fetchTodayHabits();
  } catch {
    habitStore.generateDailyTasks();
  }

  try {
    await checkInStore.fetchTodayCheckIns();
  } catch {}

  const checkedIds = checkInStore.todayCheckedHabitIds;
  for (const task of habitStore.dailyTasks) {
    if (checkedIds.includes(task.habitId)) {
      habitStore.markTaskCompleted(task.habitId);
    }
  }
});
</script>
