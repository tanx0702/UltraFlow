import type { FrequencyType } from '@/api/habit/types';

export interface Habit {
  _id: string;
  userId: string;
  name: string;
  target: string;
  frequency: FrequencyType;
  specificDays?: number[];
  weeklyCount?: number;
  targetDays?: number;
  reminderTime: string;
  icon?: string;
  color?: string;
  status: 'active' | 'paused' | 'completed' | 'archived';
  streak: number;
  bestStreak: number;
  totalCheckIns: number;
  createdAt: string;
  updatedAt: string;
}

export interface DailyTask {
  habitId: string;
  name: string;
  target: string;
  frequency: FrequencyType;
  weeklyCount?: number;
  targetDays?: number;
  reminderTime: string;
  icon?: string;
  color?: string;
  completed: boolean;
  completedAt?: string;
}

export interface HabitState {
  habits: Habit[];
  dailyTasks: DailyTask[];
  todayMotivation: string;
}
