export interface ProfileReq {
  user_id?: string;
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

export interface LoginReq {
  code: string;
}

export interface UserObject {
  _id: string;
  openid: string;
  nickname: string;
  avatar: string;
  coachPersona: string;
  reminderEnabled: boolean;
  createdAt: string;
  updatedAt: string;
}

export interface LoginRes {
  token: string;
  user: UserObject;
  isNewUser: boolean;
}

export interface UpdateCoachPersonaReq {
  coachPersona: string;
}

export interface UpdateReminderReq {
  reminderEnabled: boolean;
}
