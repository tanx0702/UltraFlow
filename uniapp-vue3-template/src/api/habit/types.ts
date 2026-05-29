export type FrequencyType = 'daily' | 'weekly' | 'weekly_days' | 'weekly_count' | 'challenge';

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

export interface HabitRes {
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
