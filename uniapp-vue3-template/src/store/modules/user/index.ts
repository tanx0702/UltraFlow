import type { CoachPersona, providerType, UserState } from './types';
import { UserApi } from '@/api';
import { clearToken, setToken } from '@/utils/auth';
import { defineStore } from 'pinia';

const PERSONA_LABELS: Record<CoachPersona, string> = {
  drill_sergeant: '硬核教官',
  healing_friend: '治愈知己',
  rational_mentor: '理性导师',
};

const PERSONA_DESCRIPTIONS: Record<CoachPersona, string> = {
  drill_sergeant: '毒舌严厉，拒绝拖延，一针见血',
  healing_friend: '温柔鼓励，情感陪伴与安慰',
  rational_mentor: '客观逻辑，数据驱动，高效方案',
};

const useUserStore = defineStore('user', {
  state: (): UserState => ({
    user_id: '',
    user_name: '',
    avatar: '',
    token: '',
    coachPersona: 'rational_mentor',
    reminderEnabled: false,
    isLoggedIn: false,
  }),
  getters: {
    coachPersonaName(state): string {
      return PERSONA_LABELS[state.coachPersona] || '理性导师';
    },
    coachPersonaDescription(state): string {
      return PERSONA_DESCRIPTIONS[state.coachPersona] || '';
    },
  },
  actions: {
    setInfo(partial: Partial<UserState>) {
      this.$patch(partial);
    },
    resetInfo() {
      this.$reset();
    },
    async info() {
      const result = await UserApi.profile();
      this.setInfo(result);
    },
    async loginByCode(code: string) {
      const res = await UserApi.login({ code });
      if (res.token) {
        setToken(res.token);
        this.setInfo({
          user_id: res.user._id,
          user_name: res.user.nickname,
          avatar: res.user.avatar,
          token: res.token,
          coachPersona: res.user.coachPersona as CoachPersona,
          reminderEnabled: res.user.reminderEnabled,
          isLoggedIn: true,
        });
      }
      return res;
    },
    authLogin(provider: providerType = 'weixin') {
      return new Promise((resolve, reject) => {
        uni.login({
          provider,
          success: async (result: UniApp.LoginRes) => {
            if (result.code) {
              try {
                const res = await this.loginByCode(result.code);
                resolve(res);
              } catch (error) {
                reject(error);
              }
            } else {
              reject(new Error(result.errMsg));
            }
          },
          fail: (err: any) => {
            reject(err);
          },
        });
      });
    },
    async updateProfile(data: { nickname?: string; avatar?: string }) {
      await UserApi.updateProfile(data);
      if (data.nickname) this.user_name = data.nickname;
      if (data.avatar) this.avatar = data.avatar;
    },
    setPersona(persona: CoachPersona) {
      this.coachPersona = persona;
    },
    toggleReminder() {
      this.reminderEnabled = !this.reminderEnabled;
    },
    async logout() {
      await UserApi.logout();
      this.resetInfo();
      clearToken();
    },
  },
  persist: true,
});

export default useUserStore;
