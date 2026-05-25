<template>
  <view v-if="visible" class="fixed inset-0 z-999 flex items-end justify-center bg-black/50">
    <!-- 半屏弹窗 -->
    <view class="w-full rounded-t-32rpx bg-white px-48rpx pb-60rpx pt-48rpx" style="padding-bottom: calc(60rpx + env(safe-area-inset-bottom))">
      <!-- 标题 -->
      <view class="flex flex-col items-center">
        <text class="text-36rpx font-bold text-[#1E293B]">完善你的个人资料</text>
        <text class="mt-12rpx text-26rpx text-[#94A3B8]">让 AI 教练更好地认识你</text>
      </view>

      <!-- 头像选择 -->
      <view class="mt-48rpx flex flex-col items-center">
        <button
          class="h-160rpx w-160rpx overflow-hidden rounded-full bg-[#F1F5F9] p-0"
          open-type="chooseAvatar"
          @chooseavatar="onChooseAvatar"
        >
          <image
            v-if="avatarTempPath"
            :src="avatarTempPath"
            mode="aspectFill"
            class="h-full w-full"
          />
          <view v-else class="h-full w-full flex items-center justify-center">
            <text class="i-mdi-camera-plus text-56rpx text-[#94A3B8]" />
          </view>
        </button>
        <text class="mt-12rpx text-22rpx text-[#94A3B8]">点击选择头像</text>
      </view>

      <!-- 昵称输入 -->
      <view class="mt-40rpx">
        <view class="flex h-88rpx items-center rounded-16rpx border-2rpx border-[#E2E8F0] bg-[#F8FAFC] px-24rpx">
          <text class="i-mdi-account text-36rpx text-[#94A3B8]" />
          <input
            type="nickname"
            class="ml-16rpx flex-1 text-28rpx text-[#1E293B]"
            :value="nickname"
            placeholder="请输入昵称"
            maxlength="20"
            @input="onNicknameInput"
          />
        </view>
      </view>

      <!-- 确认按钮 -->
      <view
        class="mt-48rpx flex h-96rpx items-center justify-center rounded-full bg-[#0EA5E9]"
        :class="{ 'opacity-50': saving }"
        @tap="onConfirm"
      >
        <text v-if="saving" class="i-mdi-loading text-36rpx text-white animate-spin" />
        <text v-else class="text-30rpx font-medium text-white">确认并进入极律</text>
      </view>

      <!-- 跳过链接 -->
      <view class="mt-24rpx flex items-center justify-center" @tap="onSkip">
        <text class="text-26rpx text-[#94A3B8]">暂时跳过，使用默认信息</text>
      </view>
    </view>
  </view>
</template>

<script setup lang="ts">
import { ref, watch } from 'vue';
import { getToken } from '@/utils/auth';

const props = defineProps<{
  visible: boolean;
}>();

const emit = defineEmits<{
  confirm: [data: { nickname: string; avatar: string }];
  skip: [];
}>();

const nickname = ref('');
const avatarUrl = ref('');
const avatarTempPath = ref('');
const saving = ref(false);

watch(() => props.visible, (val) => {
  if (val) {
    nickname.value = '';
    avatarUrl.value = '';
    avatarTempPath.value = '';
    saving.value = false;
  }
});

function onChooseAvatar(e: any) {
  avatarTempPath.value = e.detail.avatarUrl || '';
}

function onNicknameInput(e: any) {
  nickname.value = e.detail.value || '';
}

async function uploadAvatar(tempPath: string): Promise<string> {
  const baseURL = import.meta.env.VITE_API_BASE_URL;
  return new Promise((resolve, reject) => {
    uni.uploadFile({
      url: `${baseURL}/api/common/upload`,
      filePath: tempPath,
      name: 'file',
      header: { token: getToken() || '' },
      success: (res) => {
        if (res.statusCode === 200) {
          const data = JSON.parse(res.data);
          resolve(data.url);
        } else {
          reject(new Error('上传失败'));
        }
      },
      fail: () => reject(new Error('上传失败')),
    });
  });
}

async function onConfirm() {
  if (saving.value) return;
  saving.value = true;
  try {
    let permanentUrl = '';
    if (avatarTempPath.value) {
      permanentUrl = await uploadAvatar(avatarTempPath.value);
    }
    emit('confirm', {
      nickname: nickname.value.trim(),
      avatar: permanentUrl,
    });
  } catch {
    uni.showToast({ title: '头像上传失败', icon: 'none' });
    saving.value = false;
  }
}

function onSkip() {
  emit('skip');
}

defineExpose({ saving });
</script>
