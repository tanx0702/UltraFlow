<template>
  <view v-if="visible" class="fixed inset-0 z-999 flex items-center justify-center bg-black/50">
    <view class="mx-48rpx w-full rounded-32rpx bg-white px-40rpx py-40rpx">
      <view class="text-center">
        <text class="text-40rpx">⚠️</text>
        <view class="mt-16rpx text-32rpx font-bold text-[#1E293B]">检测到相似习惯</view>
      </view>
      <view class="mt-24rpx rounded-16rpx bg-[#F8FAFC] p-24rpx">
        <text class="text-26rpx text-[#64748B]">你已经有一个「{{ existing?.name }}」习惯</text>
        <view class="mt-8rpx text-28rpx font-medium text-[#1E293B]">当前目标：{{ existing?.target }}</view>
      </view>
      <view class="mt-24rpx text-26rpx text-[#64748B]">你想怎么处理？</view>
      <view
        class="mt-20rpx flex h-88rpx items-center justify-center rounded-full bg-[#0EA5E9]"
        @tap="$emit('modify')"
      >
        <text class="text-28rpx font-medium text-white">修改为 {{ newHabit?.target }}</text>
      </view>
      <view
        class="mt-16rpx flex h-88rpx items-center justify-center rounded-full border-2rpx border-[#0EA5E9]"
        @tap="$emit('create')"
      >
        <text class="text-28rpx font-medium text-[#0EA5E9]">新建一个独立习惯</text>
      </view>
      <view class="mt-16rpx py-12rpx text-center" @tap="$emit('cancel')">
        <text class="text-26rpx text-[#94A3B8]">取消，不做任何操作</text>
      </view>
    </view>
  </view>
</template>

<script setup lang="ts">
import type { ExtractedHabit } from '@/models/ai.model';

defineProps<{
  visible: boolean;
  existing: { _id: string; name: string; target: string } | null;
  newHabit: ExtractedHabit | null;
}>();

defineEmits<{
  modify: [];
  create: [];
  cancel: [];
}>();
</script>
