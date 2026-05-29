<template>
  <text
    v-if="label"
    class="rounded-full px-12rpx py-2rpx text-20rpx"
    :class="badgeClass"
  >{{ label }}</text>
</template>

<script setup lang="ts">
import { computed } from 'vue';
import type { FrequencyType } from '@/models/habit.model';

interface Props {
  frequency: FrequencyType;
  weeklyCount?: number;
  targetDays?: number;
  specificDays?: number[];
}

const props = defineProps<Props>();

const DAY_LABELS: Record<number, string> = {
  1: '周一', 2: '周二', 3: '周三', 4: '周四',
  5: '周五', 6: '周六', 7: '周日',
};

const label = computed(() => {
  switch (props.frequency) {
    case 'daily':
      return '';
    case 'weekly_days':
      if (props.specificDays && props.specificDays.length > 0) {
        return '每周（' + props.specificDays.map(d => DAY_LABELS[d]).join('、') + '）';
      }
      return '每周固定';
    case 'weekly_count':
      return `每周${props.weeklyCount ?? '?'}次`;
    case 'challenge':
      return `${props.targetDays ?? '?'}天挑战`;
    default:
      return '';
  }
});

const badgeClass = computed(() => {
  switch (props.frequency) {
    case 'weekly_days': return 'bg-[#EFF6FF] text-[#3B82F6]';
    case 'weekly_count': return 'bg-[#F0FDF4] text-[#10B981]';
    case 'challenge': return 'bg-[#FFFBEB] text-[#D97706]';
    default: return '';
  }
});
</script>
