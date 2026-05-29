<template>
  <view class="mb-24rpx">
    <view class="mb-12rpx flex items-center">
      <text class="text-26rpx font-medium text-[#64748B]">{{ label }}</text>
      <text class="ml-8rpx text-22rpx text-[#94A3B8]">{{ tasks.length }}项</text>
    </view>

    <view v-for="task in tasks" :key="task.habitId" class="mb-12rpx">
      <SwipeCard @tap="goToDetail(task.habitId)" @complete="$emit('complete', task.habitId)">
        <view class="flex w-full items-center">
          <!-- Icon -->
          <view
            class="h-72rpx w-72rpx flex flex-shrink-0 items-center justify-center rounded-full"
            :style="{ backgroundColor: (task.color || '#3B82F6') + '26' }"
          >
            <text class="text-40rpx">{{ task.icon || '📋' }}</text>
          </view>
          <!-- Info -->
          <view class="ml-20rpx flex-1">
            <view class="text-30rpx font-bold text-[#1E293B]">{{ task.name }}</view>
            <view class="mt-4rpx text-24rpx text-[#94A3B8]">{{ task.target }} · {{ task.reminderTime }}</view>
            <FreqBadge
              v-if="task.frequency !== 'daily'"
              :frequency="task.frequency"
              :weekly-count="task.weeklyCount"
              :target-days="task.targetDays"
              class="mt-6rpx"
            />
            <!-- Challenge progress -->
            <view v-if="task.frequency === 'challenge' && task.targetDays" class="mt-6rpx">
              <view class="h-6rpx overflow-hidden rounded-full bg-[#F8FAFC]">
                <view
                  class="h-full rounded-full bg-[#F59E0B]"
                  :style="{ width: onChallengeProgress(task) + '%' }"
                />
              </view>
              <text class="mt-2rpx text-20rpx text-[#94A3B8]">{{ onChallengeProgress(task) }}%</text>
            </view>
          </view>
          <!-- Streak -->
          <view class="ml-8rpx flex flex-col items-center">
            <view
              v-if="streakMap[task.habitId] > 0"
              class="mb-4rpx rounded-full bg-[#FFF7ED] px-10rpx py-2rpx"
            >
              <text class="text-22rpx font-medium text-[#F97316]">🔥 {{ streakMap[task.habitId] }}</text>
            </view>
            <text class="text-28rpx text-[#CBD5E1]">›</text>
          </view>
        </view>
      </SwipeCard>
    </view>
  </view>
</template>

<script setup lang="ts">
import type { DailyTask } from '@/models/habit.model';

interface Props {
  label: string;
  tasks: DailyTask[];
  streakMap: Record<string, number>;
  onChallengeProgress: (task: DailyTask) => number;
}

defineProps<Props>();

defineEmits<{
  complete: [habitId: string];
}>();

function goToDetail(habitId: string) {
  uni.navigateTo({ url: `/pages/common/habit-detail/index?habitId=${habitId}` });
}
</script>
