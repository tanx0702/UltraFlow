export interface Habit {
  _id: string;
  userId: string;
  name: string;
  target: string;
  frequency: 'daily' | 'weekly';
  specificDays?: number[];
  reminderTime: string;
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
  reminderTime: string;
  completed: boolean;
  completedAt?: string;
}

export interface HabitState {
  habits: Habit[];
  dailyTasks: DailyTask[];
  todayMotivation: string;
}
