<template>
  <view v-if="visible" class="fixed inset-0 z-999 flex items-end justify-center bg-black/50" @tap="$emit('cancel')">
    <view class="w-full rounded-t-32rpx bg-white px-40rpx pb-60rpx pt-32rpx" style="padding-bottom: calc(60rpx + env(safe-area-inset-bottom))" @tap.stop>
      <view class="mb-24rpx text-30rpx font-bold text-[#1E293B]">
        {{ title }}
      </view>

      <!-- Text input -->
      <input
        v-if="field === 'habitName' || field === 'target'"
        :value="value"
        class="h-88rpx rounded-16rpx border-2rpx border-[#E2E8F0] bg-[#F8FAFC] px-24rpx text-28rpx text-[#1E293B]"
        :placeholder="field === 'habitName' ? '请输入习惯名称' : '请输入目标'"
        maxlength="20"
        focus
        @input="$emit('update:value', ($event as any).detail.value)"
      />

      <!-- Frequency picker -->
      <view v-if="field === 'frequency'" class="space-y-12rpx">
        <view
          v-for="opt in frequencyOptions"
          :key="opt.value"
          class="rounded-16rpx py-24rpx text-center"
          :style="{ backgroundColor: value === opt.value ? '#0EA5E9' : '#F1F5F9', border: value === opt.value ? '2rpx solid #0EA5E9' : '2rpx solid #E2E8F0' }"
          @tap="$emit('update:value', opt.value)"
        >
          <text class="text-28rpx font-medium" :style="{ color: value === opt.value ? 'white' : '#64748B' }">{{ opt.label }}</text>
        </view>

        <!-- Day of week picker -->
        <view v-if="value === 'weekly_days'" class="flex flex-wrap gap-12rpx pl-16rpx">
          <view
            v-for="day in weekDayOptions"
            :key="day.value"
            class="rounded-12rpx px-20rpx py-14rpx"
            :style="{ backgroundColor: specificDays.includes(day.value) ? '#0EA5E9' : '#F1F5F9', border: specificDays.includes(day.value) ? '2rpx solid #0EA5E9' : '2rpx solid #E2E8F0' }"
            @tap="$emit('toggleDay', day.value)"
          >
            <text class="text-26rpx" :style="{ color: specificDays.includes(day.value) ? 'white' : '#64748B' }">{{ day.label }}</text>
          </view>
        </view>

        <!-- Weekly count stepper -->
        <Stepper
          v-if="value === 'weekly_count'"
          :model-value="weeklyCount"
          :min="1"
          :max="7"
          suffix="次/周"
          @update:model-value="$emit('update:weeklyCount', $event)"
        />

        <!-- Challenge days stepper -->
        <Stepper
          v-if="value === 'challenge'"
          :model-value="targetDays"
          :min="1"
          :max="365"
          suffix="天"
          @update:model-value="$emit('update:targetDays', $event)"
        />
      </view>

      <!-- Time picker -->
      <picker v-if="field === 'reminderTime'" mode="time" :value="value || '08:00'" @change="onTimeChange">
        <view class="flex h-88rpx items-center rounded-16rpx border-2rpx border-[#E2E8F0] bg-[#F8FAFC] px-24rpx">
          <text class="text-28rpx" :style="{ color: value ? '#1E293B' : '#94A3B8' }">{{ value || '点击选择时间' }}</text>
        </view>
      </picker>
      <view v-if="field === 'reminderTime' && value" class="mt-16rpx" @tap="$emit('update:value', '')">
        <text class="text-24rpx text-[#94A3B8]">清除提醒时间</text>
      </view>

      <!-- Confirm -->
      <view class="mt-32rpx flex h-88rpx items-center justify-center rounded-full bg-[#0EA5E9]" @tap="$emit('confirm')">
        <text class="text-30rpx font-medium text-white">确认</text>
      </view>
    </view>
  </view>
</template>

<script setup lang="ts">
import { computed } from 'vue';

interface Props {
  visible: boolean;
  field: 'habitName' | 'target' | 'frequency' | 'reminderTime';
  value: string;
  specificDays: number[];
  weeklyCount: number;
  targetDays: number;
}

const props = defineProps<Props>();

const emit = defineEmits<{
  cancel: [];
  confirm: [];
  'update:value': [val: string];
  'update:weeklyCount': [val: number];
  'update:targetDays': [val: number];
  toggleDay: [day: number];
}>();

const title = computed(() => {
  switch (props.field) {
    case 'habitName': return '修改名称';
    case 'target': return '修改目标';
    case 'frequency': return '修改频次';
    case 'reminderTime': return '修改提醒时间';
    default: return '';
  }
});

const frequencyOptions = [
  { label: '每天', value: 'daily' },
  { label: '每周固定几天', value: 'weekly_days' },
  { label: '每周完成 N 次', value: 'weekly_count' },
  { label: '坚持 N 天挑战', value: 'challenge' },
];

const weekDayOptions = [
  { label: '周一', value: 1 },
  { label: '周二', value: 2 },
  { label: '周三', value: 3 },
  { label: '周四', value: 4 },
  { label: '周五', value: 5 },
  { label: '周六', value: 6 },
  { label: '周日', value: 7 },
];

function onTimeChange(e: any) {
  emit('update:value', e.detail.value);
}
</script>
