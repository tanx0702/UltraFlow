<template>
  <view class="flex h-screen flex-col bg-[#F8FAFC]">
    <!-- Header -->
    <view class="bg-[#1E293B] px-32rpx pb-24rpx pt-80rpx">
      <view class="flex items-center">
        <view class="h-64rpx w-64rpx flex items-center justify-center rounded-full bg-[#0EA5E9]/20">
          <text class="text-32rpx text-[#0EA5E9]">🤖</text>
        </view>
        <view class="ml-16rpx">
          <view class="text-32rpx font-bold text-white">极律空间</view>
          <view class="text-22rpx text-[#94A3B8]">与AI教练对话，说出你的目标</view>
        </view>
      </view>
    </view>

    <!-- Chat Messages -->
    <scroll-view
      class="flex-1 overflow-hidden"
      scroll-y
      :scroll-into-view="scrollToView"
      scroll-with-animation
    >
      <view class="p-24rpx">
        <!-- Welcome Bubble (when no messages) -->
        <view v-if="aiStore.messages.length === 0">
          <view class="flex justify-start">
            <view class="max-w-[75%] rounded-2xl rounded-tl-sm bg-[#0EA5E9] px-24rpx py-18rpx">
              <text class="text-28rpx leading-[1.6] text-white">你好！我是极律 AI 教练，有什么想养成的习惯吗？</text>
            </view>
          </view>

          <!-- Quick Suggestions -->
          <view class="mt-32rpx flex flex-wrap gap-16rpx">
            <view
              v-for="suggestion in suggestions"
              :key="suggestion"
              class="rounded-full bg-white px-28rpx py-14rpx text-26rpx text-[#0EA5E9] shadow-sm"
              @tap="sendMessage(suggestion)"
            >
              {{ suggestion }}
            </view>
          </view>
        </view>

        <!-- Message List -->
        <view
          v-for="msg in aiStore.messages"
          :id="`msg-${msg.id}`"
          :key="msg.id"
          class="mb-20rpx"
        >
          <!-- User Message -->
          <view v-if="msg.role === 'user'" class="flex justify-end">
            <view class="max-w-[75%] rounded-2xl rounded-tr-sm bg-[#1E293B] px-24rpx py-18rpx">
              <text class="text-28rpx leading-[1.6] text-white">{{ msg.content }}</text>
            </view>
          </view>

          <!-- AI Message -->
          <view v-else>
            <view class="flex justify-start">
              <view class="max-w-[75%] rounded-2xl rounded-tl-sm bg-[#0EA5E9] px-24rpx py-18rpx">
                <text class="text-28rpx leading-[1.6] text-white">{{ msg.content }}</text>
              </view>
            </view>

            <!-- Habit Confirm Card -->
            <view v-if="msg.extractedHabit && !msg.habitConfirmed" class="mt-12rpx flex justify-start">
              <view class="max-w-[75%] rounded-xl bg-[#0284C7] p-24rpx">
                <text class="text-28rpx font-bold text-white">{{ msg.extractedHabit.action === 'PAUSE_HABIT' ? '⏸ 习惯暂停' : msg.extractedHabit.action === 'ADJUST_HABIT' ? '🔄 习惯调整' : '📋 新习惯确认' }}</text>
                <view class="mt-12rpx h-1rpx bg-white/20" />
                <view class="mt-16rpx space-y-12rpx">
                  <view class="flex items-center" @tap="startEdit(msg.id, 'habitName', msg.extractedHabit.habitName)">
                    <text class="w-100rpx text-24rpx text-white/70">名称</text>
                    <text class="text-28rpx font-medium text-white">{{ msg.extractedHabit.habitName }}</text>
                    <text class="ml-8rpx text-20rpx text-white/50">✎</text>
                  </view>
                  <view class="flex items-center" @tap="startEdit(msg.id, 'target', msg.extractedHabit.target)">
                    <text class="w-100rpx text-24rpx text-white/70">目标</text>
                    <text class="text-28rpx text-white">{{ msg.extractedHabit.target }}</text>
                    <text class="ml-8rpx text-20rpx text-white/50">✎</text>
                  </view>
                  <view class="flex items-center" @tap="startFrequencyEdit(msg.id, msg.extractedHabit.frequency)">
                    <text class="w-100rpx text-24rpx text-white/70">频次</text>
                    <text class="text-28rpx text-white">{{ msg.extractedHabit.frequency === 'daily' ? '每天' : '每周' }}</text>
                    <text class="ml-8rpx text-20rpx text-white/50">✎</text>
                  </view>
                  <view class="flex items-center" @tap="startTimeEdit(msg.id, msg.extractedHabit.reminderTime)">
                    <text class="w-100rpx text-24rpx text-white/70">提醒</text>
                    <text class="text-28rpx text-white">{{ msg.extractedHabit.reminderTime || '未设置' }}</text>
                    <text class="ml-8rpx text-20rpx text-white/50">✎</text>
                  </view>
                </view>
                <view class="mt-20rpx flex gap-16rpx">
                  <view
                    class="flex-1 rounded-full bg-white px-24rpx py-16rpx text-center"
                    @tap="confirmHabit(msg)"
                  >
                    <text class="text-28rpx font-bold text-[#0284C7]">{{ msg.extractedHabit.action === 'PAUSE_HABIT' ? '确认暂停' : msg.extractedHabit.action === 'ADJUST_HABIT' ? '确认调整' : '确认开启' }}</text>
                  </view>
                  <view
                    class="flex-1 rounded-full border border-white px-24rpx py-16rpx text-center"
                    @tap="dismissHabit()"
                  >
                    <text class="text-28rpx text-white">暂不需要</text>
                  </view>
                </view>
              </view>
            </view>

            <!-- Confirmed state -->
            <view v-if="msg.extractedHabit && msg.habitConfirmed" class="mt-12rpx flex justify-start">
              <view class="rounded-16rpx bg-[#F0FDF4] px-20rpx py-12rpx">
                <text class="text-24rpx text-[#10B981]">{{ msg.extractedHabit.action === 'PAUSE_HABIT' ? '已暂停' : msg.extractedHabit.action === 'ADJUST_HABIT' ? '已调整' : '已开启' }} {{ msg.extractedHabit.habitName }}</text>
              </view>
            </view>
          </view>
        </view>

        <!-- Typing Indicator -->
        <view v-if="aiStore.isTyping" class="mb-20rpx">
          <view class="flex justify-start">
            <view class="rounded-2xl rounded-tl-sm bg-[#0EA5E9] px-24rpx py-18rpx">
              <view class="flex items-center space-x-8rpx">
                <view class="h-12rpx w-12rpx animate-bounce rounded-full bg-white/80" />
                <view class="h-12rpx w-12rpx animate-bounce rounded-full bg-white/80" style="animation-delay: 0.1s" />
                <view class="h-12rpx w-12rpx animate-bounce rounded-full bg-white/80" style="animation-delay: 0.2s" />
              </view>
            </view>
          </view>
        </view>

        <view id="bottom" />
      </view>
    </scroll-view>

    <!-- Input Bar -->
    <view class="border-t border-[#E2E8F0] bg-white px-24rpx py-16rpx">
      <view class="flex h-72rpx items-center justify-between gap-16rpx">
        <view class="flex-1 h-full rounded-full bg-[#F1F5F9] px-24rpx flex items-center">
          <input
            v-model="inputText"
            class="w-full text-28rpx text-[#1E293B]"
            placeholder="告诉教练你的目标..."
            :disabled="aiStore.isTyping"
            @confirm="handleSend"
          />
        </view>

        <view
          class="w-120rpx h-full flex items-center justify-center rounded-full"
          :style="{ backgroundColor: isSendDisabled ? '#CBD5E1' : '#0EA5E9' }"
          @tap="handleSend"
        >
          <text class="text-28rpx font-bold text-white">发送</text>
        </view>
      </view>
    </view>

    <!-- Edit Habit Popup -->
    <view v-if="editingMsgId" class="fixed inset-0 z-999 flex items-end justify-center bg-black/50" @tap="cancelEdit">
      <view class="w-full rounded-t-32rpx bg-white px-40rpx pb-60rpx pt-32rpx" style="padding-bottom: calc(60rpx + env(safe-area-inset-bottom))" @tap.stop>
        <view class="mb-24rpx text-30rpx font-bold text-[#1E293B]">
          {{ editingField === 'habitName' ? '修改名称' : editingField === 'target' ? '修改目标' : editingField === 'frequency' ? '修改频次' : '修改提醒时间' }}
        </view>
        <!-- Text input for habitName / target -->
        <input
          v-if="editingField === 'habitName' || editingField === 'target'"
          v-model="editValue"
          class="h-88rpx rounded-16rpx border-2rpx border-[#E2E8F0] bg-[#F8FAFC] px-24rpx text-28rpx text-[#1E293B]"
          :placeholder="editingField === 'habitName' ? '请输入习惯名称' : '请输入目标'"
          maxlength="20"
          focus
        />
        <!-- Frequency picker -->
        <view v-if="editingField === 'frequency'" class="flex gap-16rpx">
          <view
            class="flex-1 rounded-16rpx py-24rpx text-center"
            :style="{ backgroundColor: editValue === 'daily' ? '#0EA5E9' : '#F1F5F9', border: editValue === 'daily' ? '2rpx solid #0EA5E9' : '2rpx solid #E2E8F0' }"
            @tap="editValue = 'daily'"
          >
            <text class="text-28rpx font-medium" :style="{ color: editValue === 'daily' ? 'white' : '#64748B' }">每天</text>
          </view>
          <view
            class="flex-1 rounded-16rpx py-24rpx text-center"
            :style="{ backgroundColor: editValue === 'weekly' ? '#0EA5E9' : '#F1F5F9', border: editValue === 'weekly' ? '2rpx solid #0EA5E9' : '2rpx solid #E2E8F0' }"
            @tap="editValue = 'weekly'"
          >
            <text class="text-28rpx font-medium" :style="{ color: editValue === 'weekly' ? 'white' : '#64748B' }">每周</text>
          </view>
        </view>
        <!-- Time picker -->
        <picker v-if="editingField === 'reminderTime'" mode="time" :value="editValue || '08:00'" @change="onTimePickerChange">
          <view class="flex h-88rpx items-center rounded-16rpx border-2rpx border-[#E2E8F0] bg-[#F8FAFC] px-24rpx">
            <text class="text-28rpx" :style="{ color: editValue ? '#1E293B' : '#94A3B8' }">{{ editValue || '点击选择时间' }}</text>
          </view>
        </picker>
        <!-- Clear reminder button -->
        <view v-if="editingField === 'reminderTime' && editValue" class="mt-16rpx" @tap="editValue = ''">
          <text class="text-24rpx text-[#94A3B8]">清除提醒时间</text>
        </view>
        <!-- Confirm button -->
        <view class="mt-32rpx flex h-88rpx items-center justify-center rounded-full bg-[#0EA5E9]" @tap="confirmEdit">
          <text class="text-30rpx font-medium text-white">确认</text>
        </view>
      </view>
    </view>
  </view>
</template>

<script setup lang="ts">
import type { AIMessage } from '@/store/modules/ai/types';
import useAIStore from '@/store/modules/ai';
import useHabitStore from '@/store/modules/habit';
import { useAuth } from '@/composables';
import { computed, nextTick, ref, watch } from 'vue';

useAuth();
const aiStore = useAIStore();
const habitStore = useHabitStore();

const inputText = ref('');
const scrollToView = ref('');

const isSendDisabled = computed(() => inputText.value.trim() === '' || aiStore.isTyping);

const suggestions = [
  '我想每天早起',
  '帮我制定健身计划',
  '我要开始背单词',
  '每天阅读30分钟',
];

function scrollToBottom() {
  nextTick(() => {
    scrollToView.value = 'bottom';
  });
}

watch(() => aiStore.messages.length, scrollToBottom);

async function handleSend() {
  if (isSendDisabled.value) return;
  const content = inputText.value.trim();
  inputText.value = '';
  await aiStore.sendMessage(content);
  scrollToBottom();
}

async function sendMessage(content: string) {
  if (!content.trim() || aiStore.isTyping) return;

  inputText.value = '';
  await aiStore.sendMessage(content);
  scrollToBottom();
}

async function confirmHabit(msg: AIMessage) {
  if (msg.extractedHabit) {
    try {
      await aiStore.confirmHabit(msg.extractedHabit);
      await habitStore.fetchHabits();
      uni.showToast({ title: '习惯已创建', icon: 'success' });
      uni.vibrateShort({ type: 'medium' });
    } catch {
      uni.showToast({ title: '创建失败', icon: 'none' });
    }
  }
}

function dismissHabit() {
  aiStore.dismissHabit();
}

// Edit habit fields
const editingMsgId = ref('');
const editingField = ref<'habitName' | 'target' | 'frequency' | 'reminderTime'>('habitName');
const editValue = ref('');

function startEdit(msgId: string, field: 'habitName' | 'target', currentValue: string) {
  editingMsgId.value = msgId;
  editingField.value = field;
  editValue.value = currentValue;
}

function startFrequencyEdit(msgId: string, currentValue: string) {
  editingMsgId.value = msgId;
  editingField.value = 'frequency';
  editValue.value = currentValue;
}

function startTimeEdit(msgId: string, currentValue: string | null) {
  editingMsgId.value = msgId;
  editingField.value = 'reminderTime';
  editValue.value = currentValue || '';
}

function onTimePickerChange(e: any) {
  editValue.value = e.detail.value;
}

function cancelEdit() {
  editingMsgId.value = '';
}

function confirmEdit() {
  const msg = aiStore.messages.find(m => m.id === editingMsgId.value);
  if (msg?.extractedHabit) {
    (msg.extractedHabit as any)[editingField.value] = editValue.value || null;
  }
  editingMsgId.value = '';
}
</script>
