export type { CheckInRecord as CheckInRes, CheckInDateInfo, WeeklyStats, WeekDayStatus } from '@/models/checkin.model';

export interface CheckInReq {
  habitId: string;
  note?: string;
}
