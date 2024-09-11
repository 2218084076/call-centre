<script setup lang="ts">
import {ref} from 'vue';
import {Plus, Delete} from '@element-plus/icons-vue';

// 标签数组
const tags = ref<string[]>([]);
const prompts = ref<string[]>([]);
const promptText = ref<string>('');
let loading = ref<boolean>(false)

function addTag() {
  loading.value = false
  const newTag = `Prompt ${tags.value.length + 1}`;
  tags.value.push(newTag);
  prompts.value.push('');
}

function removeTag(index: number) {
  tags.value.splice(index, 1);
  prompts.value.splice(index, 1);
}

function loadPrompts() {
  loading.value = true
  const newPrompts = promptText.value.split(',').map(p => p.trim()).filter(p => p);

  tags.value = [];
  prompts.value = [];

  newPrompts.forEach((prompt, index) => {
    tags.value.push(`Prompt ${index + 1}`);
    prompts.value.push(prompt);
  });

  promptText.value = '';
}
</script>

<template>
  <el-row class="row-bg tag-container">
    <el-col :span="18">
      <el-row v-for="(tag, index) in tags" :key="index" class="tag-item">
        <el-col :span="2" style="text-align: start">
          <el-tag size="large" style="font-size: 13px">{{ tag }}</el-tag>
        </el-col>
        <el-col :span="15">
          <el-input
              size="large"
              type="textarea"
              v-model="prompts[index]"
              placeholder="Enter comma-separated prompts"
          />
        </el-col>
        <el-col :span="2">
          <el-button
              size="mini"
              type="danger"
              :icon="Delete"
              circle
              @click="removeTag(index)"
          ></el-button>
        </el-col>
      </el-row>
    </el-col>
    <el-col :span="6">
      <el-button
          size="large"
          :icon="Plus"
          round
          type="success"
          style="width: 100%; margin: 0 0 2% 0"
          @click="addTag"
      > Add Tag
      </el-button>
      <div v-if="!loading">
        <el-input
            v-model="prompts"
            rows="10"
            type="textarea"
            placeholder="Paste comma-separated prompts here"
        />
      </div>
      <div v-else>
        <el-input
            v-model="promptText"
            rows="10"
            type="textarea"
            placeholder="Comma-separated prompts"
        />
      </div>
      <el-button
          size="large"
          type="primary"
          style="width: 100%; margin-top: 2%"
          @click="loadPrompts"
          round
      > Load Prompts
      </el-button>
    </el-col>
  </el-row>
</template>

<style scoped lang="stylus">
.tag-container {
  margin: 2% ;
}

.tag-item {
  display: flex;
  align-items: center;
  margin-bottom: 10px
}

.tag-item input {
  margin-left: 10px
}
</style>