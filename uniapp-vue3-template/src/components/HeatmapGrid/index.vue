<template>
  <view>
    <!-- Month Navigator -->
    <view class="flex items-center justify-between">
      <text class="text-28rpx font-semibold text-[#1E293B]">{{ title }}</text>
      <view class="flex items-center gap-12rpx">
        <view class="h-48rpx w-48rpx flex items-center justify-center" @tap="$emit('prevMonth')">
          <text class="text-28rpx text-[#94A3B8]">&#9664;</text>
        </view>
        <text class="text-24rpx font-medium text-[#64748B]">{{ year }}年{{ month }}月</text>
        <view
          class="h-48rpx w-48rpx flex items-center justify-center"
          :class="isCurrentMonth ? 'opacity-30' : ''"
          @tap="$emit('nextMonth')"
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
        v-for="(cell, idx) in cells"
        :key="idx"
        class="rounded-6rpx"
        :style="{ width: cellSize, height: cellSize, backgroundColor: cell.color, marginBottom: '6rpx', marginRight: idx % 7 === 6 ? '0' : '6rpx' }"
        @tap="cell.data ? $emit('cellTap', cell.data) : undefined"
      />
    </view>

    <!-- Legend -->
    <view v-if="legend" class="mt-12rpx flex items-center justify-end">
      <text class="mr-8rpx text-20rpx text-[#94A3B8]">少</text>
      <view class="mr-4rpx h-16rpx w-16rpx rounded-2rpx" style="background-color: #E5E7EB" />
      <view class="mr-4rpx h-16rpx w-16rpx rounded-2rpx" style="background-color: #A7F3D0" />
      <view class="mr-4rpx h-16rpx w-16rpx rounded-2rpx" style="background-color: #6EE7B7" />
      <view class="mr-4rpx h-16rpx w-16rpx rounded-2rpx" style="background-color: #10B981" />
      <view class="mr-8rpx h-16rpx w-16rpx rounded-2rpx" style="background-color: #047857" />
      <text class="text-20rpx text-[#94A3B8]">多</text>
    </view>
    <view v-else class="mt-12rpx flex items-center justify-end">
      <text class="mr-8rpx text-20rpx text-[#94A3B8]">未打卡</text>
      <view class="mr-4rpx h-16rpx w-16rpx rounded-2rpx" style="background-color: #E5E7EB" />
      <view class="mr-16rpx h-16rpx w-16rpx rounded-2rpx" style="background-color: #10B981" />
      <text class="text-20rpx text-[#94A3B8]">已打卡</text>
    </view>
  </view>
</template>

<script setup lang="ts">
export interface HeatmapCell {
  color: string;
  data?: { date: string; count: number; total: number } | null;
}

interface Props {
  title?: string;
  year: number;
  month: number;
  isCurrentMonth: boolean;
  cells: HeatmapCell[];
  legend?: boolean;
}

defineProps<Props>();

defineEmits<{
  prevMonth: [];
  nextMonth: [];
  cellTap: [data: { date: string; count: number; total: number }];
}>();

const weekdays = ['一', '二', '三', '四', '五', '六', '日'];
const cellSize = '86rpx';
</script>
