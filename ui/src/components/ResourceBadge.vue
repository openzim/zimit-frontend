<template>
  <span class="badge badge-light mr-2" :title="tooltip_text">
    <b-icon :icon="icon"></b-icon> {{ displayed_value }}
  </span>
</template>

<script type="text/javascript">
  import filesize from 'filesize';

  export default {
    name: 'ResourceBadge',
    props: {
      kind: String,  // cpu, memory, disk, shm
      value: Number, // actual data
      human_value: String,  // human repr of value (instead of raw one)
    },
    computed: {
      displayed_value() {
        if (this.human_value)
          return this.human_value;
        return (this.kind == 'cpu') ? this.value : filesize(this.value); },
      icon() { return {cpu: 'cpu-fill', memory: 'gear-fill', disk: 'server', shm: 'hdd-stack-fill'}[this.kind]; },
      tooltip_text() {
        return {cpu: "CPU", memory: "Memory", disk: "Disk", shm:"SHM"}[this.kind];
      },
    }
  }
</script>
