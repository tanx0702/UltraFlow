<template>
  <view class="py-120rpx text-center">
    <text class="text-100rpx">{{ icon }}</text>
    <view class="mt-24rpx text-28rpx text-[#94A3B8]">{{ text }}</view>
    <view v-if="actionText" class="mt-32rpx flex justify-center">
      <view class="rounded-full bg-[#0EA5E9] px-48rpx py-16rpx" @tap="onAction">
        <text class="text-26rpx font-medium text-white">{{ actionText }}</text>
      </view>
    </view>
  </view>
</template>

<script setup lang="ts">
interface Props {
  icon?: string;
  text: string;
  actionText?: string;
  actionUrl?: string;
}

const props = defineProps<Props>();

function onAction() {
  if (props.actionUrl) {
    uni.switchTab({ url: props.actionUrl });
  }
}
</script>
