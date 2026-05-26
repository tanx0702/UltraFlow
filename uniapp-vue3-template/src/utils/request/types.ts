import type { AxiosRequestConfig } from 'axios';

// 返回res.data的interface
export interface IResponse<T = any> {
  code: number;
  data: T | null;
  msg: string;
}

export interface IRequestConfig extends AxiosRequestConfig {
  /**
   * 是否携带token
   */
  isToken?: boolean;
  /**
   * 是否显示loading
   */
  loading?: boolean;
  /**
   * 是否防止重复提交
   */
  repeatSubmit?: boolean;
  /**
   * 是否显示toast
   * @default true
   */
  toast?: boolean;
}
