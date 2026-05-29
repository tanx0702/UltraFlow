<template>
  <view class="flex items-center justify-center gap-32rpx py-12rpx">
    <view
      class="h-64rpx w-64rpx flex items-center justify-center rounded-full bg-[#F8FAFC]"
      @tap="decrease"
    >
      <text class="text-36rpx text-[#64748B]">−</text>
    </view>
    <text class="text-40rpx font-bold text-[#1E293B]">{{ modelValue }}</text>
    <view
      class="h-64rpx w-64rpx flex items-center justify-center rounded-full bg-[#F8FAFC]"
      @tap="increase"
    >
      <text class="text-36rpx text-[#64748B]">+</text>
    </view>
    <text v-if="suffix" class="text-24rpx text-[#94A3B8]">{{ suffix }}</text>
  </view>
</template>

<script setup lang="ts">
interface Props {
  modelValue: number;
  min?: number;
  max?: number;
  suffix?: string;
}

const props = withDefaults(defineProps<Props>(), {
  min: 1,
  max: 99,
});

const emit = defineEmits<{
  'update:modelValue': [value: number];
}>();

function decrease() {
  emit('update:modelValue', Math.max(props.min, props.modelValue - 1));
}

function increase() {
  emit('update:modelValue', Math.min(props.max, props.modelValue + 1));
}
</script>
