import type { CheckInDateInfo, CheckInReq, CheckInRes, WeekDayStatus, WeeklyStats } from './types';
import { get, post } from '@/utils/request';

/** 打卡 */
export const checkIn = (data: CheckInReq) => post<CheckInRes>('/api/checkins', { data });

/** 获取今日打卡记录 */
export const getTodayCheckIns = () => get<CheckInRes[]>('/api/checkins/today');

/** 获取某月打卡日期 */
export const getCheckInDates = (year: number, month: number) => get<CheckInDateInfo[]>('/api/checkins/dates', { params: { year, month } });

/** 获取单个习惯某月打卡日期 */
export const getHabitCheckInDates = (habitId: string, year: number, month: number) =>
  get<CheckInDateInfo[]>(`/api/checkins/habit/${habitId}`, { params: { year, month } });

/** 获取本周统计 */
export const getWeekStats = () => get<WeeklyStats>('/api/checkins/week-stats');

/** 获取本周每日打卡状态 */
export const getWeekDayStatus = () => get<WeekDayStatus[]>('/api/checkins/week-days');
