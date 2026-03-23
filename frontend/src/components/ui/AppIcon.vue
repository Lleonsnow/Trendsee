<script setup lang="ts">
import { computed } from 'vue'
import { Icon } from '@iconify/vue'

type Props = {
  icon: string
  size?: number
  color?: string
}

const props = withDefaults(defineProps<Props>(), {
  size: 24,
})

const iconProps = computed(() => ({
  icon: props.icon,
  width: props.size,
  height: props.size,
  color: props.color,
}))
</script>

<template>
  <Icon v-bind="iconProps" />
</template>

