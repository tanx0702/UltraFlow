<template>
  <view class="min-h-screen bg-[#F8FAFC]">
    <!-- Header -->
    <view class="bg-[#1E293B] pb-64rpx pt-48rpx">
      <!-- Nav bar -->
      <view class="flex items-center justify-between px-32rpx">
        <view class="h-72rpx w-72rpx flex items-center justify-center" @tap="goBack">
          <text class="i-mdi-arrow-left text-40rpx text-white" />
        </view>
        <text class="text-34rpx font-bold text-white">个人信息</text>
        <view class="w-72rpx" />
      </view>

      <!-- Avatar area -->
      <view class="mt-32rpx flex flex-col items-center">
        <button
          class="relative h-192rpx w-192rpx overflow-hidden rounded-full p-0"
          style="background: rgba(255,255,255,0.08)"
          open-type="chooseAvatar"
          @chooseavatar="onChooseAvatar"
        >
          <image
            v-if="avatarPreview"
            :src="avatarPreview"
            mode="aspectFill"
            class="h-full w-full"
          />
          <view v-else class="h-full w-full flex items-center justify-center">
            <view class="h-96rpx w-96rpx flex items-center justify-center rounded-full bg-white/10">
              <text class="i-mdi-account text-48rpx text-white/60" />
            </view>
          </view>
        </button>
        <text class="mt-16rpx text-22rpx text-white/50">点击更换头像</text>
      </view>
    </view>

    <!-- Form section -->
    <view class="mx-28rpx -mt-24rpx rounded-24rpx bg-white shadow-lg overflow-hidden">
      <!-- Section title -->
      <view class="px-32rpx pt-28rpx pb-16rpx">
        <text class="text-24rpx font-medium tracking-wider text-[#94A3B8]">基本资料</text>
      </view>

      <!-- Nickname -->
      <view class="flex items-center justify-between px-32rpx h-104rpx">
        <view class="flex items-center">
          <view class="h-56rpx w-56rpx flex items-center justify-center rounded-16rpx bg-[#0EA5E9]/10">
            <text class="i-mdi-account text-28rpx text-[#0EA5E9]" />
          </view>
          <text class="ml-20rpx text-28rpx text-[#1E293B]">昵称</text>
        </view>
        <view class="flex items-center">
          <input
            ref="nicknameInput"
            type="nickname"
            class="w-280rpx text-right text-28rpx text-[#475569]"
            :value="nickname"
            placeholder="请输入昵称"
            maxlength="20"
            @input="onNicknameInput"
          />
          <text class="i-mdi-chevron-right ml-8rpx text-22rpx text-[#CBD5E1]" />
        </view>
      </view>

      <view class="mx-32rpx border-b border-[#F1F5F9]" />

      <!-- Gender -->
      <view class="flex items-center justify-between px-32rpx h-104rpx" @tap="showGenderPicker">
        <view class="flex items-center">
          <view class="h-56rpx w-56rpx flex items-center justify-center rounded-16rpx bg-[#8B5CF6]/10">
            <text class="i-mdi-gender-male-female text-28rpx text-[#8B5CF6]" />
          </view>
          <text class="ml-20rpx text-28rpx text-[#1E293B]">性别</text>
        </view>
        <view class="flex items-center">
          <text class="text-28rpx" :class="gender === 'private' ? 'text-[#CBD5E1]' : 'text-[#475569]'">{{ genderLabel }}</text>
          <text class="i-mdi-chevron-right ml-8rpx text-22rpx text-[#CBD5E1]" />
        </view>
      </view>

      <view class="mx-32rpx border-b border-[#F1F5F9]" />

      <!-- Birthday -->
      <picker mode="date" :value="birthday" :end="today" @change="onBirthdayChange">
        <view class="flex items-center justify-between px-32rpx h-104rpx">
          <view class="flex items-center">
            <view class="h-56rpx w-56rpx flex items-center justify-center rounded-16rpx bg-[#F59E0B]/10">
              <text class="i-mdi-cake-variant text-28rpx text-[#F59E0B]" />
            </view>
            <text class="ml-20rpx text-28rpx text-[#1E293B]">生日</text>
          </view>
          <view class="flex items-center">
            <text class="text-28rpx" :class="birthday ? 'text-[#475569]' : 'text-[#CBD5E1]'">{{ birthday || '请选择生日' }}</text>
            <text class="i-mdi-chevron-right ml-8rpx text-22rpx text-[#CBD5E1]" />
          </view>
        </view>
      </picker>
    </view>

    <!-- Hint card -->
    <view class="mx-28rpx mt-20rpx rounded-16rpx bg-[#0EA5E9]/5 px-24rpx py-20rpx">
      <view class="flex items-start">
        <text class="i-mdi-information text-24rpx text-[#0EA5E9]" />
        <text class="ml-8rpx flex-1 text-22rpx leading-relaxed text-[#64748B]">完善个人信息有助于 AI 教练根据你的特征定制更合适的习惯方案</text>
      </view>
    </view>

    <!-- Save button -->
    <view class="mx-28rpx mt-40rpx mb-32rpx">
      <view
        class="flex h-100rpx items-center justify-center rounded-24rpx bg-[#0EA5E9]"
        :class="{ 'opacity-50': saving }"
        :style="{ transform: saving ? 'scale(0.98)' : 'scale(1)' }"
        @tap="onSave"
      >
        <text v-if="saving" class="text-30rpx text-white">保存中...</text>
        <text v-else class="text-30rpx font-semibold text-white">保存修改</text>
      </view>
    </view>
  </view>
</template>

<script setup lang="ts">
import { ref } from 'vue';
import type { Gender } from '@/models/user.model';
import useUserStore from '@/store/modules/user';
import { useUpload } from '@/composables';

const userStore = useUserStore();
const { uploadFile } = useUpload();

const nickname = ref(userStore.user_name || '');
const avatarPreview = ref(userStore.avatar || '');
const avatarTempPath = ref('');
const gender = ref<Gender>(userStore.gender || 'private');
const birthday = ref(userStore.birthday || '');
const saving = ref(false);

const today = new Date().toISOString().slice(0, 10);

const genderLabel = ref(getGenderLabel(gender.value));

function getGenderLabel(g: Gender): string {
  const map: Record<Gender, string> = { male: '男', female: '女', private: '保密' };
  return map[g] || '保密';
}

function goBack() {
  uni.navigateBack();
}

function onChooseAvatar(e: any) {
  avatarTempPath.value = e.detail.avatarUrl || '';
  avatarPreview.value = e.detail.avatarUrl || '';
}

function onNicknameInput(e: any) {
  nickname.value = e.detail.value || '';
}

function showGenderPicker() {
  uni.showActionSheet({
    itemList: ['男', '女', '保密'],
    success: (res) => {
      const genders: Gender[] = ['male', 'female', 'private'];
      gender.value = genders[res.tapIndex];
      genderLabel.value = getGenderLabel(gender.value);
    },
  });
}

function onBirthdayChange(e: any) {
  birthday.value = e.detail.value;
}

async function onSave() {
  if (saving.value) return;
  if (!nickname.value.trim()) {
    uni.showToast({ title: '请输入昵称', icon: 'none' });
    return;
  }

  saving.value = true;
  try {
    let avatarUrl = userStore.avatar || '';
    if (avatarTempPath.value) {
      avatarUrl = await uploadFile(avatarTempPath.value);
    }
    await userStore.updateProfile({
      nickname: nickname.value.trim(),
      avatar: avatarUrl,
      gender: gender.value,
      birthday: birthday.value,
    });
    uni.showToast({ title: '保存成功', icon: 'success' });
    setTimeout(() => uni.navigateBack(), 1500);
  } catch {
    uni.showToast({ title: '保存失败', icon: 'error' });
  } finally {
    saving.value = false;
  }
}
</script>
