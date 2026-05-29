import type { HeatmapCell } from '@/components/HeatmapGrid/index.vue';
import useHabitStore from '@/store/modules/habit';
import useCheckInStore from '@/store/modules/checkin';
import { isLogin } from '@/utils/auth';
import { computed, ref, watch } from 'vue';

export function useStats() {
  const habitStore = useHabitStore();
  const checkinStore = useCheckInStore();

  const now = new Date();
  const currentYear = ref(now.getFullYear());
  const currentMonth = ref(now.getMonth() + 1);
  const selectedDay = ref<{ date: string; count: number; total: number } | null>(null);

  const isCurrentMonth = computed(() =>
    currentYear.value === now.getFullYear() && currentMonth.value === now.getMonth() + 1,
  );

  const heatmapDataMap = computed(() =>
    checkinStore.checkInDates.reduce<Record<string, { count: number; total: number }>>((map, d) => {
      map[d.date] = { count: d.count, total: d.total };
      return map;
    }, {}),
  );

  function getHeatmapColor(count: number, total: number): string {
    if (total === 0) return '#E5E7EB';
    const rate = count / total;
    if (rate === 0) return '#E5E7EB';
    if (rate <= 0.25) return '#A7F3D0';
    if (rate <= 0.5) return '#6EE7B7';
    if (rate <= 0.75) return '#10B981';
    return '#047857';
  }

  const gridCells = computed<HeatmapCell[]>(() => {
    const year = currentYear.value;
    const month = currentMonth.value;
    const daysInMonth = new Date(year, month, 0).getDate();
    let firstDayOfWeek = new Date(year, month - 1, 1).getDay();
    firstDayOfWeek = firstDayOfWeek === 0 ? 6 : firstDayOfWeek - 1;

    const cells: HeatmapCell[] = [];

    for (let i = 0; i < firstDayOfWeek; i++) {
      cells.push({ color: 'transparent' });
    }

    for (let d = 1; d <= daysInMonth; d++) {
      const dateStr = `${year}-${String(month).padStart(2, '0')}-${String(d).padStart(2, '0')}`;
      const data = heatmapDataMap.value[dateStr] || null;

      let color: string;
      if (data) {
        color = getHeatmapColor(data.count, data.total);
      } else if (new Date(dateStr) > now) {
        color = '#F1F5F9';
      } else {
        color = '#E5E7EB';
      }

      cells.push({
        color,
        data: data ? { date: dateStr, count: data.count, total: data.total } : null,
      });
    }

    return cells;
  });

  const fullAttendanceRanking = computed(() =>
    habitStore.habits
      .filter(h => h.streak > 0)
      .sort((a, b) => b.streak - a.streak)
      .slice(0, 5),
  );

  const easyBreakRanking = computed(() =>
    habitStore.habits
      .map(h => ({ ...h, breakCount: h.totalCheckIns - h.streak }))
      .filter(h => h.breakCount > 0)
      .sort((a, b) => b.breakCount - a.breakCount)
      .slice(0, 5),
  );

  const weekDateRange = computed(() => {
    const weekStart = new Date(now);
    weekStart.setDate(now.getDate() - now.getDay() + 1);
    const weekEnd = new Date(weekStart);
    weekEnd.setDate(weekStart.getDate() + 6);
    const fmt = (d: Date) => `${d.getMonth() + 1}.${d.getDate()}`;
    return `${fmt(weekStart)} - ${fmt(weekEnd)}`;
  });

  const weeklyReport = computed(() => {
    if (!checkinStore.weeklyStats) return null;
    const s = checkinStore.weeklyStats;
    return {
      dateRange: weekDateRange.value,
      content: `本周打卡率 ${Math.round(s.checkInRate * 100)}%，共 ${s.totalCheckIns} 次打卡`,
      stats: s,
    };
  });

  async function loadData() {
    if (!isLogin()) return;
    try {
      await Promise.all([
        habitStore.fetchHabits(),
        checkinStore.fetchCheckInDates(currentYear.value, currentMonth.value),
        checkinStore.fetchWeekStats(),
      ]);
    } catch (e) {
      console.error('[stats] loadData failed', e);
    }
  }

  function prevMonth() {
    if (currentMonth.value === 1) {
      currentMonth.value = 12;
      currentYear.value--;
    } else {
      currentMonth.value--;
    }
    selectedDay.value = null;
  }

  function nextMonth() {
    if (isCurrentMonth.value) return;
    if (currentMonth.value === 12) {
      currentMonth.value = 1;
      currentYear.value++;
    } else {
      currentMonth.value++;
    }
    selectedDay.value = null;
  }

  watch([currentYear, currentMonth], () => {
    checkinStore.fetchCheckInDates(currentYear.value, currentMonth.value);
  });

  return {
    currentYear,
    currentMonth,
    isCurrentMonth,
    selectedDay,
    gridCells,
    fullAttendanceRanking,
    easyBreakRanking,
    weeklyReport,
    loadData,
    prevMonth,
    nextMonth,
  };
}
