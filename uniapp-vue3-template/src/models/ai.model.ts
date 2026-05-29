import type { FrequencyType } from './habit.model';

export type HabitAction = 'CREATE_HABIT' | 'ADJUST_HABIT' | 'PAUSE_HABIT';

export interface ExtractedHabit {
  action: HabitAction;
  habitName: string;
  target: string;
  frequency: FrequencyType;
  specificDays: number[] | null;
  weeklyCount: number | null;
  targetDays: number | null;
  reminderTime: string | null;
  icon?: string | null;
  color?: string | null;
}

export interface ChatMessage {
  id: string;
  role: 'user' | 'assistant';
  content: string;
  timestamp: string;
  extractedHabit?: ExtractedHabit;
  habitConfirmed?: boolean;
}
