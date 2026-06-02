<template>
  <view class="flex flex-col h-screen bg-[#F8FAFC]">
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

    <!-- Messages -->
    <scroll-view
      class="flex-1 overflow-hidden"
      scroll-y
      :scroll-into-view="scrollToView"
      scroll-with-animation
      :style="{ paddingBottom: (inputBarHeight + 20) + 'rpx' }"
    >
      <view class="p-24rpx">
        <!-- Welcome -->
        <view v-if="aiStore.messages.length === 0">
          <view class="flex justify-start">
            <view class="max-w-[75%] rounded-2xl rounded-tl-sm bg-[#0EA5E9] px-24rpx py-18rpx">
              <text class="text-28rpx leading-[1.6] text-white">你好！我是极律 AI 教练，有什么想养成的习惯吗？</text>
            </view>
          </view>
          <view class="mt-32rpx flex flex-wrap gap-16rpx">
            <view
              v-for="s in suggestions"
              :key="s"
              class="rounded-full bg-white px-28rpx py-14rpx text-26rpx text-[#0EA5E9] shadow-sm"
              @tap="sendMessage(s)"
            >{{ s }}</view>
          </view>
        </view>

        <!-- Message List -->
        <view v-for="msg in aiStore.messages" :id="`msg-${msg.id}`" :key="msg.id" class="mb-20rpx">
          <MessageBubble :message="msg" />
          <HabitConfirmCard
            v-if="msg.extractedHabit"
            :habit="msg.extractedHabit"
            :confirmed="!!msg.habitConfirmed"
            @confirm="confirmHabit(msg)"
            @dismiss="dismissHabit"
            @edit="(f, v) => startEdit(msg.id, f as 'habitName' | 'target', v)"
            @edit-frequency="startFrequencyEdit(msg.id, msg.extractedHabit!.frequency, msg.extractedHabit!.specificDays, msg.extractedHabit!.weeklyCount, msg.extractedHabit!.targetDays)"
            @edit-time="(t) => startTimeEdit(msg.id, t)"
          />
        </view>

        <!-- Typing -->
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
    <view class="fixed left-0 right-0 z-50 border-t border-[#E2E8F0] bg-white px-24rpx py-16rpx" :style="{ bottom: keyboardHeight + 'px' }">
      <view class="flex h-72rpx items-center justify-between gap-16rpx">
        <view class="h-full flex-1 flex items-center rounded-full bg-[#F8FAFC] px-24rpx">
          <input
            v-model="inputText"
            class="w-full text-28rpx text-[#1E293B]"
            placeholder="告诉教练你的目标..."
            :disabled="aiStore.isTyping"
            :adjust-position="false"
            @confirm="handleSend"
            @blur="onInputBlur"
          />
        </view>
        <view
          class="h-full w-120rpx flex items-center justify-center rounded-full"
          :style="{ backgroundColor: isSendDisabled ? '#CBD5E1' : '#0EA5E9' }"
          @tap="handleSend"
        >
          <text class="text-28rpx font-bold text-white">发送</text>
        </view>
      </view>
    </view>

    <!-- Edit Popup -->

    <EditHabitPopup
      :visible="editState.visible"
      :field="editState.field"
      :value="editState.value"
      :specific-days="editState.specificDays"
      :weekly-count="editState.weeklyCount"
      :target-days="editState.targetDays"
      @cancel="cancelEdit"
      @confirm="confirmEdit"
      @update:value="editState.value = $event"
      @update:weekly-count="editState.weeklyCount = $event"
      @update:target-days="editState.targetDays = $event"
      @toggle-day="toggleDaySelect"
    />

    <!-- Conflict Modal -->
    <ConflictModal
      :visible="conflictState.visible"
      :existing="conflictState.existing"
      :new-habit="conflictState.newHabit"
      @modify="onModifyExisting"
      @create="onCreateNew"
      @cancel="closeConflict"
    />
  </view>
</template>

<script setup lang="ts">
import { useChat } from './composables/useChat';
import MessageBubble from './components/MessageBubble.vue';
import HabitConfirmCard from './components/HabitConfirmCard.vue';
import EditHabitPopup from './components/EditHabitPopup.vue';
import ConflictModal from './components/ConflictModal.vue';
import { useAuth } from '@/composables';

useAuth();

const {
  aiStore,
  inputText,
  scrollToView,
  keyboardHeight,
  inputBarHeight,
  isSendDisabled,
  suggestions,
  handleSend,
  sendMessage,
  onInputBlur,
  confirmHabit,
  dismissHabit,
  conflictState,
  onModifyExisting,
  onCreateNew,
  closeConflict,
  editState,
  startEdit,
  startFrequencyEdit,
  startTimeEdit,
  cancelEdit,
  confirmEdit,
  toggleDaySelect,
} = useChat();
</script>
