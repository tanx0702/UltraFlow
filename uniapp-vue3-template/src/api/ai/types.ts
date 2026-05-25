export interface SendMessageReq {
  message: string;
  conversationId?: string;
}

export interface ExtractedHabit {
  action: 'CREATE_HABIT' | 'ADJUST_HABIT' | 'PAUSE_HABIT';
  habitName: string;
  target: string;
  frequency: 'daily' | 'weekly';
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
  frequency: 'daily' | 'weekly';
  reminderTime?: string | null;
  force?: boolean;
}
