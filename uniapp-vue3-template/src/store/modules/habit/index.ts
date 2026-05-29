import type { DailyTask, Habit } from '@/models/habit.model';
import { HabitApi } from '@/api';
import { defineStore } from 'pinia';
import { computed, ref } from 'vue';

const useHabitStore = defineStore('habit', () => {
  const habits = ref<Habit[]>([]);
  const dailyTasks = ref<DailyTask[]>([]);
  const todayMotivation = ref('');

  const activeHabits = computed(() => habits.value.filter(h => h.status === 'active'));
  const pendingTasks = computed(() => dailyTasks.value.filter(t => !t.completed));
  const completedTasks = computed(() => dailyTasks.value.filter(t => t.completed));
  const completionRate = computed(() => {
    if (dailyTasks.value.length === 0) return 0;
    return dailyTasks.value.filter(t => t.completed).length / dailyTasks.value.length;
  });

  async function fetchHabits() {
    habits.value = await HabitApi.getHabits();
  }

  async function fetchTodayHabits() {
    habits.value = await HabitApi.getTodayHabits();
    generateDailyTasks();
  }

  function generateDailyTasks() {
    dailyTasks.value = activeHabits.value.map(habit => ({
      habitId: habit._id,
      name: habit.name,
      target: habit.target,
      frequency: habit.frequency,
      weeklyCount: habit.weeklyCount,
      targetDays: habit.targetDays,
      reminderTime: habit.reminderTime,
      icon: habit.icon,
      color: habit.color,
      completed: false,
    }));
  }

  function markTaskCompleted(habitId: string) {
    const task = dailyTasks.value.find(t => t.habitId === habitId);
    if (task) {
      task.completed = true;
      task.completedAt = new Date().toISOString();
    }
  }

  function setTodayMotivation(motivation: string) {
    todayMotivation.value = motivation;
  }

  function addHabit(habit: Habit) {
    habits.value.push(habit);
    generateDailyTasks();
  }

  async function pauseHabit(habitId: string) {
    await HabitApi.pauseHabit(habitId);
    const habit = habits.value.find(h => h._id === habitId);
    if (habit) habit.status = 'paused';
  }

  async function resumeHabit(habitId: string) {
    await HabitApi.resumeHabit(habitId);
    const habit = habits.value.find(h => h._id === habitId);
    if (habit) habit.status = 'active';
  }

  async function deleteHabit(habitId: string) {
    await HabitApi.deleteHabit(habitId);
    habits.value = habits.value.filter(h => h._id !== habitId);
    generateDailyTasks();
  }

  return {
    habits, dailyTasks, todayMotivation,
    activeHabits, pendingTasks, completedTasks, completionRate,
    fetchHabits, fetchTodayHabits, generateDailyTasks,
    markTaskCompleted, setTodayMotivation, addHabit,
    pauseHabit, resumeHabit, deleteHabit,
  };
}, {
  persist: { pick: ['habits', 'todayMotivation'] },
});

export default useHabitStore;
