import type { CoachPersona, ProviderType } from '@/models/user.model';
import { PERSONA_LABELS, PERSONA_DESCRIPTIONS } from '@/constants/persona';
import { UserApi } from '@/api';
import { clearToken, setToken } from '@/utils/auth';
import { defineStore } from 'pinia';
import { computed, ref } from 'vue';

const useUserStore = defineStore('user', () => {
  const user_id = ref('');
  const user_name = ref('');
  const avatar = ref('');
  const token = ref('');
  const coachPersona = ref<CoachPersona>('rational_mentor');
  const reminderEnabled = ref(false);
  const isLoggedIn = ref(false);

  const coachPersonaName = computed(() => PERSONA_LABELS[coachPersona.value] || '理性导师');
  const coachPersonaDescription = computed(() => PERSONA_DESCRIPTIONS[coachPersona.value] || '');

  function setInfo(partial: Record<string, any>) {
    if (partial.user_id !== undefined) user_id.value = partial.user_id;
    if (partial.user_name !== undefined) user_name.value = partial.user_name;
    if (partial.avatar !== undefined) avatar.value = partial.avatar;
    if (partial.token !== undefined) token.value = partial.token;
    if (partial.coachPersona !== undefined) coachPersona.value = partial.coachPersona;
    if (partial.reminderEnabled !== undefined) reminderEnabled.value = partial.reminderEnabled;
    if (partial.isLoggedIn !== undefined) isLoggedIn.value = partial.isLoggedIn;
  }

  function resetInfo() {
    user_id.value = '';
    user_name.value = '';
    avatar.value = '';
    token.value = '';
    coachPersona.value = 'rational_mentor';
    reminderEnabled.value = false;
    isLoggedIn.value = false;
  }

  async function info() {
    const result = await UserApi.profile();
    setInfo(result);
  }

  async function loginByCode(code: string) {
    const res = await UserApi.login({ code });
    if (res.token) {
      setToken(res.token);
      setInfo({
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
  }

  function authLogin(provider: ProviderType = 'weixin') {
    return new Promise((resolve, reject) => {
      uni.login({
        provider,
        success: async (result: UniApp.LoginRes) => {
          if (result.code) {
            try {
              const res = await loginByCode(result.code);
              resolve(res);
            } catch (error) {
              reject(error);
            }
          } else {
            reject(new Error(result.errMsg));
          }
        },
        fail: (err: any) => reject(err),
      });
    });
  }

  async function updateProfile(data: { nickname?: string; avatar?: string }) {
    await UserApi.updateProfile(data);
    if (data.nickname) user_name.value = data.nickname;
    if (data.avatar) avatar.value = data.avatar;
  }

  function setPersona(persona: CoachPersona) {
    coachPersona.value = persona;
  }

  function toggleReminder() {
    reminderEnabled.value = !reminderEnabled.value;
  }

  async function logout() {
    await UserApi.logout();
    resetInfo();
    clearToken();
  }

  return {
    user_id, user_name, avatar, token, coachPersona, reminderEnabled, isLoggedIn,
    coachPersonaName, coachPersonaDescription,
    setInfo, resetInfo, info, loginByCode, authLogin,
    updateProfile, setPersona, toggleReminder, logout,
  };
}, { persist: true });

export default useUserStore;
