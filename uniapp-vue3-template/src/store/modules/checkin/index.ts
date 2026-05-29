import type { CheckInDateInfo, CheckInRecord, WeekDayStatus, WeeklyStats } from '@/models/checkin.model';
import { CheckInApi } from '@/api';
import { defineStore } from 'pinia';
import { computed, ref } from 'vue';

const useCheckInStore = defineStore('checkin', () => {
  const todayCheckIns = ref<CheckInRecord[]>([]);
  const checkInDates = ref<CheckInDateInfo[]>([]);
  const weeklyStats = ref<WeeklyStats | null>(null);
  const weekDayStatuses = ref<WeekDayStatus[]>([]);
  const loading = ref(false);

  const todayCheckedHabitIds = computed(() => todayCheckIns.value.map(c => c.habitId));

  async function checkIn(habitId: string, note?: string) {
    const result = await CheckInApi.checkIn({ habitId, note });
    todayCheckIns.value.push(result);
    return result;
  }

  async function fetchTodayCheckIns() {
    loading.value = true;
    try {
      todayCheckIns.value = await CheckInApi.getTodayCheckIns();
    } finally {
      loading.value = false;
    }
  }

  async function fetchCheckInDates(year: number, month: number) {
    checkInDates.value = await CheckInApi.getCheckInDates(year, month);
  }

  async function fetchWeekStats() {
    weeklyStats.value = await CheckInApi.getWeekStats();
  }

  async function fetchWeekDayStatuses() {
    weekDayStatuses.value = await CheckInApi.getWeekDayStatus();
  }

  return {
    todayCheckIns, checkInDates, weeklyStats, weekDayStatuses, loading,
    todayCheckedHabitIds,
    checkIn, fetchTodayCheckIns, fetchCheckInDates, fetchWeekStats, fetchWeekDayStatuses,
  };
}, {
  persist: false,
});

export default useCheckInStore;
