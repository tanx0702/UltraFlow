import type { FrequencyType } from '@/models/habit.model';

export type { FrequencyType };
export type { Habit as HabitRes } from '@/models/habit.model';

export interface CreateHabitReq {
  name: string;
  target: string;
  frequency: FrequencyType;
  specificDays?: number[];
  weeklyCount?: number;
  targetDays?: number;
  reminderTime: string;
  icon?: string;
  color?: string;
}

export interface UpdateHabitReq {
  name?: string;
  target?: string;
  frequency?: FrequencyType;
  specificDays?: number[];
  weeklyCount?: number;
  targetDays?: number;
  reminderTime?: string;
  icon?: string;
  color?: string;
}
