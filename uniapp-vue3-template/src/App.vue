<script setup lang="ts">
import { mpUpdate } from '@/utils/index';

onLaunch(() => {
  // #ifdef MP-WEIXIN
  mpUpdate();
  // #endif
});
onShow(() => {});
onHide(() => {});
</script>

<style lang="scss">
/* 每个页面公共css */
@import 'uview-plus/index.scss';
@import '@/static/styles/common.scss';
</style>
