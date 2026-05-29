export type { ExtractedHabit, ChatMessage as AIMessage } from '@/models/ai.model';

export interface AIState {
  messages: import('@/models/ai.model').ChatMessage[];
  currentExtractedHabit: import('@/models/ai.model').ExtractedHabit | null;
  isTyping: boolean;
}
