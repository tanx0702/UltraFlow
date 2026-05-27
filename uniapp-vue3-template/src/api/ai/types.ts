export interface SendMessageReq {
  message: string;
  conversationId?: string;
}

import type { FrequencyType } from '../habit/types';

export interface ExtractedHabit {
  action: 'CREATE_HABIT' | 'ADJUST_HABIT' | 'PAUSE_HABIT';
  habitName: string;
  target: string;
  frequency: FrequencyType;
  specificDays: number[] | null;
  weeklyCount: number | null;
  targetDays: number | null;
  reminderTime: string | null;
}

export interface SendMessageRes {
  reply: string;
  conversationId?: string;
  extractedHabit?: ExtractedHabit;
}

export interface ConfirmHabitReq {
  habitName: string;
  target: string;
  frequency: FrequencyType;
  specificDays?: number[] | null;
  weeklyCount?: number | null;
  targetDays?: number | null;
  reminderTime?: string | null;
  force?: boolean;
}
