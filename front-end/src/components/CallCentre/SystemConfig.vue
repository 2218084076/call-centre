<template>
  <el-row class="row-bg" style="margin: 1% 0 1% 0">
    <el-col class="title-p">Call Centre</el-col>
  </el-row>
  <el-row class="row-bg">
    <el-col :span="19">
      <el-input
          v-model="prompt"
          style="width: 100%"
          :autosize="{ maxRows: 55 }"
          type="textarea"
          placeholder="Enter a system message"
      />
    </el-col>
    <el-col :span="5">
      <el-button round size="large" type="primary" @click="submit" :loading="isSubmitting" style="width: 80%">
        <template #loading>
          <div class="custom-loading">
            <svg class="circular" viewBox="-10, -10, 50, 50">
              <path
                  class="path"
                  d="
            M 30 15
            L 28 17
            M 25.61 25.61
            A 15 15, 0, 0, 1, 15 30
            A 15 15, 0, 1, 1, 27.99 7.5
            L 15 15
          "
                  style="stroke-width: 4px; fill: rgba(0, 0, 0, 0)"
              />
            </svg>
          </div>
        </template>
        Save
      </el-button>
    </el-col>
  </el-row>
</template>

<style scoped lang="stylus">
.title-p {
  color: hsla(161, 100%, 24%, 0.66);
  font-weight: bold;
}

.el-button .custom-loading .circular {
  margin-right: 6px;
  width: 18px;
  height: 18px;
  animation: loading-rotate 2s linear infinite;
}

.el-button .custom-loading .circular .path {
  animation: loading-dash 1.5s ease-in-out infinite;
  stroke-dasharray: 90, 150;
  stroke-dashoffset: 0;
  stroke-width: 2;
  stroke: var(--el-button-text-color);
  stroke-linecap: round;
}
</style>

<script>
import axios from 'axios'
import * as marked from 'marked'
import Recorder from 'js-audio-recorder'
import {getCurrentInstance} from 'vue'


export default {
  data() {
    const instance = getCurrentInstance();
    return {
      newMessage: '',
      baseUrl: instance?.appContext.config.globalProperties.callCentreUrl,
      isSubmitting: false,
      prompt: '',
      temperature: 1
    }
  },
  created() {
    this.recorder = new Recorder()
  },
  methods: {
    async submit() {
      try {
        this.isSubmitting = true
        await axios.post(
            this.baseUrl + 'prompt/',
            {prompt: this.prompt},
            {
              headers: {
                'Content-Type': 'multipart/form-data'
              }
            }
        );
        await this.getPrompt()
      } catch (error) {
        console.error('Error sending message:', error)
        this.newMessage = ''
      } finally {
        this.isSubmitting = false
        this.newMessage = ''
      }
    },
    markdownToHtml(markdownString) {
      return marked.marked(markdownString);
    },
    async getPrompt() {
      try {
        this.isSubmitting = true
        const response = await axios.get(this.baseUrl + 'prompt/')
        this.prompt = response.data
      } catch (error) {
        console.error('Error getting prompt:', error)
      } finally {
        this.isSubmitting = false
      }
    }
  },
  beforeUnmount() {
    if (this.timer) {
      clearInterval(this.timer);
    }
  },
  mounted() {
    this.getPrompt()
  },
}
</script>
