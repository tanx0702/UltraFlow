export type CoachPersona = 'drill_sergeant' | 'healing_friend' | 'rational_mentor';

export type Gender = 'male' | 'female' | 'private';

export type ProviderType = 'weixin' | 'qq' | 'sinaweibo' | 'xiaomi' | 'apple' | 'univerify' | undefined;

export interface UserProfile {
  _id: string;
  openid: string;
  nickname: string;
  avatar: string;
  gender: Gender;
  birthday: string;
  coachPersona: CoachPersona;
  reminderEnabled: boolean;
  createdAt: string;
  updatedAt: string;
}
