<script setup>
import SystemConfig from "../components/SalesHotline/SystemConfig.vue";
import SalesHotline from "../components/SalesHotline/SalesHotline.vue";
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
  <el-tabs tab-position="top" class="demo-tabs" @tab-click="handleTabClick">
    <el-tab-pane label="Sales Hotline Assistant">
      <SalesHotline/>
    </el-tab-pane>
    <el-tab-pane label="SYSTEM">
      <SystemConfig/>
    </el-tab-pane>
  </el-tabs>
</template>

<style scoped>
</style>