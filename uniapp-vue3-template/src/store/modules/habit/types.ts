export type { Habit, DailyTask, FrequencyType } from '@/models/habit.model';

export interface HabitState {
  habits: import('@/models/habit.model').Habit[];
  dailyTasks: import('@/models/habit.model').DailyTask[];
  todayMotivation: string;
}
