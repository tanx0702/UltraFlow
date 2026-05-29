<template>
  <view v-if="message.role === 'user'" class="flex justify-end">
    <view class="max-w-[75%] rounded-2xl rounded-tr-sm bg-[#1E293B] px-24rpx py-18rpx">
      <text class="text-28rpx leading-[1.6] text-white">{{ message.content }}</text>
    </view>
  </view>
  <view v-else class="flex justify-start">
    <view class="max-w-[75%] rounded-2xl rounded-tl-sm bg-[#0EA5E9] px-24rpx py-18rpx">
      <text class="text-28rpx leading-[1.6] text-white">{{ message.content }}</text>
    </view>
  </view>
</template>

<script setup lang="ts">
import type { ChatMessage } from '@/models/ai.model';

defineProps<{
  message: ChatMessage;
}>();
</script>
