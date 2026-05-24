<template>
  <scroll-view class="min-h-screen bg-[#F8FAFC]" scroll-y>
    <!-- Header -->
    <view class="bg-[#1E293B] px-32rpx pb-32rpx pt-80rpx">
      <view class="text-40rpx font-bold text-white">成长轨迹</view>
      <view class="mt-8rpx text-24rpx text-[#94A3B8]">记录你的每一步成长</view>
    </view>

    <!-- Heatmap Card -->
    <view class="mx-32rpx mt-24rpx rounded-20rpx bg-white p-24rpx shadow-sm">
      <!-- Title + Month Selector -->
      <view class="mb-3 flex items-center justify-between">
        <text class="text-32rpx font-semibold text-[#1E293B]">自律热力图</text>
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
      <view class="mb-8rpx flex">
        <view v-for="wd in weekdays" :key="wd" class="flex-1 text-center">
          <text class="text-20rpx text-[#94A3B8]">{{ wd }}</text>
        </view>
      </view>

      <!-- Heatmap Grid -->
      <view class="flex flex-wrap">
        <view
          v-for="(cell, idx) in gridCells"
          :key="idx"
          class="rounded-6rpx"
          :style="{ width: cellSize, height: cellSize, backgroundColor: cell.color, marginBottom: '6rpx', marginRight: idx % 7 === 6 ? '0' : '6rpx' }"
          @tap="cell.data ? showDetail(cell.data) : undefined"
        />
      </view>

      <!-- Color Legend -->
      <view class="mt-16rpx flex items-center justify-end">
        <text class="mr-8rpx text-20rpx text-[#94A3B8]">少</text>
        <view class="mr-4rpx h-16rpx w-16rpx rounded-2rpx" style="background-color: #E5E7EB" />
        <view class="mr-4rpx h-16rpx w-16rpx rounded-2rpx" style="background-color: #A7F3D0" />
        <view class="mr-4rpx h-16rpx w-16rpx rounded-2rpx" style="background-color: #6EE7B7" />
        <view class="mr-4rpx h-16rpx w-16rpx rounded-2rpx" style="background-color: #10B981" />
        <view class="mr-8rpx h-16rpx w-16rpx rounded-2rpx" style="background-color: #047857" />
        <text class="text-20rpx text-[#94A3B8]">多</text>
      </view>
    </view>

    <!-- Day Detail Popup -->
    <view v-if="selectedDay" class="mx-32rpx mt-16rpx rounded-20rpx bg-white p-32rpx shadow-sm">
      <view class="flex items-center justify-between">
        <text class="text-28rpx font-bold text-[#1E293B]">{{ selectedDay.date }}</text>
        <view @tap="selectedDay = null">
          <text class="text-28rpx text-[#94A3B8]">&#10005;</text>
        </view>
      </view>
      <view class="mt-16rpx flex items-center">
        <text class="text-26rpx text-[#64748B]">打卡 {{ selectedDay.count }} / {{ selectedDay.total }}</text>
        <view
          class="ml-16rpx rounded-full px-16rpx py-4rpx"
          :style="{ backgroundColor: selectedDay.count === selectedDay.total ? '#F0FDF4' : '#FEF2F2' }"
        >
          <text
            class="text-22rpx font-medium"
            :style="{ color: selectedDay.count === selectedDay.total ? '#10B981' : '#EF4444' }"
          >{{ selectedDay.count === selectedDay.total ? '全部完成' : '未全部完成' }}</text>
        </view>
      </view>
    </view>

    <!-- Habit Rankings -->
    <view class="mx-32rpx mt-24rpx flex gap-16rpx">
      <!-- Full Attendance Ranking -->
      <view class="flex-1 rounded-20rpx bg-white p-24rpx shadow-sm">
        <text class="text-26rpx font-bold text-[#10B981]">&#127942; 全勤榜</text>
        <view v-if="fullAttendanceRanking.length > 0" class="mt-12rpx">
          <view v-for="(item, idx) in fullAttendanceRanking" :key="item._id" class="mb-8rpx flex items-center">
            <text class="text-24rpx text-[#1E293B]">{{ idx + 1 }}. {{ item.name }} - {{ item.streak }}天</text>
          </view>
        </view>
        <view v-else class="mt-12rpx">
          <text class="text-24rpx text-[#94A3B8]">暂无数据</text>
        </view>
      </view>

      <!-- Easy to Break Ranking -->
      <view class="flex-1 rounded-20rpx bg-white p-24rpx shadow-sm">
        <text class="text-26rpx font-bold text-[#EF4444]">&#9888;&#65039; 易断卡榜</text>
        <view v-if="easyBreakRanking.length > 0" class="mt-12rpx">
          <view v-for="(item, idx) in easyBreakRanking" :key="item._id" class="mb-8rpx flex items-center">
            <text class="text-24rpx text-[#1E293B]">{{ idx + 1 }}. {{ item.name }} - 断卡{{ item.breakCount }}次</text>
          </view>
        </view>
        <view v-else class="mt-12rpx">
          <text class="text-24rpx text-[#94A3B8]">暂无数据</text>
        </view>
      </view>
    </view>

    <!-- AI Weekly Report -->
    <view class="mx-32rpx mt-24rpx mb-32rpx rounded-20rpx bg-white p-32rpx shadow-sm">
      <view class="flex items-center justify-between">
        <text class="text-28rpx font-bold text-[#1E293B]">&#128202; AI 复盘周报</text>
        <text v-if="weeklyReport" class="text-22rpx text-[#94A3B8]">{{ weeklyReport.dateRange }}</text>
      </view>

      <!-- Has Report -->
      <view v-if="weeklyReport" class="mt-16rpx">
        <text class="text-26rpx leading-[1.8] text-[#475569]">{{ weeklyReport.content }}</text>
        <view class="mt-16rpx h-1rpx bg-[#E2E8F0]" />
        <view class="mt-16rpx flex items-center justify-between">
          <text class="text-22rpx text-[#94A3B8]">打卡率: {{ Math.round(weeklyReport.stats.checkInRate * 100) }}%</text>
          <text class="text-22rpx text-[#94A3B8]">总打卡: {{ weeklyReport.stats.totalCheckIns }}次</text>
          <text class="text-22rpx text-[#94A3B8]">最佳: {{ weeklyReport.stats.bestDay }}</text>
        </view>
      </view>

      <!-- No Report -->
      <view v-else class="mt-24rpx">
        <view
          class="w-full rounded-full py-24rpx text-center"
          :style="{ backgroundColor: '#0EA5E9' }"
          @tap="generateReport"
        >
          <text class="text-28rpx font-bold text-white">&#128202; 生成本周报告</text>
        </view>
      </view>
    </view>
  </scroll-view>
</template>

<script setup lang="ts">
import useHabitStore from '@/store/modules/habit';
import { computed, ref } from 'vue';

const habitStore = useHabitStore();

const now = new Date();
const currentYear = ref(now.getFullYear());
const currentMonth = ref(now.getMonth() + 1);
const selectedDay = ref<{ date: string; count: number; total: number } | null>(null);

const weekdays = ['一', '二', '三', '四', '五', '六', '日'];

const cellSize = computed(() => {
  // 7 columns with gaps: (750rpx - 48rpx*2 padding - 6rpx*6 gaps) / 7 ≈ 87rpx
  return '86rpx';
});

const isCurrentMonth = computed(() => {
  return currentYear.value === now.getFullYear() && currentMonth.value === now.getMonth() + 1;
});

// TODO: 接入真实数据后删除
const mockCheckInDates = [
  { date: '2026-05-01', count: 3, total: 5 },
  { date: '2026-05-02', count: 5, total: 5 },
  { date: '2026-05-03', count: 2, total: 5 },
  { date: '2026-05-04', count: 4, total: 5 },
  { date: '2026-05-05', count: 5, total: 5 },
  { date: '2026-05-06', count: 1, total: 5 },
  { date: '2026-05-07', count: 0, total: 5 },
  { date: '2026-05-08', count: 5, total: 5 },
  { date: '2026-05-09', count: 3, total: 5 },
  { date: '2026-05-10', count: 4, total: 5 },
  { date: '2026-05-11', count: 5, total: 5 },
  { date: '2026-05-12', count: 0, total: 5 },
  { date: '2026-05-13', count: 2, total: 5 },
  { date: '2026-05-14', count: 5, total: 5 },
  { date: '2026-05-15', count: 3, total: 5 },
  { date: '2026-05-16', count: 4, total: 5 },
];

const heatmapDataMap = computed(() => {
  const monthPrefix = `${currentYear.value}-${String(currentMonth.value).padStart(2, '0')}`;
  return mockCheckInDates
    .filter(d => d.date.startsWith(monthPrefix))
    .reduce<Record<string, { count: number; total: number }>>((map, d) => {
      map[d.date] = { count: d.count, total: d.total };
      return map;
    }, {});
});

function getHeatmapColor(count: number, total: number): string {
  if (total === 0) return '#E5E7EB';
  const rate = count / total;
  if (rate === 0) return '#E5E7EB';
  if (rate <= 0.25) return '#A7F3D0';
  if (rate <= 0.5) return '#6EE7B7';
  if (rate <= 0.75) return '#10B981';
  return '#047857';
}

interface GridCell {
  dateStr: string;
  color: string;
  data: { date: string; count: number; total: number } | null;
}

const gridCells = computed<GridCell[]>(() => {
  const year = currentYear.value;
  const month = currentMonth.value;
  const daysInMonth = new Date(year, month, 0).getDate();
  // 0=Sun, 1=Mon, ..., 6=Sat → convert to Mon=0 start
  let firstDayOfWeek = new Date(year, month - 1, 1).getDay();
  firstDayOfWeek = firstDayOfWeek === 0 ? 6 : firstDayOfWeek - 1;

  const cells: GridCell[] = [];

  // Empty leading cells
  for (let i = 0; i < firstDayOfWeek; i++) {
    cells.push({ dateStr: '', color: 'transparent', data: null });
  }

  // Day cells
  for (let d = 1; d <= daysInMonth; d++) {
    const dateStr = `${year}-${String(month).padStart(2, '0')}-${String(d).padStart(2, '0')}`;
    const data = heatmapDataMap.value[dateStr] || null;

    let color: string;
    if (data) {
      color = getHeatmapColor(data.count, data.total);
    } else if (new Date(dateStr) > now) {
      color = '#F1F5F9';
    } else {
      color = '#E5E7EB';
    }

    cells.push({
      dateStr,
      color,
      data: data ? { date: dateStr, count: data.count, total: data.total } : null,
    });
  }

  return cells;
});

function showDetail(data: { date: string; count: number; total: number }) {
  selectedDay.value = data;
}

function prevMonth() {
  if (currentMonth.value === 1) {
    currentMonth.value = 12;
    currentYear.value--;
  } else {
    currentMonth.value--;
  }
  selectedDay.value = null;
}

function nextMonth() {
  if (isCurrentMonth.value) return;
  if (currentMonth.value === 12) {
    currentMonth.value = 1;
    currentYear.value++;
  } else {
    currentMonth.value++;
  }
  selectedDay.value = null;
}

// Habit Rankings
const fullAttendanceRanking = computed(() => {
  return habitStore.habits
    .filter(h => h.streak > 0)
    .sort((a, b) => b.streak - a.streak)
    .slice(0, 5);
});

const easyBreakRanking = computed(() => {
  return habitStore.habits
    .map(h => ({ ...h, breakCount: h.totalCheckIns - h.streak }))
    .filter(h => h.breakCount > 0)
    .sort((a, b) => b.breakCount - a.breakCount)
    .slice(0, 5);
});

// Weekly Report
// TODO: 接入真实数据后删除
const mockWeeklyReport = {
  dateRange: '5.10 - 5.16',
  content: '本周总结：你完成了 85% 的打卡目标，表现优秀！冥想习惯连续打卡 7 天，保持得很好。\n\n建议：跑步习惯连续断卡 2 次，建议调整到早上执行，利用精力最充沛的时段完成。',
  stats: {
    totalCheckIns: 25,
    totalHabits: 5,
    checkInRate: 0.85,
    bestDay: '周三',
    missedDays: ['2026-05-07', '2026-05-12'],
  },
};

const weeklyReport = ref(mockWeeklyReport);

function generateReport() {
  // TODO: 调用 useAIStore.fetchWeeklyReport()
  weeklyReport.value = mockWeeklyReport;
}
</script>
