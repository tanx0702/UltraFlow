export interface CheckInRecord {
  _id: string;
  habitId: string;
  userId: string;
  checkInDate: string;
  checkInTime: string;
  note?: string;
  createdAt: string;
}

export interface CheckInDateInfo {
  date: string;
  count: number;
  total: number;
}

export interface WeeklyStats {
  totalCheckIns: number;
  totalHabits: number;
  checkInRate: number;
  bestDay: string;
  missedDays: string[];
}

export interface WeekDayStatus {
  date: string;
  dayLabel: string;
  checkInCount: number;
  totalHabits: number;
  completed: boolean;
  isToday: boolean;
}
