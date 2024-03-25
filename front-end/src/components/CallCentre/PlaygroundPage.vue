<script setup lang="ts">
import {ref, Ref, getCurrentInstance, onMounted, watch} from 'vue';
import axios from 'axios';
import {UploadFilled} from '@element-plus/icons-vue';
import * as marked from 'marked';


interface Message {
  role: string,
  content: string
}


const textarea: Ref<string> = ref(' ')
const prompts: Ref<string> = ref('')
const instance = getCurrentInstance()
const callCentreUrl = instance?.appContext.config.globalProperties.callCentreUrl
let messages: Ref<Message[]> = ref([])
let file = ref('')
let fileName = ref('')
let isLoading = ref(false)
let isSubmitting = ref(false)

async function updatePrompts() {
  try {
    let formData = new FormData()
    formData.append('prompt', prompts.value)
    const response = await axios.post(
        callCentreUrl + 'prompts/', formData
    )
    prompts.value = response.data
  } catch (error) {
    console.error("Failed to fetch prompts:", error)
  }
}

async function getPrompts() {
  try {
    const response = await axios.get(callCentreUrl + 'prompts/')
    prompts.value = response.data
  } catch (error) {
    console.error("Failed to fetch prompts:", error)
  }
}

async function submitFile() {
  try {
    let formData = new FormData()
    formData.append('content', textarea.value)
    formData.append('temperature', '1')
    formData.append('audio', file.value)
    await axios.post(callCentreUrl + 'analyse/', formData);
    await allMessages()
    file.value = ''
  } catch (error) {
    console.error("Failed to fetch prompts:", error)
  }
}


async function submitMessage() {
  try {
    let formData = new FormData()
    formData.append('content', textarea.value)
    formData.append('temperature', '1')
    await axios.post(callCentreUrl + 'chatCompletion/', formData);
    await allMessages()
  } catch (error) {
    console.error("Failed to fetch prompts:", error)
  }
}


async function submit() {
  isSubmitting.value = true
  console.log(file.value)
  if (file.value) {
    await submitFile();
  } else {
    await submitMessage();
  }
}

function handleFileUpload(e: any) {
  file.value = e.raw
  fileName.value = e.name
}

async function allMessages() {
  try {
    await axios.get(callCentreUrl + `messages/?timestamp=${new Date().getTime()}`,
    ).then(res => {
      if (res.data && res.data.length > 0) {
        messages.value = reversePairs(res.data).filter((message: any) => message.role !== "system");
      } else {
        messages.value = [];
      }
      isSubmitting.value = false
    })
  } catch (error) {
    isLoading.value = false
    console.error('Error fetching chat history:', error)
  }
}

function reversePairs(allMessage: any[]) {
  const pairs: any = [];
  let pair: any = [];
  allMessage.forEach((message, index) => {
    pair.push(message);
    if (message.role === 'assistant' || index === messages.value.length - 1) {
      pairs.push([...pair]);
      pair = [];
    }
  });
  const reversedPairs = pairs.reverse();
  const flattened = reversedPairs.flat();
  return flattened;
}

function markdownToHtml(markdownString: string) {
  return marked.marked(markdownString);
}

async function clear() {
  messages.value = []
  await axios.get(callCentreUrl + `initMessages/?timestamp=${new Date().getTime()}`)
  await allMessages()
}

onMounted(() => {
  getPrompts()
  allMessages()
  updatePrompts()
})
</script>

<template>
  <el-row class="row-bg" justify="space-evenly">
    <el-col :span="10">
      <div class="itemTitle">SYSTEM</div>
      <el-input
          v-model="prompts"
          style="width:100%;"
          :rows="2"
          type="textarea"
          placeholder="Please input"
          :autosize="{minRows:55}"
          @blur="updatePrompts"
      />
    </el-col>
    <el-col :span="13">
      <div class="itemTitle">USER</div>
      <el-row class="row-bg">
        <el-col :span="5">
          <el-upload
              drag
              action="https://run.mocky.io/v3/9d059bf9-4660-45f2-925d-ce80ad6c4d15"
              @change="handleFileUpload"
              multiple
          >
            <el-icon class="el-icon--upload">
              <upload-filled/>
            </el-icon>
            <br/>
            <em>click to select audio file</em>
          </el-upload>
        </el-col>
        <el-col :span="19">
          <el-input
              v-model="textarea"
              style="width: 100%;"
              :rows="2"
              type="textarea"
              placeholder="Enter user message"
              :autosize="{minRows:5}"
          />
        </el-col>
      </el-row>
      <el-row class="row-bg" justify="end" style="margin: 0 0 1% 0">
        <el-col :span="4">
          <el-button style="width: 100%" size="large" round type="info" @click="clear">
            Clear
          </el-button>
        </el-col>
        <el-col :span="1"/>
        <el-col :span="5">
          <el-button style="width: 100%" :loading="isSubmitting" size="large" round type="primary"
                     @click="submit">Submit
          </el-button>
        </el-col>
      </el-row>
      <el-row class="row-bg" justify="start" v-for="(message,index) in messages" :key="index"
              style="border:1px solid #ccc;border-radius: 0">
        <el-col :span="2" style="text-align: start;padding: 0 0 0 1%" v-html="markdownToHtml(message.role)"/>
        <el-col :span="22" style="text-align: start" v-html="markdownToHtml(message.content)"/>
      </el-row>
    </el-col>
  </el-row>
  <el-backtop :right="100" :bottom="100"/>
</template>

<style scoped lang="stylus">
.itemTitle {
  margin: 1% 0 2% 0;
}

.slider-demo-block {
  max-width: 600px;
  display: flex;
  align-items: center;
}

.slider-demo-block .el-slider {
  margin-top: 0;
  margin-left: 12px;
}

</style>