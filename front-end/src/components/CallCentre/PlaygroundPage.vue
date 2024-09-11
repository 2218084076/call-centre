<script setup lang="ts">
import {ref, Ref, getCurrentInstance, onMounted, watch} from 'vue';
import axios from "axios";
import {UploadFilled} from '@element-plus/icons-vue';
import * as marked from 'marked';


interface Message {
  role: string,
  content: string
}


const textarea: Ref<string> = ref(' ')
const prompts: Ref<string> = ref('')
const instance = getCurrentInstance()
const audioFiles = [
  {
    value: 'https://testapp.tfg.ltd/api/output/callcentre/ONEPIP02AshokaXpress.mp3',
    label: 'English telephone recording'
  },
]
const callCentreUrl = instance?.appContext.config.globalProperties.callCentreUrl
let messages: Ref<Message[]> = ref([])
let file = ref('')
let fileName = ref('')
let isLoading = ref(false)
let isSubmitting = ref(false)
let audioFile = ref('')

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
    formData.append('audio', audioFile.value)
    await axios.post(callCentreUrl + 'analyse/', formData);
    await allMessages()
    textarea.value = ''
    await allMessages()
  } catch (error) {
    console.error("Failed to fetch prompts:", error)
    await allMessages()
  }
}


async function submitMessage() {
  try {
    let formData = new FormData()
    formData.append('content', textarea.value)
    formData.append('temperature', '1')
    await axios.post(callCentreUrl + 'chatCompletion/', formData);
    await allMessages()
    textarea.value = ''
  } catch (error) {
    console.error("Failed to fetch prompts:", error)
  }
}


async function submit() {
  isSubmitting.value = true
  console.log(audioFile.value)
  if (audioFile.value) {
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
      <h3>System</h3>
      <el-input
          v-model="prompts"
          type="textarea"
          placeholder="Please input"
          @blur="updatePrompts"
          rows="50"
      />
    </el-col>
    <el-col :span="13">
      <h3>User</h3>
      <el-row class="row-bg">
        <el-col :span="10">
          <el-select
              v-model="audioFile"
              :empty-values="[null, undefined]"
              :value-on-clear="null"
              clearable
              placeholder="Select"
              size="large"
          >
            <el-option
                v-for="item in audioFiles"
                :key="item.value"
                :label="item.label"
                :value="item.value"
            />
          </el-select>
          <audio
              ref="audioElement"
              v-if="audioFile"
              :src="audioFile"
              controls
              preload="auto"
          ></audio>
        </el-col>
        <el-col :span="1"/>
        <el-col :span="5">
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
      <br/>
      <el-row class="row-bg" justify="start" v-for="(message,index) in messages" :key="index"
              style="border:1px solid #ccc;border-radius: 0">
        <el-col :span="3"
                style="text-align: start;padding: 1%;display: flex; ">
          <div style="display: flex;text-align: start">
            <el-icon
                v-if="message.role === 'user'"
            >
              <Avatar style="color: #303133;"/>
            </el-icon>
            <el-icon v-if="message.role === 'assistant'"
                     style="display: inline-flex; justify-content: center; align-items: center; border: 2px solid rgba(243,243,243,0.11); border-radius: 50%;">
              <Connection style="color: #529b2e"/>
            </el-icon>
          </div>
          <h5 style="margin: 0"> {{ message.role }} </h5>
        </el-col>
        <el-col :span="21" style="text-align: start" v-html="markdownToHtml(message.content)"/>
      </el-row>
    </el-col>
  </el-row>
  <el-backtop :right="100" :bottom="100"/>
</template>

<style scoped lang="stylus">

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