<template>
  <br/>
  <el-row class="row-bg" justify="space-evenly">
    <el-col :span="20">
      <el-row class="row-bg">
        <h4 style="margin: 0 0 1% 0">Prompts</h4>
        <el-input
            v-model="prompt.prompt"
            type="textarea"
            placeholder='Please enter ChatBot sys prompts. '
            @blur="updatePrompt()"
            rows="50"
        />
      </el-row>
    </el-col>
  </el-row>
</template>

<style scoped lang="stylus">

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
      baseUrl: instance?.appContext.config.globalProperties.chatbotUrl,
      isSubmitting: false,
      prompt: {
        prompt: '',
        humor: 0,
        knowledgeability: 0,
        friendliness: 0,
        tone: ''
      },
      model: '',
    }
  },
  created() {
    this.recorder = new Recorder()
  },
  methods: {
    markdownToHtml(markdownString) {
      return marked.marked(markdownString);
    },
    async getPrompt() {
      try {
        this.isSubmitting = true
        const response = await axios.get(this.baseUrl + `prompt/?timestamp=${new Date().getTime()}`)
        this.prompt = response.data
      } catch (error) {
        console.error('Error getting prompt:', error)
      } finally {
        this.isSubmitting = false
      }
    },
    async updatePrompt() {
      try {
        this.isSubmitting = true
        await axios.post(
            this.baseUrl + `prompt/?timestamp=${new Date().getTime()}`,
            {
              prompt: this.prompt.prompt,
              humor: this.prompt.humor,
              knowledgeability: this.prompt.knowledgeability,
              friendliness: this.prompt.friendliness,
              tone: this.prompt.tone
            },
            {
              headers: {
                'Content-Type': 'application/x-www-form-urlencoded'
              }
            }
        );
        await this.getPrompt()
      } catch (error) {
        console.error('Error sending message:', error)
      } finally {
        this.isSubmitting = false
      }
    },
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
