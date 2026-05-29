<template>
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
        transform: `translateX(${offset}rpx)`,
        opacity: cardOpacity,
        transition: useTransition ? 'transform 0.3s ease, opacity 0.3s ease' : 'none',
      }"
      @touchstart="onTouchStart"
      @touchmove="onTouchMove"
      @touchend="onTouchEnd"
    >
      <slot />
    </view>
  </view>
</template>

<script setup lang="ts">
import { ref } from 'vue';

const emit = defineEmits<{
  complete: [];
  tap: [];
}>();

const offset = ref(0);
const cardOpacity = ref(1);
const useTransition = ref(false);
const touchStartX = ref(0);
const touchMoved = ref(false);
const SWIPE_THRESHOLD = 160;

function onTouchStart(e: any) {
  touchStartX.value = e.touches[0].clientX;
  useTransition.value = false;
  touchMoved.value = false;
}

function onTouchMove(e: any) {
  touchMoved.value = true;
  const deltaX = (e.touches[0].clientX - touchStartX.value) * 2;
  const clamped = Math.max(0, Math.min(deltaX, 500));
  offset.value = clamped;
  cardOpacity.value = 1 - (clamped / 500) * 0.7;
}

function onTouchEnd() {
  if (!touchMoved.value) {
    emit('tap');
    return;
  }

  if (offset.value > SWIPE_THRESHOLD) {
    useTransition.value = true;
    offset.value = 750;
    cardOpacity.value = 0;
    setTimeout(() => {
      emit('complete');
      offset.value = 0;
      cardOpacity.value = 1;
      useTransition.value = true;
      setTimeout(() => {
        useTransition.value = false;
      }, 300);
    }, 300);
  } else {
    useTransition.value = true;
    offset.value = 0;
    cardOpacity.value = 1;
    setTimeout(() => {
      useTransition.value = false;
    }, 300);
  }
}
</script>
