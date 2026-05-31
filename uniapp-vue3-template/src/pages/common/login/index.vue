<template>
  <view class="flex h-screen flex-col items-center justify-center bg-[#F8FAFC] px-48rpx">
    <!-- Brand Area -->
    <view class="flex flex-col items-center">
      <!-- Logo -->
      <view class="h-160rpx w-160rpx flex items-center justify-center rounded-32rpx bg-[#1E293B]">
        <text class="i-mdi-lightning-bolt text-80rpx text-[#0EA5E9]" />
      </view>
      <!-- App Name -->
      <view class="mt-32rpx text-56rpx font-bold tracking-[0.2em] text-[#1E293B]">极律</view>
      <!-- Slogan -->
      <view class="mt-16rpx text-26rpx tracking-[0.1em] text-[#94A3B8]">UltraFlow · 让自律进入心流</view>
    </view>

    <!-- CTA Area -->
    <view class="mt-80rpx w-full">
      <!-- WeChat Login Button -->
      <view
        class="flex h-96rpx w-full items-center justify-center rounded-full bg-[#0EA5E9] shadow-md"
        :class="{ 'animate-shake': showWarning }"
        @tap="handleWechatLogin"
      >
        <text class="i-mdi-wechat text-40rpx text-white" />
        <text class="ml-12rpx text-30rpx font-medium text-white">微信一键登录 / 开启自律</text>
      </view>

      <!-- Privacy Agreement -->
      <view class="mt-24rpx flex items-center justify-center py-16rpx" @tap="agreePolicy = !agreePolicy">
        <!-- 💡 这里去掉了动态 style，改用更纯粹、性能更好的 :class 控制闪烁 -->
        <view
          class="h-36rpx w-36rpx flex shrink-0 items-center justify-center rounded-8rpx border-3rpx transition-all duration-200"
          :class="[
            agreePolicy ? 'border-[#0EA5E9] bg-[#0EA5E9]' : 'border-[#94A3B8] bg-[#F1F5F9]',
            { 'animate-warn-blink': showWarning }
          ]"
        >
          <text v-if="agreePolicy" class="i-mdi-check text-28rpx" style="color: white" />
        </view>
        <text class="ml-12rpx text-24rpx text-[#94A3B8]">登录即同意</text>
        <text class="text-24rpx text-[#0EA5E9]">《用户协议》</text>
        <text class="text-24rpx text-[#94A3B8]">与</text>
        <text class="text-24rpx text-[#0EA5E9]">《隐私政策》</text>
      </view>
    </view>

    <!-- 新用户授权弹窗 -->
    <ProfileAuthPopup
      :visible="showProfileAuth"
      @confirm="onProfileConfirm"
      @skip="onProfileSkip"
    />
  </view>
</template>

<script setup lang="ts">
import useUserStore from '@/store/modules/user';
import ProfileAuthPopup from '@/components/ProfileAuthPopup/ProfileAuthPopup.vue';
import { HOME_PATH } from '@/router';
import { ref } from 'vue';

const userStore = useUserStore();
const agreePolicy = ref(false);
const showProfileAuth = ref(false);

// 💡 统一成一个状态控制，当未勾选时，按钮和单选框同步触发动画
const showWarning = ref(false);

function navigateHome() {
  uni.reLaunch({ url: HOME_PATH });
}

function handleWechatLogin() {
  if (!agreePolicy.value) {
    showWarning.value = true;
    setTimeout(() => {
      showWarning.value = false;
    }, 600);

    uni.showToast({ title: '请先同意用户协议', icon: 'none' });
    return;
  }

  uni.showLoading({ title: '登录中...' });

  userStore.authLogin('weixin').then((res: any) => {
    uni.hideLoading();
    if (res?.isNewUser) {
      showProfileAuth.value = true;
    } else {
      uni.showToast({ title: '登录成功', icon: 'success' });
      setTimeout(navigateHome, 800);
    }
  }).catch((err: any) => {
    uni.hideLoading();
    uni.showToast({ title: err?.message || '登录失败', icon: 'error' });
  });
}

async function onProfileConfirm(data: { nickname: string; avatar: string }) {
  try {
    const payload: { nickname?: string; avatar?: string } = {};
    if (data.nickname) payload.nickname = data.nickname;
    if (data.avatar) payload.avatar = data.avatar;
    await userStore.updateProfile(payload);
    uni.showToast({ title: '登录成功', icon: 'success' });
  } catch {
    uni.showToast({ title: '信息保存失败', icon: 'error' });
  }
  showProfileAuth.value = false;
  setTimeout(navigateHome, 800);
}

function onProfileSkip() {
  showProfileAuth.value = false;
  navigateHome();
}
</script>

<style scoped>
/* 按钮晃动动画 */
@keyframes shake {
  0%, 100% { transform: translateX(0); }
  20%, 60% { transform: translateX(-10rpx); }
  40%, 80% { transform: translateX(10rpx); }
}

@keyframes warnBlink {
  0%, 100% { border-color: #94A3B8; transform: scale(1); }
  50% { border-color: #0EA5E9; transform: scale(1.18); border-width: 4rpx; }
}

.animate-shake {
  animation: shake 0.6s ease-in-out;
}

.animate-warn-blink {
  animation: warnBlink 0.6s ease-in-out;
}
</style>