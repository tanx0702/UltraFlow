import type { AxiosInstance, AxiosResponse } from 'axios';
import type { IRequestConfig } from './types';
import { useUserStore } from '@/store';
import { clearToken, getToken } from '@/utils/auth';
import { showMessage } from './status';

// 重试队列
let requestQueue: (() => void)[] = [];

// 是否正在刷新 token
let isRefreshing = false;

// 刷新 token 并重试队列中的请求
const refreshToken = async (http: AxiosInstance, config: IRequestConfig) => {
  if (!isRefreshing) {
    isRefreshing = true;
    try {
      await useUserStore().authLogin();
      requestQueue.forEach(cb => cb());
    } finally {
      requestQueue = [];
      isRefreshing = false;
    }
    return http.request(config);
  }

  return new Promise<AxiosResponse>((resolve) => {
    requestQueue.push(() => {
      resolve(http.request(config));
    });
  });
};

export function requestInterceptors(http: AxiosInstance) {
  http.interceptors.request.use(
    (config: IRequestConfig) => {
      config.data = config.data || {};

      const isToken = config?.isToken === false;
      if (getToken() && !isToken && config.headers) {
        config.headers.token = getToken();
      }

      if (config?.loading) {
        uni.showLoading({ title: '加载中', mask: true });
      }

      return config;
    },
    (error: any) => Promise.reject(error),
  );
}

export function responseInterceptors(http: AxiosInstance) {
  http.interceptors.response.use((response: AxiosResponse) => {
    const data = response.data;
    const config = response.config as IRequestConfig;

    if (data.code === 401) {
      return refreshToken(http, config);
    }

    if (config?.loading) {
      uni.hideLoading();
    }

    if (data.code === 0 || data.code === undefined) {
      return response || {};
    }

    if (config?.toast !== false) {
      uni.$u.toast(data.msg);
    }

    return Promise.reject(data);
  }, (error: any) => {
    const config = error.config;

    if (config?.loading !== false) {
      uni.hideLoading();
    }

    if (error.statusCode === 401 || error?.response?.status === 401) {
      clearToken();
      uni.reLaunch({ url: '/pages/common/login/index' });
      return Promise.reject(error);
    }

    if (config?.toast !== false) {
      const message = error.statusCode ? showMessage(error.statusCode) : '网络连接异常,请稍后再试!';
      uni.$u.toast(message);
    }

    return Promise.reject(error);
  });
}
