<script setup>
import AtomSysConfig from "../components/Atom/AtomSysConfig.vue";
import AtomSys from "../components/Atom/AtomSys.vue";
import {onMounted, onUnmounted, ref} from "vue";

let activeTab = ref(localStorage.getItem('activeTab') || 'Article Analysis System');

onMounted(() => {
  const savedTab = localStorage.getItem('activeTab');
  if (savedTab) {
    activeTab.value = savedTab;
  }
});

onUnmounted(() => {
  localStorage.setItem('activeTab', activeTab.value);
});

async function handleTabClick(tab) {
  activeTab = tab.props.label;
  console.log(tab.props.label)
}

</script>

<template>
  <el-tabs tab-position="top" @tab-click="handleTabClick" style="">
    <el-tab-pane label="Acrostic-Poem">
      <AtomSys/>
    </el-tab-pane>
    <el-tab-pane label="System">
      <AtomSysConfig/>
    </el-tab-pane>
  </el-tabs>
</template>

<style scoped>

</style>