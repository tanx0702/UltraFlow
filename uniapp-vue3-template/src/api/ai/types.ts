import type { FrequencyType } from '@/models/habit.model';
import type { ExtractedHabit } from '@/models/ai.model';

export type { ExtractedHabit };

export interface SendMessageReq {
  message: string;
  conversationId?: string;
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
  icon?: string | null;
  color?: string | null;
  force?: boolean;
}
