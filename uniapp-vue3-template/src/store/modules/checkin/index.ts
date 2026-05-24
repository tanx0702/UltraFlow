import type { CheckInDateInfo, CheckInRecord, CheckInState, WeeklyStats } from './types';
import { CheckInApi } from '@/api';
import { defineStore } from 'pinia';

// TODO: 接入真实数据后删除
const today = new Date();
const todayStr = `${today.getFullYear()}-${String(today.getMonth() + 1).padStart(2, '0')}-${String(today.getDate()).padStart(2, '0')}`;
const mockCheckIns: CheckInRecord[] = [
  {
    _id: 'mock_checkin_1',
    habitId: 'mock_3',
    userId: 'dev_user',
    checkInDate: todayStr,
    checkInTime: `${todayStr}T06:35:00Z`,
    createdAt: `${todayStr}T06:35:00Z`,
  },
];

const useCheckInStore = defineStore('checkin', {
  state: (): CheckInState => ({
    todayCheckIns: mockCheckIns,
    checkInDates: [],
    weeklyStats: null,
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
  },
  persist: true,
});

export default useCheckInStore;
