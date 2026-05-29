<template>
  <scroll-view class="min-h-screen bg-[#F8FAFC]" scroll-y>
    <!-- Header -->
    <view class="bg-[#1E293B] px-32rpx pb-32rpx pt-80rpx">
      <view class="text-40rpx font-bold text-white">成长轨迹</view>
      <view class="mt-8rpx text-24rpx text-[#94A3B8]">记录你的每一步成长</view>
    </view>

    <!-- Heatmap -->
    <view class="mx-32rpx mt-24rpx rounded-20rpx bg-white p-24rpx shadow-sm">
      <HeatmapGrid
        title="自律热力图"
        :year="currentYear"
        :month="currentMonth"
        :is-current-month="isCurrentMonth"
        :cells="gridCells"
        legend
        @prev-month="prevMonth"
        @next-month="nextMonth"
        @cell-tap="selectedDay = $event"
      />
    </view>

    <!-- Day Detail -->
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

    <!-- Rankings -->
    <view class="mx-32rpx mt-24rpx flex gap-16rpx">
      <view class="flex-1 rounded-20rpx bg-white p-24rpx shadow-sm">
        <text class="text-26rpx font-bold text-[#10B981]">&#127942; 全勤榜</text>
        <view v-if="fullAttendanceRanking.length > 0" class="mt-12rpx">
          <view v-for="(item, idx) in fullAttendanceRanking" :key="item._id" class="mb-8rpx">
            <text class="text-24rpx text-[#1E293B]">{{ idx + 1 }}. {{ item.name }} - {{ item.streak }}天</text>
          </view>
        </view>
        <view v-else class="mt-12rpx">
          <text class="text-24rpx text-[#94A3B8]">暂无数据</text>
        </view>
      </view>
      <view class="flex-1 rounded-20rpx bg-white p-24rpx shadow-sm">
        <text class="text-26rpx font-bold text-[#EF4444]">&#9888;&#65039; 易断卡榜</text>
        <view v-if="easyBreakRanking.length > 0" class="mt-12rpx">
          <view v-for="(item, idx) in easyBreakRanking" :key="item._id" class="mb-8rpx">
            <text class="text-24rpx text-[#1E293B]">{{ idx + 1 }}. {{ item.name }} - 断卡{{ item.breakCount }}次</text>
          </view>
        </view>
        <view v-else class="mt-12rpx">
          <text class="text-24rpx text-[#94A3B8]">暂无数据</text>
        </view>
      </view>
    </view>

    <!-- Weekly Report -->
    <view class="mx-32rpx mt-24rpx mb-32rpx rounded-20rpx bg-white p-32rpx shadow-sm">
      <view class="flex items-center justify-between">
        <text class="text-28rpx font-bold text-[#1E293B]">&#128202; AI 复盘周报</text>
        <text v-if="weeklyReport" class="text-22rpx text-[#94A3B8]">{{ weeklyReport.dateRange }}</text>
      </view>
      <view v-if="weeklyReport" class="mt-16rpx">
        <text class="text-26rpx leading-[1.8] text-[#64748B]">{{ weeklyReport.content }}</text>
        <view class="mt-16rpx h-1rpx bg-[#F8FAFC]" />
        <view class="mt-16rpx flex items-center justify-between">
          <text class="text-22rpx text-[#94A3B8]">打卡率: {{ Math.round(weeklyReport.stats.checkInRate * 100) }}%</text>
          <text class="text-22rpx text-[#94A3B8]">总打卡: {{ weeklyReport.stats.totalCheckIns }}次</text>
          <text class="text-22rpx text-[#94A3B8]">最佳: {{ weeklyReport.stats.bestDay }}</text>
        </view>
      </view>
      <view v-else class="mt-24rpx">
        <text class="text-24rpx text-[#94A3B8]">暂无本周数据</text>
      </view>
    </view>
  </scroll-view>
</template>

<script setup lang="ts">
import { useStats } from './composables/useStats';
import HeatmapGrid from '@/components/HeatmapGrid/index.vue';
import { useAuth } from '@/composables';
import { onShow } from '@dcloudio/uni-app';

useAuth();

const {
  currentYear,
  currentMonth,
  isCurrentMonth,
  selectedDay,
  gridCells,
  fullAttendanceRanking,
  easyBreakRanking,
  weeklyReport,
  loadData,
  prevMonth,
  nextMonth,
} = useStats();

onShow(loadData);
</script>
