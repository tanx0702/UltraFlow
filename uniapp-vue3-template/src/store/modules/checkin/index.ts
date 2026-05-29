import type { CheckInState } from './types';
import { CheckInApi } from '@/api';
import { defineStore } from 'pinia';

const useCheckInStore = defineStore('checkin', {
  state: (): CheckInState => ({
    todayCheckIns: [],
    checkInDates: [],
    weeklyStats: null,
    weekDayStatuses: [],
    loading: false,
  }),
  getters: {
    todayCheckedHabitIds(state): string[] {
      return state.todayCheckIns.map(c => c.habitId);
    },
  },
  actions: {
    async checkIn(habitId: string, note?: string) {
      const result = await CheckInApi.checkIn({ habitId, note });
      this.todayCheckIns.push(result);
      return result;
    },
    async fetchTodayCheckIns() {
      this.loading = true;
      try {
        this.todayCheckIns = await CheckInApi.getTodayCheckIns();
      } finally {
        this.loading = false;
      }
    },
    async fetchCheckInDates(year: number, month: number) {
      this.checkInDates = await CheckInApi.getCheckInDates(year, month);
    },
    async fetchWeekStats() {
      this.weeklyStats = await CheckInApi.getWeekStats();
    },
    async fetchWeekDayStatuses() {
      this.weekDayStatuses = await CheckInApi.getWeekDayStatus();
    },
  },
  persist: true,
});

export default useCheckInStore;
