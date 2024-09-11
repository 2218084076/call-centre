<script setup lang="ts">
import {ref} from 'vue'
import type {TabsPaneContext} from 'element-plus'
import AiChatSys from "@/components/SalesHotline/AiChatSys.vue";
import SystemConfig from "@/components/SalesHotline/SystemConfig.vue";
import Stream from '@/components/SalesHotline/Stream.vue'

const activeName = ref('first')

const handleClick = (tab: TabsPaneContext, event: Event) => {
  console.log(tab, event)
}
// import SystemConfig from "../components/SalesHotline/SystemConfig.vue";
// import AiChatSys from "../components/SalesHotline/AiChatSys.vue";
// import {ChatLineRound} from '@element-plus/icons-vue'
// import {onMounted, onUnmounted, ref} from "vue";
//
// const activeName = ref('first')
// let activeTab = ref(localStorage.getItem('activeTab') || 'chat bot');
//
// onMounted(() => {
//   const savedTab = localStorage.getItem('activeTab');
//   if (savedTab) {
//     activeTab.value = savedTab;
//   }
// });
//
// onUnmounted(() => {
//   localStorage.setItem('activeTab', activeTab.value);
// });
//
// async function handleTabClick(tab) {
//   activeTab = tab.props.label;
//   console.log(tab.props.label)
// }

</script>

<template>
  <el-tabs
      v-model="activeName"
      type="border-card"
      class="aisys-tabs"
      style="border: none"
      @tab-click="handleClick"
  >
    <el-tab-pane label="WebSocket Stream Demo" name="first">
      <template #label>
        <el-icon size="20px">
          <Stamp/>
        </el-icon>
        <span>WebSocket Stream Demo</span>
      </template>
      <Stream/>
    </el-tab-pane>
    <el-tab-pane label="System" name="second">
      <template #label>
        <el-icon size="20px" style="align-items: center;">
          <Setting/>
        </el-icon>
        <span>System</span>
      </template>
      <SystemConfig/>
    </el-tab-pane>
  </el-tabs>
</template>

<style scoped>
.aisys-tabs > .el-tabs__content {
  padding: 32px;
  color: #6b778c;
  font-size: 32px;
  font-weight: 600;
}
</style>