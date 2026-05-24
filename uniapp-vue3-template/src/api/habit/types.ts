export interface CreateHabitReq {
  name: string;
  target: string;
  frequency: 'daily' | 'weekly';
  specificDays?: number[];
  reminderTime: string;
}

export interface UpdateHabitReq {
  name?: string;
  target?: string;
  reminderTime?: string;
}

export interface HabitRes {
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
