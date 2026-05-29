import type { CoachPersona } from '@/models/user.model';

export interface PersonaOption {
  id: CoachPersona;
  name: string;
  icon: string;
  desc: string;
}

export const PERSONA_OPTIONS: PersonaOption[] = [
  { id: 'drill_sergeant', name: '硬核教官', icon: '💂', desc: '毒舌严厉，拒绝拖延，一针见血' },
  { id: 'healing_friend', name: '治愈知己', icon: '💚', desc: '温柔鼓励，情感陪伴与安慰' },
  { id: 'rational_mentor', name: '理性导师', icon: '🧠', desc: '客观逻辑，数据驱动，高效方案' },
];

export const PERSONA_LABELS: Record<CoachPersona, string> = {
  drill_sergeant: '硬核教官',
  healing_friend: '治愈知己',
  rational_mentor: '理性导师',
};

export const PERSONA_DESCRIPTIONS: Record<CoachPersona, string> = {
  drill_sergeant: '毒舌严厉，拒绝拖延，一针见血',
  healing_friend: '温柔鼓励，情感陪伴与安慰',
  rational_mentor: '客观逻辑，数据驱动，高效方案',
};
