<template>
  <el-table
      :data="tableData"
      :default-sort="{ prop: 'date', order: 'descending' }"
      style="width: 100%;margin: 2% 0 0 0"
      border
  >
    <el-table-column prop="id" label="ID" width="60"/>
    <el-table-column prop="thread_id" label="Thread Id" sortable>
      <template #default="{ row }">
        {{ truncateContent(row.thread_id) }}
      </template>
    </el-table-column>
    <el-table-column prop="role" label="Role" width="68"/>
    <el-table-column prop="assistants" label="Assistants"/>
    <el-table-column prop="content" label="Content">
      <template #default="{ row }">
        {{ truncateContent(row.content) }}
      </template>
    </el-table-column>
    <el-table-column prop="audio_time_consuming" label="Audio Time Consuming" sortable>
      <template #default="{ row }">
        {{ filter(row.audio_time_consuming) }}
      </template>
    </el-table-column>
    <el-table-column prop="req_life_cycle" label="Request life cycle" sortable>
      <template #default="{ row }">
        {{ filter(row.req_life_cycle) }}
      </template>
    </el-table-column>
    <el-table-column prop="create_time" label="Create Time" sortable>
      <template #default="{ row }">
        {{ getDate(row.create_time) }}
      </template>
    </el-table-column>
    <el-table-column prop="token" label="Token" sortable :formatter="formatter"/>
  </el-table>
</template>

<script lang="ts" setup>
import type {TableColumnCtx} from 'element-plus'
import axios from "axios";
import {onMounted, ref, onUnmounted, getCurrentInstance} from "vue";

let resizeObserver: ResizeObserver | null = null;
let element: HTMLElement | null = null;
let tableData = ref<Record[]>([]);
const instance = getCurrentInstance();
const baseUrl = instance?.appContext.config.globalProperties.baseUrl;

interface Record {
  id: number
  role: string
  assistants: string
  content: string
  token: number
  thread_id: string
  audio_time_consuming: string
  create_time: string
  update_time: string

}

const formatter = (row: Record, column: TableColumnCtx<Record>) => {
  return row.token
}
const getData = async () => {
  const response = await axios.get(baseUrl + 'all');
  tableData.value = response.data.data;
}


const truncateContent = (content: string) => {
  return content.length > 5 ? content.substr(0, 10) + '***' : content;
}

const filter = (content: string) => {
  if (content !== '0:00:00') {
    return content
  } else {
    return '0'
  }
}

function getDate(text: string) {
  let date = new Date(text);
  return date.getFullYear() + '-'
      + (date.getMonth() + 1).toString().padStart(2, '0') + '-'
      + date.getDate().toString().padStart(2, '0') + ' '
      + date.getHours().toString().padStart(2, '0') + ':'
      + date.getMinutes().toString().padStart(2, '0') + ':'
      + date.getSeconds().toString().padStart(2, '0');
}

onMounted(
    async () => {
      await getData()
    }
);
onUnmounted(() => {
  if (resizeObserver && element) {
    resizeObserver.unobserve(element);
    resizeObserver = null;
    element = null;
  }
});

</script>
