import type { DailyTask, Habit, HabitState } from './types';
import { HabitApi } from '@/api';
import { defineStore } from 'pinia';

const useHabitStore = defineStore('habit', {
  state: (): HabitState => ({
    habits: [],
    dailyTasks: [],
    todayMotivation: '',
  }),
  getters: {
    activeHabits(state): Habit[] {
      return state.habits.filter(h => h.status === 'active');
    },
    pendingTasks(state): DailyTask[] {
      return state.dailyTasks.filter(t => !t.completed);
    },
    completedTasks(state): DailyTask[] {
      return state.dailyTasks.filter(t => t.completed);
    },
    completionRate(state): number {
      if (state.dailyTasks.length === 0) return 0;
      return state.dailyTasks.filter(t => t.completed).length / state.dailyTasks.length;
    },
  },
  actions: {
    async fetchHabits() {
      const habits = await HabitApi.getHabits();
      this.habits = habits;
    },
    async fetchTodayHabits() {
      const habits = await HabitApi.getTodayHabits();
      this.habits = habits;
      this.generateDailyTasks();
    },
    generateDailyTasks() {
      const today = new Date().toISOString().split('T')[0];
      this.dailyTasks = this.activeHabits.map(habit => ({
        habitId: habit._id,
        name: habit.name,
        target: habit.target,
        reminderTime: habit.reminderTime,
        completed: false,
      }));
    },
    markTaskCompleted(habitId: string) {
      const task = this.dailyTasks.find(t => t.habitId === habitId);
      if (task) {
        task.completed = true;
        task.completedAt = new Date().toISOString();
      }
    },
    setTodayMotivation(motivation: string) {
      this.todayMotivation = motivation;
    },
    addHabit(habit: Habit) {
      this.habits.push(habit);
      this.generateDailyTasks();
    },
    async pauseHabit(habitId: string) {
      await HabitApi.pauseHabit(habitId);
      const habit = this.habits.find(h => h._id === habitId);
      if (habit) habit.status = 'paused';
    },
    async resumeHabit(habitId: string) {
      await HabitApi.resumeHabit(habitId);
      const habit = this.habits.find(h => h._id === habitId);
      if (habit) habit.status = 'active';
    },
    async deleteHabit(habitId: string) {
      await HabitApi.deleteHabit(habitId);
      this.habits = this.habits.filter(h => h._id !== habitId);
      this.generateDailyTasks();
    },
  },
  persist: true,
});

export default useHabitStore;
