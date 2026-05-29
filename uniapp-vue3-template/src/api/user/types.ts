import type { CoachPersona } from '@/models/user.model';

export type { CoachPersona };

export interface LoginReq {
  code: string;
}

export interface LoginRes {
  token: string;
  user: {
    _id: string;
    openid: string;
    nickname: string;
    avatar: string;
    coachPersona: string;
    reminderEnabled: boolean;
  };
  isNewUser: boolean;
}

export interface ProfileRes {
  _id: string;
  openid: string;
  nickname: string;
  avatar: string;
  coachPersona: string;
  reminderEnabled: boolean;
  createdAt: string;
  updatedAt: string;
}

export interface UpdateCoachPersonaReq {
  coachPersona: string;
}

export interface UpdateReminderReq {
  reminderEnabled: boolean;
}

export interface UpdateProfileReq {
  nickname?: string;
  avatar?: string;
}
