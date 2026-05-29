<template>
  <view class="bg-[#1E293B] px-32rpx pb-32rpx pt-80rpx">
    <view class="flex items-center justify-between">
      <view>
        <view v-if="subtitle" class="text-26rpx text-[#94A3B8]">{{ subtitle }}</view>
        <view class="mt-8rpx text-40rpx font-bold text-white">{{ title }}</view>
      </view>
      <slot name="right" />
    </view>
    <slot />
  </view>
</template>

<script setup lang="ts">
interface Props {
  title: string;
  subtitle?: string;
}

defineProps<Props>();
</script>
