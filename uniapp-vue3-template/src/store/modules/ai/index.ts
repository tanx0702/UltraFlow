import type { ChatMessage, ExtractedHabit } from '@/models/ai.model';
import { AIApi } from '@/api';
import { defineStore } from 'pinia';
import { computed, ref } from 'vue';

const useAIStore = defineStore('ai', () => {
  const messages = ref<ChatMessage[]>([]);
  const currentExtractedHabit = ref<ExtractedHabit | null>(null);
  const isTyping = ref(false);

  const lastMessage = computed(() => messages.value[messages.value.length - 1]);

  async function sendMessage(content: string) {
    const userMsg: ChatMessage = {
      id: Date.now().toString(),
      role: 'user',
      content,
      timestamp: new Date().toISOString(),
    };
    messages.value.push(userMsg);
    isTyping.value = true;

    try {
      const res = await AIApi.sendMessage({ message: content });
      const aiMsg: ChatMessage = {
        id: (Date.now() + 1).toString(),
        role: 'assistant',
        content: res.reply,
        timestamp: new Date().toISOString(),
        extractedHabit: res.extractedHabit || undefined,
      };
      messages.value.push(aiMsg);

      if (res.extractedHabit) {
        currentExtractedHabit.value = res.extractedHabit;
      }
    } catch {
      const errorMsg: ChatMessage = {
        id: (Date.now() + 1).toString(),
        role: 'assistant',
        content: '抱歉，出了点问题，请稍后再试。',
        timestamp: new Date().toISOString(),
      };
      messages.value.push(errorMsg);
    } finally {
      isTyping.value = false;
    }
  }

  async function confirmHabit(habit: ExtractedHabit, options?: { force?: boolean }) {
    await AIApi.confirmHabit({
      habitName: habit.habitName,
      target: habit.target,
      frequency: habit.frequency,
      specificDays: habit.specificDays,
      weeklyCount: habit.weeklyCount,
      targetDays: habit.targetDays,
      reminderTime: habit.reminderTime,
      icon: habit.icon,
      color: habit.color,
      force: options?.force,
    });

    // 通过替换触发响应式（避免直接 mutate）
    const reversed = [...messages.value].reverse();
    const idx = reversed.findIndex(m => m.role === 'assistant' && m.extractedHabit);
    if (idx !== -1) {
      const realIdx = messages.value.length - 1 - idx;
      messages.value[realIdx] = { ...messages.value[realIdx], habitConfirmed: true };
    }
    currentExtractedHabit.value = null;
  }

  function dismissHabit() {
    currentExtractedHabit.value = null;
  }

  function clearMessages() {
    messages.value = [];
    currentExtractedHabit.value = null;
  }

  return {
    messages, currentExtractedHabit, isTyping, lastMessage,
    sendMessage, confirmHabit, dismissHabit, clearMessages,
  };
}, {
  persist: {
    pick: ['messages'],
    // 只持久化最近 50 条消息
    serializer: {
      serialize: (state: any) => {
        const msgs = state.messages || [];
        return JSON.stringify({ ...state, messages: msgs.slice(-50) });
      },
      deserialize: (str: string) => JSON.parse(str),
    },
  },
});

export default useAIStore;
