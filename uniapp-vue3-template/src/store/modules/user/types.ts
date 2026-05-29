export type { CoachPersona, ProviderType as providerType } from '@/models/user.model';

export interface UserState {
  user_id: string;
  user_name: string;
  avatar: string;
  token: string;
  coachPersona: import('@/models/user.model').CoachPersona;
  reminderEnabled: boolean;
  isLoggedIn: boolean;
}
