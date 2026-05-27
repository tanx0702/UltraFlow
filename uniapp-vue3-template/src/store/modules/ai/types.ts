import type { FrequencyType } from '@/api/habit/types';

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

export interface AIMessage {
  id: string;
  role: 'user' | 'assistant';
  content: string;
  timestamp: string;
  extractedHabit?: ExtractedHabit;
  habitConfirmed?: boolean;
}

export interface AIState {
  messages: AIMessage[];
  currentExtractedHabit: ExtractedHabit | null;
  isTyping: boolean;
}
