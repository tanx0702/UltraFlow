export type { CoachPersona, Gender, ProviderType as providerType } from '@/models/user.model';

export interface UserState {
  user_id: string;
  user_name: string;
  avatar: string;
  gender: import('@/models/user.model').Gender;
  birthday: string;
  token: string;
  coachPersona: import('@/models/user.model').CoachPersona;
  reminderEnabled: boolean;
  isLoggedIn: boolean;
}
