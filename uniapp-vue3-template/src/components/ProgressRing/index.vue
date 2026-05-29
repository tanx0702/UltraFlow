<template>
  <view class="relative flex-shrink-0" :style="{ width: size + 'rpx', height: size + 'rpx' }">
    <svg :viewBox="`0 0 ${svgSize} ${svgSize}`" class="h-full w-full -rotate-90">
      <circle
        :cx="center" :cy="center" :r="radius"
        fill="none"
        stroke="#475569"
        :stroke-width="strokeWidth"
      />
      <circle
        :cx="center" :cy="center" :r="radius"
        fill="none"
        :stroke="percentage >= 100 ? '#F59E0B' : 'url(#progressGrad)'"
        :stroke-width="strokeWidth"
        stroke-linecap="round"
        :stroke-dasharray="circumference"
        :stroke-dashoffset="circumference * (1 - percentage / 100)"
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
        :class="percentage >= 100 ? 'text-[#F59E0B]' : 'text-[#10B981]'"
      >{{ percentage }}%</text>
    </view>
  </view>
</template>

<script setup lang="ts">
import { computed } from 'vue';

interface Props {
  percentage: number;
  size?: number;
}

const props = withDefaults(defineProps<Props>(), {
  size: 100,
});

const svgSize = 100;
const center = svgSize / 2;
const radius = 42;
const strokeWidth = 8;
const circumference = 2 * Math.PI * radius;
</script>
