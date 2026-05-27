import type { CreateHabitReq, HabitRes, UpdateHabitReq } from './types';
import { del, get, post, put } from '@/utils/request';

/** 获取所有习惯 */
export const getHabits = () => get<HabitRes[]>('/api/habits');

/** 获取单个习惯 */
export const getHabitById = (habitId: string) => get<HabitRes>(`/api/habits/${habitId}`);

/** 获取今日习惯 */
export const getTodayHabits = () => get<HabitRes[]>('/api/habits/today');

/** 创建习惯 */
export const createHabit = (data: CreateHabitReq) => post<HabitRes>('/api/habits', { data });

/** 更新习惯 */
export const updateHabit = (habitId: string, data: UpdateHabitReq) => put<HabitRes>(`/api/habits/${habitId}`, { data });

/** 暂停习惯 */
export const pauseHabit = (habitId: string) => put<void>(`/api/habits/${habitId}/pause`);

/** 恢复习惯 */
export const resumeHabit = (habitId: string) => put<void>(`/api/habits/${habitId}/resume`);

/** 删除习惯 */
export const deleteHabit = (habitId: string) => del<void>(`/api/habits/${habitId}`);
