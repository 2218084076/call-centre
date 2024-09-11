<template>
  <br/>
  <el-row class="row-bg" justify="space-evenly">
    <el-col :span="20">
      <el-row class="row-bg">
        <p style="font-size: large">Prompts</p>
        <el-input
            v-model="prompt.gpt"
            type="textarea"
            placeholder='Please enter the "acrostic poem" prompts. '
            @blur="updatePrompt('gpt')"
            style="font-size: large"
            rows="4"
        />
      </el-row>
    </el-col>
    <el-col :span="20">
      <el-row class="row-bg">
        <p style="font-size: large">DALL·E Prompts</p>
        <el-input
            v-model="prompt.img_prompt"
            type="textarea"
            placeholder='Please enter "DALL·E" to generate image prompts. '
            @blur="updatePrompt('img')"
            style="font-size: large"
            rows="7"
        />
      </el-row>
    </el-col>
    <el-col :span="20">
      <el-row class="row-bg">
        <p style="font-size: large">Filter words prompts</p>
        <el-input
            v-model="prompt.check"
            type="textarea"
            placeholder='Please enter "DALL·E" to generate image prompts. '
            @blur="updatePrompt('check')"
            style="font-size: large"
            rows="7"
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
      newMessage: '',
      baseUrl: instance?.appContext.config.globalProperties.atomSysUrl,
      isSubmitting: false,
      prompt: {'img_prompt': '', 'gpt': '', 'check': ''},
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
    async getModel() {
      try {
        this.isSubmitting = true
        const response = await axios.get(this.baseUrl + 'model/')
        this.model = response.data
      } catch (error) {
        console.error('Error getting model:', error)
      } finally {
        this.isSubmitting = false
      }
    },
    async updatePrompt(role) {
      try {
        this.isSubmitting = true
        if (role === 'img') {
          const prompt = this.prompt.img_prompt
          await axios.post(
              this.baseUrl + `prompt/`,
              {prompt: prompt, role: 'img'},
              {
                headers: {
                  'Content-Type': 'multipart/form-data'
                }
              }
          );
        }
        if (role === 'check') {
          const prompt = this.prompt.check
          await axios.post(
              this.baseUrl + `prompt/`,
              {prompt: prompt, role: 'check'},
              {
                headers: {
                  'Content-Type': 'multipart/form-data'
                }
              }
          );
        }
        if (role === 'gpt') {
          const prompt = this.prompt.gpt
          await axios.post(
              this.baseUrl + `prompt/`,

              {prompt: prompt, role: 'gpt'},
              {
                headers: {
                  'Content-Type': 'multipart/form-data'
                }
              }
          );
        }

        await this.getPrompt()
      } catch (error) {
        console.error('Error sending message:', error)
        this.newMessage = ''
      } finally {
        this.isSubmitting = false
        this.newMessage = ''
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
