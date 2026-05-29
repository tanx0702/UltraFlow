<template>
  <view class="sticky top-0 z-10 bg-[#1E293B] px-32rpx pb-40rpx pt-80rpx">
    <view class="flex items-center justify-between">
      <view>
        <view class="text-26rpx text-[#94A3B8]">{{ todayDate }}</view>
        <view class="mt-8rpx text-40rpx font-bold text-white">今日看板</view>
      </view>
    </view>

    <view class="mt-24rpx flex items-center rounded-20rpx bg-[#334155] p-24rpx">
      <ProgressRing :percentage="percentage" :size="100" />
      <view class="ml-20rpx flex-1">
        <view class="text-24rpx text-[#94A3B8]">{{ motivation }}</view>
        <view class="mt-8rpx flex items-baseline">
          <text class="text-44rpx font-bold text-white">{{ completed }}</text>
          <text class="text-26rpx text-[#94A3B8]">/{{ total }} 项</text>
        </view>
      </view>
    </view>

    <!-- Gradient Progress Bar -->
    <view class="mt-16rpx h-8rpx overflow-hidden rounded-full bg-[#475569]">
      <view
        class="h-full rounded-full transition-all duration-500"
        style="background: linear-gradient(90deg, #10B981, #0EA5E9)"
        :style="{ width: `${percentage}%` }"
      />
    </view>
  </view>
</template>

<script setup lang="ts">
interface Props {
  todayDate: string;
  percentage: number;
  motivation: string;
  completed: number;
  total: number;
}

defineProps<Props>();
</script>
