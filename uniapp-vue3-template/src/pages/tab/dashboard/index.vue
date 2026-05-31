<template>
  <view class="min-h-screen bg-[#F8FAFC]">
    <!-- Skeleton -->
    <view v-if="loading" class="px-32rpx pt-48rpx">
      <view class="bg-[#1E293B] px-32rpx pb-24rpx pt-48rpx">
        <view class="flex items-center justify-between">
          <view>
            <view class="h-24rpx w-120rpx rounded bg-[#334155]" :style="{ opacity: shimmerOpacity }" />
            <view class="mt-8rpx h-36rpx w-160rpx rounded bg-[#334155]" :style="{ opacity: shimmerOpacity }" />
          </view>
        </view>
        <view class="mt-24rpx flex items-center rounded-20rpx bg-[#334155] p-24rpx">
          <view class="flex-shrink-0 rounded-full bg-[#475569]" style="width: 100rpx; height: 100rpx;" :style="{ opacity: shimmerOpacity }" />
          <view class="ml-20rpx flex-1">
            <view class="h-24rpx w-200rpx rounded bg-[#475569]" :style="{ opacity: shimmerOpacity }" />
            <view class="mt-8rpx h-36rpx w-120rpx rounded bg-[#475569]" :style="{ opacity: shimmerOpacity }" />
          </view>
        </view>
      </view>
      <!-- Skeleton Week Bar -->
      <view class="mt-24rpx flex justify-between px-16rpx">
        <view v-for="i in 7" :key="i" class="flex flex-col items-center">
          <view class="h-64rpx w-64rpx rounded-full bg-[#E2E8F0]" :style="{ opacity: shimmerOpacity }" />
          <view class="mt-8rpx h-20rpx w-32rpx rounded bg-[#E2E8F0]" :style="{ opacity: shimmerOpacity }" />
        </view>
      </view>
      <!-- Skeleton Cards -->
      <view class="mt-32rpx">
        <view v-for="i in 3" :key="i" class="mb-16rpx h-120rpx rounded-20rpx bg-white" :style="{ opacity: shimmerOpacity }" />
      </view>
    </view>

    <!-- Main Content -->
    <view v-else>
      <DashboardHeader
        :today-date="todayDate"
        :percentage="completionPercentage"
        :motivation="smartMotivation"
        :completed="completedCount"
        :total="totalCount"
      />

      <view class="mx-32rpx mt-24rpx">
        <!-- Pending Tasks -->
        <TaskGroup
          v-for="group in groupedTasks"
          :key="group.period"
          :label="group.label"
          :tasks="group.tasks"
          :streak-map="habitStreakMap"
          :on-challenge-progress="challengeProgress"
          @complete="handleComplete"
        />

        <!-- Empty State -->
        <EmptyState
          v-if="totalCount === 0"
          icon="📋"
          text="还没有习惯，去极律空间和 AI 教练聊聊吧"
          action-text="去极律空间"
          action-url="/pages/tab/chat/index"
        />

        <!-- Completed Tasks -->
        <view v-if="habitStore.completedTasks.length > 0" class="mt-8rpx">
          <view class="mb-12rpx text-26rpx font-medium text-[#64748B]">已完成</view>
          <view
            v-for="task in habitStore.completedTasks"
            :key="task.habitId"
            class="mb-12rpx flex items-center rounded-20rpx px-24rpx py-20rpx"
            :style="{ backgroundColor: (task.color || '#10B981') + '1A' }"
            @tap="goToDetail(task.habitId)"
          >
            <view
              class="h-72rpx w-72rpx flex flex-shrink-0 items-center justify-center rounded-full"
              :style="{ backgroundColor: (task.color || '#10B981') + '26' }"
            >
              <text class="text-40rpx">{{ task.icon || '📋' }}</text>
            </view>
            <view class="ml-20rpx flex-1">
              <view class="text-28rpx font-medium text-[#1E293B]">{{ task.name }}</view>
              <view class="mt-2rpx text-22rpx text-[#94A3B8]">{{ task.target }}</view>
            </view>
            <view class="flex flex-col items-end">
              <view
                v-if="habitStreakMap[task.habitId] > 0"
                class="mb-4rpx rounded-full bg-[#FFF7ED] px-10rpx py-2rpx"
              >
                <text class="text-22rpx text-[#F97316]">🔥 {{ habitStreakMap[task.habitId] }}</text>
              </view>
              <text v-if="task.completedAt" class="text-22rpx text-[#94A3B8]">
                {{ formatCheckInTime(task.completedAt) }}
              </text>
            </view>
          </view>
        </view>

        <!-- Celebration -->
        <CelebrationBanner v-if="completionPercentage >= 100 && totalCount > 0" />

        <view class="h-40rpx" />
      </view>
    </view>
  </view>
</template>

<script setup lang="ts">
import { useDashboard } from './composables/useDashboard';
import DashboardHeader from './components/DashboardHeader.vue';
import TaskGroup from './components/TaskGroup.vue';
import CelebrationBanner from './components/CelebrationBanner.vue';
import { onShow } from '@dcloudio/uni-app';
import { computed } from 'vue';
import { useAuth } from '@/composables';

useAuth();

const {
  loading,
  shimmerOpacity,
  habitStore,
  completedCount,
  totalCount,
  completionPercentage,
  smartMotivation,
  habitStreakMap,
  groupedTasks,
  challengeProgress,
  loadData,
  handleComplete,
} = useDashboard();

const todayDate = computed(() => {
  const date = new Date();
  const month = date.getMonth() + 1;
  const day = date.getDate();
  const weekDays = ['日', '一', '二', '三', '四', '五', '六'];
  return `${month}月${day}日 周${weekDays[date.getDay()]}`;
});

function formatCheckInTime(isoStr: string): string {
  const d = new Date(isoStr);
  return `${String(d.getHours()).padStart(2, '0')}:${String(d.getMinutes()).padStart(2, '0')}`;
}

function goToDetail(habitId: string) {
  uni.navigateTo({ url: `/pages/common/habit-detail/index?habitId=${habitId}` });
}

onShow(loadData);
</script>
