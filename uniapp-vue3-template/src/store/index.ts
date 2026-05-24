import type { App } from 'vue';
import { createPinia } from 'pinia';
import { createPersistedState } from 'pinia-plugin-persistedstate';

import useAppStore from './modules/app';
import useUserStore from './modules/user';
import useHabitStore from './modules/habit';
import useAIStore from './modules/ai';
import useCheckInStore from './modules/checkin';

function setupStore(app: App) {
  const store = createPinia();

  const piniaPersist = createPersistedState({
    storage: {
      getItem: uni.getStorageSync,
      setItem: uni.setStorageSync,
    },
  });
  store.use(piniaPersist);

  app.use(store);
}

export { useAppStore, useUserStore, useHabitStore, useAIStore, useCheckInStore };
export default setupStore;
