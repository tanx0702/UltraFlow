import { ref, watch } from 'vue';

/**
 * 防抖函数
 * @param fn 需要防抖的函数
 * @param delay 延迟毫秒数，默认 300
 */
export function useDebounceFn<T extends (...args: any[]) => any>(fn: T, delay = 300) {
  let timer: ReturnType<typeof setTimeout> | null = null;

  const debouncedFn = (...args: Parameters<T>) => {
    if (timer) clearTimeout(timer);
    timer = setTimeout(() => {
      fn(...args);
      timer = null;
    }, delay);
  };

  const cancel = () => {
    if (timer) {
      clearTimeout(timer);
      timer = null;
    }
  };

  return { run: debouncedFn, cancel };
}

/**
 * 防抖响应式值
 * @param value 响应式 ref
 * @param delay 延迟毫秒数，默认 300
 */
export function useDebounce<T>(value: Ref<T>, delay = 300) {
  const debouncedValue = ref<T>(value.value) as Ref<T>;

  watch(value, (newVal) => {
    const timer = setTimeout(() => {
      debouncedValue.value = newVal;
    }, delay);
    return () => clearTimeout(timer);
  });

  return debouncedValue;
}
