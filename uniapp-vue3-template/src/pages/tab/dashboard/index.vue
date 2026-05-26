<template>
  <view class="min-h-screen bg-[#F8FAFC]">
    <!-- Header -->
    <view class="bg-[#1E293B] px-32rpx pb-40rpx pt-80rpx">
      <view class="flex items-center justify-between">
        <view>
          <view class="text-26rpx text-[#94A3B8]">{{ todayDate }}</view>
          <view class="mt-8rpx text-40rpx font-bold text-white">今日看板</view>
        </view>
      </view>

      <!-- Progress -->
      <view class="mt-24rpx flex items-center justify-between rounded-20rpx bg-[#334155] p-24rpx">
        <view>
          <view class="text-24rpx text-[#94A3B8]">今日进度</view>
          <view class="mt-8rpx flex items-baseline">
            <text class="text-48rpx font-bold text-white">{{ completedCount }}</text>
            <text class="text-28rpx text-[#94A3B8]">/{{ totalCount }}</text>
          </view>
        </view>
        <view class="relative h-100rpx w-100rpx">
          <view class="absolute inset-0 flex items-center justify-center">
            <text
              class="text-28rpx font-bold"
              :style="{ color: progressFlash ? '#34D399' : '#10B981' }"
            >{{ completionPercentage }}%</text>
          </view>
        </view>
      </view>

      <!-- Progress Bar -->
      <view class="mt-16rpx h-8rpx overflow-hidden rounded-full bg-[#475569]">
        <view
          class="h-full rounded-full transition-all duration-300"
          :class="completionPercentage >= 100 ? 'bg-[#F59E0B]' : 'bg-[#10B981]'"
          :style="{ width: `${completionPercentage}%` }"
        />
      </view>
    </view>

    <!-- AI Daily Motivation -->
    <view class="mx-32rpx mt-24rpx rounded-16rpx bg-[#F0F9FF] p-24rpx">
      <view class="flex items-center">
        <text class="text-32rpx">☀️</text>
        <text class="ml-12rpx text-26rpx text-[#64748B]">{{ motivationText }}</text>
      </view>
    </view>

    <!-- Task List -->
    <view class="mx-32rpx mt-32rpx">
      <!-- Pending Tasks -->
      <view v-if="habitStore.pendingTasks.length > 0">
        <view class="mb-16rpx text-26rpx font-medium text-[#94A3B8]">待完成</view>
        <view v-for="task in habitStore.pendingTasks" :key="task.habitId" class="mb-16rpx">
          <!-- Swipe Container -->
          <view
            class="relative overflow-hidden rounded-20rpx"
            style="height: 144rpx"
          >
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
                <view class="flex items-center">
                  <view class="h-56rpx w-56rpx flex items-center justify-center rounded-16rpx bg-[#1E293B]">
                    <text class="text-28rpx text-[#0EA5E9]">○</text>
                  </view>
                  <view class="ml-20rpx">
                    <view class="text-30rpx font-bold text-[#1E293B]">{{ task.name }}</view>
                    <view class="mt-4rpx text-24rpx text-[#94A3B8]">{{ task.target }} · {{ task.reminderTime }}</view>
                  </view>
                </view>
                <text class="text-24rpx text-[#CBD5E1]">&#9654;</text>
              </view>
              <view class="mt-8rpx text-center text-22rpx text-[#CBD5E1]">&#8594; 右滑打卡</view>
            </view>
          </view>
        </view>
      </view>

      <!-- Empty State -->
      <view v-if="habitStore.pendingTasks.length === 0 && habitStore.completedTasks.length === 0" class="py-120rpx text-center">
        <text class="text-100rpx text-[#CBD5E1]">📋</text>
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
          <view class="rounded-20rpx bg-[#10B981] p-24rpx">
            <view class="flex items-center justify-between">
              <view class="flex items-center">
                <view class="h-56rpx w-56rpx flex items-center justify-center rounded-16rpx bg-white/20">
                  <text class="text-28rpx text-white">✓</text>
                </view>
                <view class="ml-20rpx">
                  <view class="text-30rpx font-bold text-white">{{ task.name }}</view>
                  <view class="mt-4rpx text-24rpx text-white/80">{{ task.target }}</view>
                </view>
              </view>
              <text class="text-26rpx text-white">✅ 已完成</text>
            </view>
            <view class="mt-12rpx text-22rpx text-white/70">{{ todayDateStr }}</view>
          </view>
        </view>
      </view>
    </view>

    <!-- 100% Celebration -->
    <view v-if="completionPercentage >= 100 && totalCount > 0" class="mx-32rpx mt-24rpx rounded-16rpx bg-[#FFFBEB] p-24rpx text-center">
      <text class="text-32rpx">🎉</text>
      <text class="ml-8rpx text-26rpx font-medium text-[#D97706]">太棒了！今日目标全部完成！</text>
    </view>

  </view>
</template>

<script setup lang="ts">
import useHabitStore from '@/store/modules/habit';
import useCheckInStore from '@/store/modules/checkin';
import { useAuth } from '@/composables';
import { isLogin } from '@/utils/auth';
import { onShow } from '@dcloudio/uni-app';
import { computed, ref } from 'vue';

useAuth();
const habitStore = useHabitStore();
const checkInStore = useCheckInStore();

const todayDate = computed(() => {
  const date = new Date();
  const month = date.getMonth() + 1;
  const day = date.getDate();
  const weekDays = ['日', '一', '二', '三', '四', '五', '六'];
  const weekDay = weekDays[date.getDay()];
  return `${month}月${day}日 周${weekDay}`;
});

const todayDateStr = computed(() => {
  const d = new Date();
  return `${d.getFullYear()}-${String(d.getMonth() + 1).padStart(2, '0')}-${String(d.getDate()).padStart(2, '0')}`;
});

const motivationText = computed(() => {
  if (habitStore.todayMotivation) return habitStore.todayMotivation;
  return '今天也要加油鸭！';
});

const completedCount = computed(() => habitStore.completedTasks.length);
const totalCount = computed(() => habitStore.dailyTasks.length);
const completionPercentage = computed(() => {
  if (totalCount.value === 0) return 0;
  return Math.round((completedCount.value / totalCount.value) * 100);
});

// Swipe state
const swipeStates = ref<Record<string, number>>({});
const swipeOpacities = ref<Record<string, number>>({});
const swipeTransitions = ref<Record<string, boolean>>({});
const progressFlash = ref(false);
const touchStartX = ref(0);
const swipeThreshold = 160; // rpx

function onTouchStart(habitId: string, e: any) {
  touchStartX.value = e.touches[0].clientX;
  swipeTransitions.value[habitId] = false;
}

function onTouchMove(habitId: string, e: any) {
  const deltaX = (e.touches[0].clientX - touchStartX.value) * 2; // scale for rpx
  const offset = Math.max(0, Math.min(deltaX, 500));
  swipeStates.value[habitId] = offset;
  // Fade out as card slides: 1 → 0.3 over the swipe range
  swipeOpacities.value[habitId] = 1 - (offset / 500) * 0.7;
}

function onTouchEnd(habitId: string) {
  const offset = swipeStates.value[habitId] || 0;
  if (offset > swipeThreshold) {
    // Swipe complete — slide off + fade out
    swipeTransitions.value[habitId] = true;
    swipeStates.value[habitId] = 750;
    swipeOpacities.value[habitId] = 0;
    setTimeout(() => {
      handleComplete(habitId);
      // Reset for next use
      swipeStates.value[habitId] = 0;
      swipeOpacities.value[habitId] = 1;
      swipeTransitions.value[habitId] = true;
      setTimeout(() => {
        swipeTransitions.value[habitId] = false;
      }, 300);
    }, 300);
  } else {
    // Snap back
    swipeTransitions.value[habitId] = true;
    swipeStates.value[habitId] = 0;
    swipeOpacities.value[habitId] = 1;
    setTimeout(() => {
      swipeTransitions.value[habitId] = false;
    }, 300);
  }
}

function goToChat() {
  uni.switchTab({ url: '/pages/tab/chat/index' });
}

async function handleComplete(habitId: string) {
  try {
    await checkInStore.checkIn(habitId);
  } catch {
    // TODO: 接入真实数据后删除 mock fallback
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
  progressFlash.value = true;
  setTimeout(() => { progressFlash.value = false; }, 600);
}

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

