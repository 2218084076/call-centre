<template>
  <el-row class="row-bg" justify="space-evenly">
    <el-col :span="22">
      <el-row class="row-bg">
        <h4 style="margin: 1% 0 1% 0">Prompts</h4>
        <el-input
            v-model="prompt"
            style="width: 100%"
            type="textarea"
            placeholder="Enter a system message"
            @blur="submit"
            rows="50"
        />
      </el-row>
    </el-col>
  </el-row>
  <el-row class="row-bg" justify="space-evenly">
    <el-col :span="20">

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
import {getCurrentInstance} from 'vue'


export default {
  data() {
    const instance = getCurrentInstance();
    return {
      newMessage: '',
      baseUrl: instance?.appContext.config.globalProperties.orderSysUrl,
      isSubmitting: false,
      prompt: '',
      temperature: 1
    }
  },
  created() {
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
