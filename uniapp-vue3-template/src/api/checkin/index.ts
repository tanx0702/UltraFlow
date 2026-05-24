import type { CheckInDateInfo, CheckInReq, CheckInRes, WeeklyStats } from './types';
import { get, post } from '@/utils/request';

/** 打卡 */
export const checkIn = (data: CheckInReq) => post<CheckInRes>('/api/checkins', { data });

/** 获取今日打卡记录 */
export const getTodayCheckIns = () => get<CheckInRes[]>('/api/checkins/today');

/** 获取某月打卡日期 */
export const getCheckInDates = (year: number, month: number) => get<CheckInDateInfo[]>('/api/checkins/dates', { params: { year, month } });

/** 获取本周统计 */
export const getWeekStats = () => get<WeeklyStats>('/api/checkins/week-stats');
