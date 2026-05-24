export interface ExtractedHabit {
  action: 'CREATE_HABIT' | 'ADJUST_HABIT' | 'PAUSE_HABIT';
  habitName: string;
  target: string;
  frequency: 'daily' | 'weekly';
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
