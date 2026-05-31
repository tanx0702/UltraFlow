<template>
  <scroll-view class="min-h-screen bg-[#F8FAFC]" scroll-y>
    <!-- Header -->
    <view class="bg-[#1E293B] px-32rpx pb-32rpx pt-80rpx">
      <view class="text-40rpx font-bold text-white">教练配置</view>
      <view class="mt-8rpx text-24rpx text-[#94A3B8]">定制你的专属AI教练</view>
    </view>

    <!-- Profile -->
    <view class="mx-32rpx mt-24rpx rounded-20rpx bg-white p-24rpx shadow-sm" @tap="goProfileEdit">
      <view class="flex items-center">
        <view class="h-80rpx w-80rpx flex items-center justify-center overflow-hidden rounded-full bg-[#0EA5E9]/10">
          <image v-if="userStore.avatar" :src="userStore.avatar" mode="aspectFill" class="h-full w-full" />
          <text v-else class="text-40rpx text-[#0EA5E9]">&#128100;</text>
        </view>
        <view class="ml-20rpx flex-1">
          <view class="text-30rpx font-bold text-[#1E293B]">{{ userStore.user_name || '未登录' }}</view>
        </view>
        <text class="text-28rpx text-[#94A3B8]">&#8250;</text>
      </view>
    </view>

    <!-- Habit Management -->
    <view class="mx-32rpx mt-24rpx rounded-20rpx bg-white p-24rpx shadow-sm">
      <view class="mb-16rpx flex items-center justify-between">
        <text class="text-32rpx font-semibold text-[#1E293B]">&#128203; 我的习惯</text>
        <text class="text-22rpx text-[#94A3B8]">共{{ habitStore.habits.length }}个</text>
      </view>

      <view v-if="habitStore.habits.length > 0">
        <view
          v-for="habit in habitStore.habits"
          :key="habit._id"
          class="flex items-center justify-between border-b border-[#E2E8F0] py-20rpx"
          @tap="goToHabitDetail(habit._id)"
          @longpress="handleDeleteHabit(habit._id, habit.name)"
        >
          <view class="flex items-center">
            <text class="text-26rpx text-[#1E293B]">{{ habit.name }}</text>
            <FreqBadge
              :frequency="habit.frequency"
              :weekly-count="habit.weeklyCount"
              :target-days="habit.targetDays"
              :specific-days="habit.specificDays"
              class="ml-12rpx"
            />
          </view>
          <view class="flex items-center">
            <view
              class="rounded-full px-16rpx py-4rpx"
              :style="{ backgroundColor: habit.status === 'active' ? '#F0FDF4' : '#F1F5F9' }"
            >
              <text
                class="text-20rpx"
                :style="{ color: habit.status === 'active' ? '#10B981' : '#64748B' }"
              >{{ habit.status === 'active' ? '活跃' : '暂停' }}</text>
            </view>
            <view class="ml-16rpx" @tap.stop="habit.status === 'active' ? handlePauseHabit(habit._id, habit.name) : handleResumeHabit(habit._id)">
              <text
                class="text-22rpx"
                :style="{ color: habit.status === 'active' ? '#94A3B8' : '#0EA5E9' }"
              >{{ habit.status === 'active' ? '暂停' : '恢复' }}</text>
            </view>
          </view>
        </view>
      </view>
      <view v-else class="py-48rpx text-center">
        <text class="text-26rpx text-[#94A3B8]">暂无习惯，去极律空间创建吧</text>
      </view>
    </view>

    <!-- AI Persona -->
    <view class="mx-32rpx mt-24rpx rounded-20rpx bg-white p-24rpx shadow-sm">
      <view class="mb-20rpx text-32rpx font-semibold text-[#1E293B]">&#129302; 选择你的 AI 教练</view>
      <view
        v-for="persona in personas"
        :key="persona.id"
        class="mb-16rpx flex items-center rounded-16rpx p-20rpx"
        :style="{
          backgroundColor: userStore.coachPersona === persona.id ? '#F0F9FF' : '#F8FAFC',
          border: userStore.coachPersona === persona.id ? '2rpx solid #0EA5E9' : '2rpx solid transparent',
        }"
        @tap="selectPersona(persona.id)"
      >
        <text class="text-48rpx">{{ persona.icon }}</text>
        <view class="ml-20rpx flex-1">
          <view class="text-28rpx font-medium text-[#1E293B]">{{ persona.name }}</view>
          <view class="mt-6rpx text-22rpx text-[#94A3B8]">{{ persona.desc }}</view>
        </view>
        <view
          v-if="userStore.coachPersona === persona.id"
          class="h-40rpx w-40rpx flex items-center justify-center rounded-full bg-[#0EA5E9]"
        >
          <text class="text-22rpx text-white">&#10003;</text>
        </view>
      </view>
    </view>

    <!-- Settings -->
    <view class="mx-32rpx mt-24rpx rounded-20rpx bg-white p-24rpx shadow-sm">
      <view class="mb-16rpx text-32rpx font-semibold text-[#1E293B]">&#9881;&#65039; 系统设置</view>
      <view class="flex items-center justify-between border-b border-[#E2E8F0] py-24rpx">
        <text class="text-26rpx text-[#1E293B]">提醒通知</text>
        <switch :checked="userStore.reminderEnabled" color="#0EA5E9" @change="toggleReminder" />
      </view>
      <view class="flex items-center justify-between border-b border-[#E2E8F0] py-24rpx" @tap="goAbout">
        <text class="text-26rpx text-[#1E293B]">关于极律</text>
        <text class="text-28rpx text-[#94A3B8]">&#8250;</text>
      </view>
      <view class="mt-32rpx rounded-16rpx border border-[#FCA5A5] py-24rpx text-center" @tap="handleLogout">
        <text class="text-26rpx text-[#EF4444]">退出登录</text>
      </view>
    </view>

    <view class="mt-40rpx pb-40rpx text-center">
      <text class="text-22rpx text-[#CBD5E1]">极律 UltraFlow v1.0.0</text>
    </view>
  </scroll-view>
</template>

<script setup lang="ts">
import type { CoachPersona } from '@/models/user.model';
import useUserStore from '@/store/modules/user';
import useHabitStore from '@/store/modules/habit';
import { UserApi } from '@/api';
import { LOGIN_PATH } from '@/router';
import { PERSONA_OPTIONS } from '@/constants/persona';
import { useAuth } from '@/composables';
import { isLogin } from '@/utils/auth';
import { onShow } from '@dcloudio/uni-app';

useAuth();
const userStore = useUserStore();
const habitStore = useHabitStore();

const personas = PERSONA_OPTIONS;

onShow(async () => {
  if (!isLogin()) return;
  try {
    await habitStore.fetchHabits();
  } catch (e) {
    console.error('[coach] fetchHabits failed', e);
  }
});

async function selectPersona(persona: CoachPersona) {
  userStore.setPersona(persona);
  try {
    await UserApi.updateCoachPersona({ coachPersona: persona });
    uni.showToast({ title: `已切换为${userStore.coachPersonaName}`, icon: 'success' });
  } catch {
    uni.showToast({ title: '更新失败', icon: 'error' });
  }
}

async function toggleReminder() {
  userStore.toggleReminder();
  try {
    await UserApi.updateReminder({ reminderEnabled: userStore.reminderEnabled });
  } catch {
    userStore.toggleReminder();
    uni.showToast({ title: '更新失败', icon: 'error' });
  }
}

function handlePauseHabit(habitId: string, habitName: string) {
  uni.showModal({
    title: '暂停习惯',
    content: `确定要暂停「${habitName}」吗？`,
    success: async (res) => {
      if (res.confirm) {
        await habitStore.pauseHabit(habitId);
        uni.showToast({ title: '已暂停', icon: 'success' });
      }
    },
  });
}

async function handleResumeHabit(habitId: string) {
  await habitStore.resumeHabit(habitId);
  uni.showToast({ title: '已恢复', icon: 'success' });
}

function handleDeleteHabit(habitId: string, habitName: string) {
  uni.showModal({
    title: '删除习惯',
    content: `确定要删除「${habitName}」吗？此操作不可恢复。`,
    success: async (res) => {
      if (res.confirm) {
        await habitStore.deleteHabit(habitId);
        uni.showToast({ title: '已删除', icon: 'success' });
      }
    },
  });
}

function goToHabitDetail(habitId: string) {
  uni.navigateTo({ url: `/pages/common/habit-detail/index?habitId=${habitId}` });
}

function goProfileEdit() {
  uni.navigateTo({ url: '/pages/common/profile-edit/index' });
}

function goAbout() {
  uni.showToast({ title: '暂未开放', icon: 'none' });
}

function handleLogout() {
  uni.showModal({
    title: '确认退出',
    content: '退出后需要重新登录',
    success: async (res) => {
      if (res.confirm) {
        await userStore.logout();
        uni.clearStorageSync();
        uni.reLaunch({ url: LOGIN_PATH });
      }
    },
  });
}
</script>
