import type { LoginReq, LoginRes, ProfileRes, UpdateCoachPersonaReq, UpdateProfileReq, UpdateReminderReq } from './types';
import { get, post, put } from '@/utils/request';

/** 微信登录 */
export const login = (data: LoginReq) => post<LoginRes>('/api/auth/login', { data, isToken: false });

/** 获取用户信息 */
export const profile = () => get<ProfileRes>('/api/user/profile');

/** 更新教练人设 */
export const updateCoachPersona = (data: UpdateCoachPersonaReq) => put<void>('/api/user/coach-persona', { data });

/** 更新提醒设置 */
export const updateReminder = (data: UpdateReminderReq) => put<void>('/api/user/reminder', { data });

/** 更新用户头像昵称 */
export const updateProfile = (data: UpdateProfileReq) => put<void>('/api/user/profile', { data });

/** 退出登录 */
export const logout = () => post<void>('/api/user/logout');
