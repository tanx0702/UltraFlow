/** 频率类型 */
export type FrequencyType = 'daily' | 'weekly' | 'weekly_days' | 'weekly_count' | 'challenge';

/** 习惯 */
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

/** 今日任务 */
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
