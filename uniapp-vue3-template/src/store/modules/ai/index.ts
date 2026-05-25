import type { AIState, AIMessage, ExtractedHabit } from './types';
import { AIApi } from '@/api';
import { defineStore } from 'pinia';

const useAIStore = defineStore('ai', {
  state: (): AIState => ({
    messages: [],
    currentExtractedHabit: null,
    isTyping: false,
  }),
  getters: {
    lastMessage(state): AIMessage | undefined {
      return state.messages[state.messages.length - 1];
    },
  },
  actions: {
    async sendMessage(content: string) {
      const userMsg: AIMessage = {
        id: Date.now().toString(),
        role: 'user',
        content,
        timestamp: new Date().toISOString(),
      };
      this.messages.push(userMsg);
      this.isTyping = true;

      try {
        const res = await AIApi.sendMessage({ message: content });
        const aiMsg: AIMessage = {
          id: (Date.now() + 1).toString(),
          role: 'assistant',
          content: res.reply,
          timestamp: new Date().toISOString(),
          extractedHabit: res.extractedHabit || undefined,
        };
        this.messages.push(aiMsg);

        if (res.extractedHabit) {
          this.currentExtractedHabit = res.extractedHabit;
        }
      } catch (error) {
        const errorMsg: AIMessage = {
          id: (Date.now() + 1).toString(),
          role: 'assistant',
          content: '抱歉，出了点问题，请稍后再试。',
          timestamp: new Date().toISOString(),
        };
        this.messages.push(errorMsg);
      } finally {
        this.isTyping = false;
      }
    },
    async confirmHabit(habit: ExtractedHabit, options?: { force?: boolean }) {
      await AIApi.confirmHabit({
        habitName: habit.habitName,
        target: habit.target,
        frequency: habit.frequency,
        reminderTime: habit.reminderTime,
        force: options?.force,
      });

      const lastAI = [...this.messages].reverse().find(m => m.role === 'assistant' && m.extractedHabit);
      if (lastAI) {
        lastAI.habitConfirmed = true;
      }
      this.currentExtractedHabit = null;
    },
    dismissHabit() {
      this.currentExtractedHabit = null;
    },
    clearMessages() {
      this.messages = [];
      this.currentExtractedHabit = null;
    },
  },
  persist: true,
});

export default useAIStore;
