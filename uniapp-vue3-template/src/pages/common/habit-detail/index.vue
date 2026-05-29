<template>
  <scroll-view class="min-h-screen bg-[#F8FAFC]" scroll-y>
    <!-- Header -->
    <view class="bg-[#1E293B] px-32rpx pb-32rpx pt-80rpx">
      <view class="flex items-center justify-between">
        <view class="flex items-center" @tap="goBack">
          <text class="text-36rpx text-white">&#8592;</text>
        </view>
        <text class="text-34rpx font-bold text-white">{{ habit?.name || '习惯详情' }}</text>
        <view
          class="rounded-full px-16rpx py-4rpx"
          :style="{ backgroundColor: statusBadge.bg }"
        >
          <text class="text-22rpx font-medium" :style="{ color: statusBadge.color }">{{ statusBadge.text }}</text>
        </view>
      </view>

      <!-- Stats Row -->
      <view class="mt-24rpx flex gap-16rpx">
        <view class="flex-1 rounded-16rpx bg-[#334155] p-16rpx text-center">
          <text class="text-26rpx">🔥</text>
          <view class="mt-4rpx text-36rpx font-bold text-white">{{ habit?.streak ?? 0 }}</view>
          <view class="mt-2rpx text-20rpx text-[#94A3B8]">天连续</view>
        </view>
        <view class="flex-1 rounded-16rpx bg-[#334155] p-16rpx text-center">
          <text class="text-26rpx">🏆</text>
          <view class="mt-4rpx text-36rpx font-bold text-white">{{ habit?.bestStreak ?? 0 }}</view>
          <view class="mt-2rpx text-20rpx text-[#94A3B8]">天最佳</view>
        </view>
        <view class="flex-1 rounded-16rpx bg-[#334155] p-16rpx text-center">
          <text class="text-26rpx">{{ habit?.icon || '📋' }}</text>
          <view class="mt-4rpx text-36rpx font-bold text-white">{{ habit?.totalCheckIns ?? 0 }}</view>
          <view class="mt-2rpx text-20rpx text-[#94A3B8]">次累计</view>
        </view>
      </view>
    </view>

    <!-- Heatmap Card -->
    <view class="mx-32rpx mt-24rpx rounded-20rpx bg-white p-24rpx shadow-sm">
      <view class="flex items-center justify-between">
        <text class="text-28rpx font-semibold text-[#1E293B]">打卡日历</text>
        <view class="flex items-center gap-12rpx">
          <view class="h-48rpx w-48rpx flex items-center justify-center" @tap="prevMonth">
            <text class="text-28rpx text-[#94A3B8]">&#9664;</text>
          </view>
          <text class="text-24rpx font-medium text-[#475569]">{{ currentYear }}年{{ currentMonth }}月</text>
          <view
            class="h-48rpx w-48rpx flex items-center justify-center"
            :class="isCurrentMonth ? 'opacity-30' : ''"
            @tap="nextMonth"
          >
            <text class="text-28rpx text-[#94A3B8]">&#9654;</text>
          </view>
        </view>
      </view>

      <!-- Weekday Headers -->
      <view class="mb-8rpx mt-12rpx flex">
        <view v-for="wd in weekdays" :key="wd" class="flex-1 text-center">
          <text class="text-20rpx text-[#94A3B8]">{{ wd }}</text>
        </view>
      </view>

      <!-- Grid -->
      <view class="flex flex-wrap">
        <view
          v-for="(cell, idx) in gridCells"
          :key="idx"
          class="rounded-6rpx"
          :style="{ width: cellSize, height: cellSize, backgroundColor: cell.color, marginBottom: '6rpx', marginRight: idx % 7 === 6 ? '0' : '6rpx' }"
        />
      </view>

      <!-- Legend -->
      <view class="mt-12rpx flex items-center justify-end">
        <text class="mr-8rpx text-20rpx text-[#94A3B8]">未打卡</text>
        <view class="mr-4rpx h-16rpx w-16rpx rounded-2rpx" style="background-color: #E5E7EB" />
        <view class="mr-16rpx h-16rpx w-16rpx rounded-2rpx" style="background-color: #10B981" />
        <text class="text-20rpx text-[#94A3B8]">已打卡</text>
      </view>
    </view>

    <!-- Habit Info Card -->
    <view class="mx-32rpx mt-16rpx rounded-20rpx bg-white p-24rpx shadow-sm">
      <text class="text-28rpx font-semibold text-[#1E293B]">习惯信息</text>
      <view class="mt-16rpx space-y-12rpx">
        <view class="flex items-center">
          <text class="w-100rpx text-26rpx text-[#94A3B8]">目标</text>
          <text class="text-26rpx text-[#1E293B]">{{ habit?.target }}</text>
        </view>
        <view class="flex items-center">
          <text class="w-100rpx text-26rpx text-[#94A3B8]">频率</text>
          <text class="text-26rpx text-[#1E293B]">{{ freqDescription }}</text>
        </view>
        <view v-if="habit?.reminderTime" class="flex items-center">
          <text class="w-100rpx text-26rpx text-[#94A3B8]">提醒</text>
          <text class="text-26rpx text-[#1E293B]">{{ habit.reminderTime }}</text>
        </view>
        <view class="flex items-center">
          <text class="w-100rpx text-26rpx text-[#94A3B8]">创建于</text>
          <text class="text-26rpx text-[#1E293B]">{{ formatDate(habit?.createdAt) }}</text>
        </view>
      </view>
    </view>

    <!-- Actions -->
    <view class="mx-32rpx mt-24rpx mb-32rpx space-y-16rpx">
      <view
        class="rounded-full py-20rpx text-center"
        :style="{ backgroundColor: habit?.status === 'paused' ? '#10B981' : '#F59E0B' }"
        @tap="togglePause"
      >
        <text class="text-28rpx font-medium text-white">
          {{ habit?.status === 'paused' ? '恢复习惯' : '暂停习惯' }}
        </text>
      </view>
      <view
        class="rounded-full bg-[#EF4444] py-20rpx text-center"
        @tap="onDelete"
      >
        <text class="text-28rpx font-medium text-white">删除习惯</text>
      </view>
    </view>
  </scroll-view>
</template>

<script setup lang="ts">
import type { HabitRes } from '@/api/habit/types';
import type { CheckInDateInfo } from '@/api/checkin/types';
import { HabitApi, CheckInApi } from '@/api';
import useHabitStore from '@/store/modules/habit';
import { onLoad } from '@dcloudio/uni-app';
import { computed, ref } from 'vue';

const habitStore = useHabitStore();

const habit = ref<HabitRes | null>(null);
const checkInDates = ref<CheckInDateInfo[]>([]);

const now = new Date();
const currentYear = ref(now.getFullYear());
const currentMonth = ref(now.getMonth() + 1);

const weekdays = ['一', '二', '三', '四', '五', '六', '日'];

const statusBadge = computed(() => {
  if (habit.value?.status === 'paused') {
    return { bg: '#FEF3C7', color: '#D97706', text: '已暂停' };
  }
  if (habit.value?.status === 'archived') {
    return { bg: '#FEE2E2', color: '#DC2626', text: '已归档' };
  }
  return { bg: '#D1FAE5', color: '#059669', text: '进行中' };
});

const freqDescription = computed(() => {
  if (!habit.value) return '';
  const h = habit.value;
  switch (h.frequency) {
    case 'daily': return '每天';
    case 'weekly_days': {
      const names = ['一', '二', '三', '四', '五', '六', '日'];
      const days = (h.specificDays || []).map(d => names[d - 1] || d);
      return `每周${days.join('、')}`;
    }
    case 'weekly_count': return `每周${h.weeklyCount || '?'}次`;
    case 'challenge': return `${h.targetDays || '?'}天挑战`;
    default: return h.frequency;
  }
});

const isCurrentMonth = computed(() => {
  return currentYear.value === now.getFullYear() && currentMonth.value === now.getMonth() + 1;
});

const cellSize = computed(() => '86rpx');

const heatmapDataMap = computed(() => {
  return checkInDates.value.reduce<Record<string, { count: number; total: number }>>((map, d) => {
    map[d.date] = { count: d.count, total: d.total };
    return map;
  }, {});
});

function getHeatmapColor(count: number, total: number): string {
  if (total === 0) return '#E5E7EB';
  if (count === 0) return '#E5E7EB';
  return '#10B981';
}

interface GridCell {
  color: string;
}

const gridCells = computed<GridCell[]>(() => {
  const year = currentYear.value;
  const month = currentMonth.value;
  const daysInMonth = new Date(year, month, 0).getDate();
  let firstDayOfWeek = new Date(year, month - 1, 1).getDay();
  firstDayOfWeek = firstDayOfWeek === 0 ? 6 : firstDayOfWeek - 1;

  const cells: GridCell[] = [];

  for (let i = 0; i < firstDayOfWeek; i++) {
    cells.push({ color: 'transparent' });
  }

  for (let d = 1; d <= daysInMonth; d++) {
    const dateStr = `${year}-${String(month).padStart(2, '0')}-${String(d).padStart(2, '0')}`;
    const data = heatmapDataMap.value[dateStr];

    let color: string;
    if (data) {
      color = getHeatmapColor(data.count, data.total);
    } else if (new Date(dateStr) > now) {
      color = '#F1F5F9';
    } else {
      color = '#E5E7EB';
    }

    cells.push({ color });
  }

  return cells;
});

function formatDate(isoStr?: string): string {
  if (!isoStr) return '';
  const d = new Date(isoStr);
  return `${d.getFullYear()}-${String(d.getMonth() + 1).padStart(2, '0')}-${String(d.getDate()).padStart(2, '0')}`;
}

async function loadData(habitId: string) {
  try {
    const [h, dates] = await Promise.all([
      HabitApi.getHabitById(habitId),
      CheckInApi.getHabitCheckInDates(habitId, currentYear.value, currentMonth.value),
    ]);
    habit.value = h;
    checkInDates.value = dates;
  } catch {
    uni.showToast({ title: '加载失败', icon: 'error' });
  }
}

async function loadDates() {
  if (!habit.value) return;
  try {
    const dates = await CheckInApi.getHabitCheckInDates(
      habit.value._id, currentYear.value, currentMonth.value,
    );
    checkInDates.value = dates;
  } catch {}
}

function prevMonth() {
  if (currentMonth.value === 1) {
    currentMonth.value = 12;
    currentYear.value--;
  } else {
    currentMonth.value--;
  }
  loadDates();
}

function nextMonth() {
  if (isCurrentMonth.value) return;
  if (currentMonth.value === 12) {
    currentMonth.value = 1;
    currentYear.value++;
  } else {
    currentMonth.value++;
  }
  loadDates();
}

async function togglePause() {
  if (!habit.value) return;
  try {
    if (habit.value.status === 'paused') {
      await HabitApi.resumeHabit(habit.value._id);
      habit.value.status = 'active';
      uni.showToast({ title: '已恢复', icon: 'success' });
    } else {
      await HabitApi.pauseHabit(habit.value._id);
      habit.value.status = 'paused';
      uni.showToast({ title: '已暂停', icon: 'success' });
    }
  } catch {
    uni.showToast({ title: '操作失败', icon: 'error' });
  }
}

async function onDelete() {
  const res = await uni.showModal({
    title: '删除习惯',
    content: '确定要删除这个习惯吗？此操作不可恢复。',
  });
  if (!res.confirm || !habit.value) return;

  try {
    await habitStore.deleteHabit(habit.value._id);
    uni.showToast({ title: '已删除', icon: 'success' });
    setTimeout(() => uni.navigateBack(), 800);
  } catch {
    uni.showToast({ title: '删除失败', icon: 'error' });
  }
}

function goBack() {
  uni.navigateBack();
}

onLoad((options: any) => {
  if (options?.habitId) {
    loadData(options.habitId);
  }
});
</script>
