export interface CommonReq {
  [key: string]: any;
}

export interface CommonRes {
  [key: string]: any;
}

export type UploadRes = string;

export interface SendCodeReq {
  phone: number;
  code: number;
}

export interface SendCodeRes {
  code: number;
}
