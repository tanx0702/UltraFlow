import type { DailyTask } from '@/models/habit.model';
import useHabitStore from '@/store/modules/habit';
import useCheckInStore from '@/store/modules/checkin';
import { isLogin } from '@/utils/auth';
import { computed, onUnmounted, ref } from 'vue';

export interface TaskGroup {
  period: string;
  label: string;
  tasks: DailyTask[];
}

export function useDashboard() {
  const habitStore = useHabitStore();
  const checkInStore = useCheckInStore();
  const loading = ref(true);
  const shimmerOpacity = ref(0.3);
  let shimmerInterval: ReturnType<typeof setInterval> | null = null;

  function startShimmer() {
    shimmerInterval = setInterval(() => {
      shimmerOpacity.value = shimmerOpacity.value === 0.3 ? 0.6 : 0.3;
    }, 800);
  }

  function stopShimmer() {
    if (shimmerInterval) {
      clearInterval(shimmerInterval);
      shimmerInterval = null;
    }
  }

  onUnmounted(() => stopShimmer());

  const completedCount = computed(() => habitStore.completedTasks.length);
  const totalCount = computed(() => habitStore.dailyTasks.length);

  const completionPercentage = computed(() => {
    if (totalCount.value === 0) return 0;
    return Math.round((completedCount.value / totalCount.value) * 100);
  });

  const smartMotivation = computed(() => {
    if (habitStore.todayMotivation) return habitStore.todayMotivation;
    if (totalCount.value === 0) return '去创建第一个习惯吧';
    const pct = completionPercentage.value;
    const maxStreak = Math.max(0, ...habitStore.habits.map(h => h.streak));
    if (pct === 0 && maxStreak > 0) return `已连续坚持${maxStreak}天，别断了！`;
    if (pct === 0) return '新的一天，开始行动吧';
    if (pct < 50) return '好的开始是成功的一半';
    if (pct < 100) return '胜利在望，继续加油';
    return '全部完成，太棒了！';
  });

  const habitStreakMap = computed(() => {
    const map: Record<string, number> = {};
    for (const h of habitStore.habits) {
      map[h._id] = h.streak;
    }
    return map;
  });

  const groupedTasks = computed<TaskGroup[]>(() => {
    const groups: Record<string, DailyTask[]> = {
      morning: [],
      afternoon: [],
      evening: [],
      lateNight: [],
    };
    for (const task of habitStore.pendingTasks) {
      const hour = task.reminderTime ? parseInt(task.reminderTime.split(':')[0]) : 18;
      if (hour >= 6 && hour < 12) groups.morning.push(task);
      else if (hour >= 12 && hour < 18) groups.afternoon.push(task);
      else if (hour >= 18) groups.evening.push(task);
      else groups.lateNight.push(task);
    }
    for (const key of Object.keys(groups)) {
      groups[key].sort((a, b) => (a.reminderTime || '').localeCompare(b.reminderTime || ''));
    }
    const order = [
      { period: 'morning', label: '🌅 上午' },
      { period: 'afternoon', label: '🌤️ 下午' },
      { period: 'evening', label: '🌙 晚上' },
      { period: 'lateNight', label: '🌃 深夜' },
    ];
    return order
      .map(o => ({ ...o, tasks: groups[o.period] }))
      .filter(g => g.tasks.length > 0);
  });

  function challengeProgress(task: DailyTask): number {
    if (!task.targetDays) return 0;
    const habit = habitStore.habits.find(h => h._id === task.habitId);
    const streak = habit?.streak ?? 0;
    return Math.min(Math.round((streak / task.targetDays) * 100), 100);
  }

  async function loadData() {
    if (!isLogin()) return;
    loading.value = true;
    startShimmer();
    try {
      await Promise.all([
        habitStore.fetchTodayHabits(),
        checkInStore.fetchTodayCheckIns(),
        checkInStore.fetchWeekDayStatuses(),
      ]);
      const checkedIds = checkInStore.todayCheckedHabitIds;
      for (const task of habitStore.dailyTasks) {
        if (checkedIds.includes(task.habitId)) {
          habitStore.markTaskCompleted(task.habitId);
        }
      }
    } catch (e) {
      console.error('[dashboard] loadData failed', e);
    } finally {
      loading.value = false;
      stopShimmer();
    }
  }

  async function handleComplete(habitId: string) {
    try {
      await checkInStore.checkIn(habitId);
    } catch (e) {
      console.error('[dashboard] checkIn failed', e);
    }
    habitStore.markTaskCompleted(habitId);
    uni.showToast({ title: '打卡成功', icon: 'success', duration: 1000 });
  }

  return {
    loading,
    shimmerOpacity,
    habitStore,
    checkInStore,
    completedCount,
    totalCount,
    completionPercentage,
    smartMotivation,
    habitStreakMap,
    groupedTasks,
    challengeProgress,
    loadData,
    handleComplete,
  };
}
