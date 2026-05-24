export type CoachPersona = 'drill_sergeant' | 'healing_friend' | 'rational_mentor';

export type providerType =
  | 'weixin'
  | 'qq'
  | 'sinaweibo'
  | 'xiaomi'
  | 'apple'
  | 'univerify'
  | undefined;

export interface UserState {
  user_id: string;
  user_name: string;
  avatar: string;
  token: string;
  coachPersona: CoachPersona;
  reminderEnabled: boolean;
  isLoggedIn: boolean;
}
