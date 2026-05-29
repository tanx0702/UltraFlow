import type { AxiosResponse } from 'axios';
import type { IRequestConfig, IResponse } from './types';
import { createUniAppAxiosAdapter } from '@uni-helper/axios-adapter';
import axios from 'axios';
import { requestInterceptors, responseInterceptors } from './interceptors';

function getBaseURL(): string {
  let baseURL = import.meta.env.VITE_API_BASE_URL;
  // #ifdef H5
  if (import.meta.env.VITE_APP_PROXY === 'true') {
    baseURL = import.meta.env.VITE_API_PREFIX;
  }
  // #endif
  return baseURL;
}

// 单例：只创建一次 axios 实例
const instance = axios.create({
  baseURL: getBaseURL(),
  timeout: 10000,
  headers: {
    'Content-Type': 'application/json;charset=UTF-8',
  },
  adapter: createUniAppAxiosAdapter(),
});

// 拦截器只注册一次
requestInterceptors(instance);
responseInterceptors(instance);

export function request<T = any>(config?: IRequestConfig): Promise<T> {
  return new Promise((resolve, reject) => {
    instance.request(config!).then((res: AxiosResponse<IResponse<T>>) => {
      const { data } = res.data;
      resolve(data != null ? data as T : res.data as T);
    }).catch(reject);
  });
}

export function get<T = any>(url: string, config?: IRequestConfig): Promise<T> {
  return request({ ...config, url, method: 'get' });
}

export function post<T = any>(url: string, config?: IRequestConfig): Promise<T> {
  return request({ ...config, url, method: 'post' });
}

export function put<T = any>(url: string, config?: IRequestConfig): Promise<T> {
  return request({ ...config, url, method: 'put' });
}

export function del<T = any>(url: string, config?: IRequestConfig): Promise<T> {
  return request({ ...config, url, method: 'delete' });
}

const transformFromData = (data: { [key: string]: string }) => {
  const formData = new FormData();
  for (const key in data) {
    data[key] && formData.append(key, data[key]);
  }
  return formData;
};

export function upload<T = any>(url: string, config?: IRequestConfig): Promise<T> {
  if (config?.data) {
    config.data = transformFromData(config?.data);
  }
  return request({
    headers: {
      'Content-Type': 'multipart/form-data;charset=UTF-8',
    },
    ...config,
    url,
    method: 'upload',
  });
}

export function download<T = any>(url: string, config?: IRequestConfig): Promise<T> {
  return request({ ...config, url, method: 'download' });
}
