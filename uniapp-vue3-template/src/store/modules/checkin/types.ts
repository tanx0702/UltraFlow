export type { CheckInRecord, CheckInDateInfo, WeeklyStats, WeekDayStatus } from '@/models/checkin.model';

export interface CheckInState {
  todayCheckIns: import('@/models/checkin.model').CheckInRecord[];
  checkInDates: import('@/models/checkin.model').CheckInDateInfo[];
  weeklyStats: import('@/models/checkin.model').WeeklyStats | null;
  weekDayStatuses: import('@/models/checkin.model').WeekDayStatus[];
  loading: boolean;
}
