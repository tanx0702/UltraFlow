import type { ConfirmHabitReq, SendMessageReq, SendMessageRes } from './types';
import { post } from '@/utils/request';

/** 发送消息给AI */
export const sendMessage = (data: SendMessageReq) => post<SendMessageRes>('/api/ai/chat', { data });

/** 确认创建习惯 */
export const confirmHabit = (data: ConfirmHabitReq) => post<void>('/api/ai/confirm-habit', { data });
