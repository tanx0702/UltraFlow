import { isLogin } from '@/utils/auth';
import { LOGIN_PATH } from '@/router';
import { onShow } from '@dcloudio/uni-app';

/**
 * 页面登录守卫 — 在 onShow 中检查登录状态
 * 用于 tabbar 页面（微信小程序点击原生 tabbar 不触发 switchTab 拦截器）
 */
export function useAuth() {
  onShow(() => {
    if (!isLogin()) {
      const pages = getCurrentPages();
      const currentPage = pages[pages.length - 1];
      const redirectPath = currentPage ? `/${currentPage.route}` : '';
      uni.redirectTo({
        url: `${LOGIN_PATH}?redirect=${encodeURIComponent(redirectPath)}`,
      });
    }
  });
}
