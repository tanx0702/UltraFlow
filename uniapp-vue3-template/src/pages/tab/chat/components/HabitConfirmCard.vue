<template>
  <view>
    <!-- Unconfirmed card -->
    <view v-if="!confirmed" class="mt-12rpx flex justify-start">
      <view class="max-w-[75%] rounded-xl bg-[#0284C7] p-24rpx">
        <text class="text-28rpx font-bold text-white">{{ actionTitle }}</text>
        <view class="mt-12rpx h-1rpx bg-white/20" />
        <view class="mt-16rpx space-y-12rpx">
          <view class="flex items-center" @tap="$emit('edit', 'habitName', habit.habitName)">
            <text class="w-100rpx text-24rpx text-white/70">名称</text>
            <text class="text-28rpx font-medium text-white">{{ habit.habitName }}</text>
            <text class="ml-8rpx text-20rpx text-white/50">✎</text>
          </view>
          <view class="flex items-center" @tap="$emit('edit', 'target', habit.target)">
            <text class="w-100rpx text-24rpx text-white/70">目标</text>
            <text class="text-28rpx text-white">{{ habit.target }}</text>
            <text class="ml-8rpx text-20rpx text-white/50">✎</text>
          </view>
          <view class="flex items-center" @tap="$emit('editFrequency')">
            <text class="w-100rpx text-24rpx text-white/70">频次</text>
            <text class="text-28rpx text-white">{{ freqLabel }}</text>
            <text class="ml-8rpx text-20rpx text-white/50">✎</text>
          </view>
          <view class="flex items-center" @tap="$emit('editTime', habit.reminderTime)">
            <text class="w-100rpx text-24rpx text-white/70">提醒</text>
            <text class="text-28rpx text-white">{{ habit.reminderTime || '未设置' }}</text>
            <text class="ml-8rpx text-20rpx text-white/50">✎</text>
          </view>
        </view>
        <view class="mt-20rpx flex gap-16rpx">
          <view class="flex-1 rounded-full bg-white px-24rpx py-16rpx text-center" @tap="$emit('confirm')">
            <text class="text-28rpx font-bold text-[#0284C7]">{{ confirmText }}</text>
          </view>
          <view class="flex-1 rounded-full border border-white px-24rpx py-16rpx text-center" @tap="$emit('dismiss')">
            <text class="text-28rpx text-white">暂不需要</text>
          </view>
        </view>
      </view>
    </view>

    <!-- Confirmed badge -->
    <view v-else class="mt-12rpx flex justify-start">
      <view class="rounded-16rpx bg-[#F0FDF4] px-20rpx py-12rpx">
        <text class="text-24rpx text-[#10B981]">{{ confirmedText }} {{ habit.habitName }}</text>
      </view>
    </view>
  </view>
</template>

<script setup lang="ts">
import { computed } from 'vue';
import type { ExtractedHabit } from '@/models/ai.model';

const DAY_LABELS: Record<number, string> = {
  1: '周一', 2: '周二', 3: '周三', 4: '周四',
  5: '周五', 6: '周六', 7: '周日',
};

const props = defineProps<{
  habit: ExtractedHabit;
  confirmed: boolean;
}>();

defineEmits<{
  confirm: [];
  dismiss: [];
  edit: [field: string, value: string];
  editFrequency: [];
  editTime: [time: string | null];
}>();

const actionTitle = computed(() => {
  if (props.habit.action === 'PAUSE_HABIT') return '⏸ 习惯暂停';
  if (props.habit.action === 'ADJUST_HABIT') return '🔄 习惯调整';
  return '📋 新习惯确认';
});

const confirmText = computed(() => {
  if (props.habit.action === 'PAUSE_HABIT') return '确认暂停';
  if (props.habit.action === 'ADJUST_HABIT') return '确认调整';
  return '确认开启';
});

const confirmedText = computed(() => {
  if (props.habit.action === 'PAUSE_HABIT') return '已暂停';
  if (props.habit.action === 'ADJUST_HABIT') return '已调整';
  return '已开启';
});

const freqLabel = computed(() => {
  const h = props.habit;
  switch (h.frequency) {
    case 'daily': return '每天';
    case 'weekly_days':
      if (h.specificDays && h.specificDays.length > 0) {
        return '每周（' + h.specificDays.map(d => DAY_LABELS[d]).join('、') + '）';
      }
      return '每周固定';
    case 'weekly_count': return `每周${h.weeklyCount || '?'}次`;
    case 'challenge': return `坚持${h.targetDays || '?'}天`;
    default: return h.frequency;
  }
});
</script>
