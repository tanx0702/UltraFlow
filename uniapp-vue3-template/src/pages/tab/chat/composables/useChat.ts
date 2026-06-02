import type { AIMessage } from '@/models/ai.model';
import type { ExtractedHabit } from '@/models/ai.model';
import useAIStore from '@/store/modules/ai';
import useHabitStore from '@/store/modules/habit';
import { HabitApi } from '@/api';
import { computed, nextTick, onUnmounted, reactive, ref, watch } from 'vue';

export function useChat() {
  const aiStore = useAIStore();
  const habitStore = useHabitStore();

  const inputText = ref('');
  const scrollToView = ref('');
  const keyboardHeight = ref(0);
  const inputBarHeight = 104; // py-16rpx*2 + h-72rpx ≈ 32+72=104rpx → ~52px

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

  // ── Keyboard Handling ──
  // onKeyboardHeightChange 比 @focus 的 e.detail.height 更可靠
  // 刘海屏上报的键盘高度包含 SafeArea 底部，需要减去避免输入框过高

  const sysInfo = uni.getSystemInfoSync();
  // onKeyboardHeightChange 上报的高度基于屏幕底部，fixed bottom 基于视口底部
  // 差值 = 状态栏高度 = screenHeight - windowHeight
  const statusBarHeight = sysInfo.screenHeight - sysInfo.windowHeight;
  let debounceTimer: ReturnType<typeof setTimeout> | null = null;

  uni.onKeyboardHeightChange((res) => {
    if (debounceTimer) clearTimeout(debounceTimer);
    debounceTimer = setTimeout(() => {
      const corrected = Math.max(0, res.height - statusBarHeight);
      keyboardHeight.value = corrected;
      if (corrected > 0) {
        setTimeout(() => scrollToBottom(), 150);
      }
    }, 100);
  });

  function onInputBlur() {
    keyboardHeight.value = 0;
    scrollToBottom();
  }

  onUnmounted(() => {
    uni.offKeyboardHeightChange();
    if (debounceTimer) clearTimeout(debounceTimer);
  });

  // ── Confirm Habit ──

  const conflictState = reactive({
    visible: false,
    existing: null as { _id: string; name: string; target: string } | null,
    newHabit: null as ExtractedHabit | null,
  });

  async function confirmHabit(msg: AIMessage) {
    if (!msg.extractedHabit) return;
    try {
      await aiStore.confirmHabit(msg.extractedHabit);
      await habitStore.fetchHabits();
      const isAdjust = msg.extractedHabit.action === 'ADJUST_HABIT';
      uni.showToast({ title: isAdjust ? '已调整' : '已开启', icon: 'success' });
      uni.vibrateShort({ type: 'medium' });
    } catch (err: any) {
      const status = err?.response?.status ?? err?.statusCode;
      const body = err?.response?.data ?? err?.data;
      const existing = body?.data?.existing;
      if (status === 409 && existing) {
        conflictState.existing = existing;
        conflictState.newHabit = msg.extractedHabit;
        conflictState.visible = true;
      } else {
        uni.showToast({ title: '操作失败', icon: 'error' });
      }
    }
  }

  function dismissHabit() {
    aiStore.dismissHabit();
  }

  async function onModifyExisting() {
    if (!conflictState.existing || !conflictState.newHabit) return;
    try {
      await HabitApi.updateHabit(conflictState.existing._id, {
        target: conflictState.newHabit.target,
        reminderTime: conflictState.newHabit.reminderTime || undefined,
      });
      await habitStore.fetchHabits();
      const lastAI = [...aiStore.messages].reverse().find(m => m.role === 'assistant' && m.extractedHabit);
      if (lastAI) lastAI.habitConfirmed = true;
      uni.showToast({ title: `已调整：${conflictState.existing.name}`, icon: 'success' });
    } catch {
      uni.showToast({ title: '调整失败', icon: 'error' });
    }
    closeConflict();
  }

  async function onCreateNew() {
    if (!conflictState.newHabit) return;
    try {
      await aiStore.confirmHabit(conflictState.newHabit, { force: true });
      await habitStore.fetchHabits();
      uni.showToast({ title: '已开启', icon: 'success' });
      uni.vibrateShort({ type: 'medium' });
    } catch {
      uni.showToast({ title: '创建失败', icon: 'error' });
    }
    closeConflict();
  }

  function closeConflict() {
    conflictState.visible = false;
    conflictState.existing = null;
    conflictState.newHabit = null;
  }

  // ── Edit Habit ──

  const editState = reactive({
    visible: false,
    msgId: '',
    field: 'habitName' as 'habitName' | 'target' | 'frequency' | 'reminderTime',
    value: '',
    specificDays: [] as number[],
    weeklyCount: 3,
    targetDays: 21,
  });

  function startEdit(msgId: string, field: 'habitName' | 'target', currentValue: string) {
    editState.msgId = msgId;
    editState.field = field;
    editState.value = currentValue;
    editState.visible = true;
  }

  function startFrequencyEdit(msgId: string, currentValue: string, specificDays: number[] | null | undefined, weeklyCount?: number | null, targetDays?: number | null) {
    editState.msgId = msgId;
    editState.field = 'frequency';
    editState.value = currentValue === 'weekly' ? 'weekly_days' : currentValue;
    editState.specificDays = specificDays && specificDays.length > 0 ? [...specificDays] : [];
    editState.weeklyCount = weeklyCount || 3;
    editState.targetDays = targetDays || 21;
    editState.visible = true;
  }

  function startTimeEdit(msgId: string, currentValue: string | null) {
    editState.msgId = msgId;
    editState.field = 'reminderTime';
    editState.value = currentValue || '';
    editState.visible = true;
  }

  function cancelEdit() {
    editState.visible = false;
  }

  function confirmEdit() {
    const msg = aiStore.messages.find(m => m.id === editState.msgId);
    if (msg?.extractedHabit) {
      const habit = msg.extractedHabit;
      if (editState.field === 'frequency') {
        habit.frequency = editState.value as ExtractedHabit['frequency'];
        if (editState.value === 'weekly_days') {
          habit.specificDays = editState.specificDays.length > 0 ? [...editState.specificDays] : null;
          habit.weeklyCount = null;
          habit.targetDays = null;
        } else if (editState.value === 'weekly_count') {
          habit.specificDays = null;
          habit.weeklyCount = editState.weeklyCount;
          habit.targetDays = null;
        } else if (editState.value === 'challenge') {
          habit.specificDays = null;
          habit.weeklyCount = null;
          habit.targetDays = editState.targetDays;
        } else {
          habit.specificDays = null;
          habit.weeklyCount = null;
          habit.targetDays = null;
        }
      } else {
        if (editState.field === 'habitName') habit.habitName = editState.value || '';
        else if (editState.field === 'target') habit.target = editState.value || '';
        else if (editState.field === 'reminderTime') habit.reminderTime = editState.value || null;
      }
    }
    editState.visible = false;
  }

  function toggleDaySelect(day: number) {
    const idx = editState.specificDays.indexOf(day);
    if (idx >= 0) {
      editState.specificDays.splice(idx, 1);
    } else {
      editState.specificDays.push(day);
    }
  }

  return {
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
  };
}
