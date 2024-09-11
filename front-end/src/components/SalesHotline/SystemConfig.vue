<template>
  <!--  stt -->
  <el-row class="row-bg" justify="center">
    <el-col :span="23" style="text-align: start">
      <h2 style="text-align: start;color: #303133;">STT Configuration</h2>
    </el-col>
  </el-row>
  <el-row class="row-bg" justify="space-evenly">
    <el-col :span="11">
      <h3 style="margin: 0 0 1% 0;text-align: start;color: #6b778c">Provider</h3>
      <el-select
          v-model="configMsg.stt"
          placeholder="Select"
          size="large"
          @blur="upConfig('stt')"
      >
        <el-option
            v-for="item in sttFunctionOptions"
            :key="item.value"
            :label="item.label"
            :value="item.value"
            :disabled="item.disabled"
        />
      </el-select>
    </el-col>
    <el-col :span="11">
      <h3 style="margin: 0 0 1% 0;text-align: start;color: #6b778c">Models</h3>
      <el-select
          v-model="configMsg.stt_model"
          placeholder="Select"
          size="large"
          @blur="upConfig('stt_model')"
          @click="upConfig('stt_model')"
      >
        <el-option
            v-for="item in currentSttModelOptions"
            :key="item.value"
            :label="item.label"
            :value="item.value"
        />
      </el-select>
    </el-col>
    <el-col :span="24">
      <hr style="border-style: dashed;color: #c4c4c4;margin: 3% 0 1% 0"/>
    </el-col>
  </el-row>
  <!-- Ai assistant -->
  <el-row class="row-bg" justify="center">
    <el-col :span="23">
      <h2 style="text-align: start">Ai assistant configuration</h2>
    </el-col>
  </el-row>
  <el-row class="row-bg" justify="space-evenly">
    <el-col style="text-align: start" :span="11">
      <h3 style="margin: 0 0 1% 0;text-align: start;color: #6b778c">Provider</h3>
      <el-select
          v-model="configMsg.assistant"
          placeholder="Select"
          size="large"
          @blur="upConfig('assistant')"
      >
        <el-option
            v-for="item in assistantProviderOptions"
            :key="item.value"
            :label="item.label"
            :value="item.value"
            :disabled="item.disabled"
        />
      </el-select>
    </el-col>
    <el-col style="text-align: start" :span="11">
      <h3 style="margin: 0 0 1% 0;text-align: start;color: #6b778c">Models</h3>
      <el-select
          v-model="configMsg.llms"
          placeholder="Select"
          size="large"
          @blur="upConfig('')"
      >
        <el-option
            v-for="item in currentAiModelOptions"
            :key="item.value"
            :label="item.label"
            :value="item.value"
        />
      </el-select>
    </el-col>
    <el-col :span="24">
      <hr style="border-style: dashed;color: #c4c4c4;margin: 3% 0 1% 0"/>
    </el-col>
  </el-row>
  <!--  tts -->
  <el-row class="row-bg" justify="center">
    <el-col :span="23">
      <h2 style="text-align: start">TTS Voice Configuration</h2>
    </el-col>
  </el-row>
  <el-row class="row-bg" justify="space-evenly">
    <el-col :span="11">
      <h3 style="margin: 0 0 1% 0;text-align: start;color: #6b778c">Provider</h3>
      <el-select
          v-model="configMsg.tts"
          placeholder="Select"
          size="large"
          @blur="upConfig('tts')"
          @click="upConfig('tts')"
      >
        <el-option
            v-for="item in ttsFunctionOptions"
            :key="item.value"
            :label="item.label"
            :value="item.value"
            :disabled="item.disabled"
        >
        </el-option>
      </el-select>
    </el-col>
    <el-col :span="11">
      <h3 style="margin: 0 0 1% 0;text-align: start;color: #6b778c">Model</h3>
      <el-select
          v-model="configMsg.tts_model"
          placeholder="Select"
          size="large"
          @blur="upConfig('')"
          @click="upConfig('')"
      >
        <el-option
            v-for="item in currentTtsModelOptions"
            :key="item.value"
            :label="item.label"
            :value="item.value"
            :disabled="item.disabled"
        >
        </el-option>
      </el-select>
    </el-col>
    <el-col :span="24">
      <hr style="border-style: dashed;color: #c4c4c4;margin: 3% 0 1% 0"/>
    </el-col>
  </el-row>
  <!-- Prompts -->
  <el-row class="row-bg" justify="space-evenly">
    <el-col :span="23">
      <h2 style="text-align: start">Prompts</h2>
    </el-col>
    <el-col :span="23">
      <el-row class="row-bg">
        <el-input
            v-model="prompt.prompt"
            type="textarea"
            placeholder='Please enter ChatBot sys prompts. '
            @blur="updatePrompt()"
            @click="updatePrompt()"
            rows="10"
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
      baseUrl: instance?.appContext.config.globalProperties.aiSysUrl,
      isSubmitting: false,
      prompt: {
        prompt: '',
      },
      model: '',
      activeName: 'first',
      sttModelOptions: {
        wf: [
          {
            value: 'Whisper-large-v3',
            label: 'Whisper-large-v3',
          },
        ],
        dg: [
          {
            value: 'nova-2',
            label: 'nova-2',
          },
        ],
        funasr: [
          {
            value: 'iic/speech_paraformer-large_asr_nat-zh-cn-16k-common-vocab8404-pytorch',
            label: 'speech_paraformer-large_asr_nat-zh-cn-16k-common-vocab8404-pytorch',
          },
          {
            value: 'iic/Whisper-large-v3',
            label: 'Whisper-large-v3',
          },
        ]
      },
      sttFunctionOptions: [
        {
          value: 'wf',
          label: 'whisper-finetune',
          disabled: true,
          des: ''
        },
        {
          value: 'dg',
          label: 'deepgram',
          disabled: true
        },
        {
          value: 'funasr',
          label: 'FunASR',
        },
      ],
      ttsFunctionOptions: [
        {
          value: 'elevenlabs',
          label: 'ElevenLabs',
          disabled: true, des: ''
        },
        {
          value: 'playht',
          label: 'PlayHT',
          disabled: true, des: ''
        },
        {value: 'cartesia', label: 'Cartesia', disabled: true, des: ''}
      ],
      ttsModelOptions: {
        elevenlabs: [
          {
            value: 'eleven_multilingual_v2',
            label: 'Eleven Multilingual v2',
            disabled: true, des: ''
          },
          {
            value: 'eleven_multilingual_v1',
            label: 'Eleven Multilingual v1',
            disabled: true
          },
        ],
        playht: [
          {
            value: 'PlayHT2.0',
            label: 'PlayHT2.0',
            disabled: true, des: ''
          },
          {
            value: 'PlayHT1.0',
            label: 'PlayHT1.0',
            disabled: true, des: ''
          },
        ],
      },
      configMsg: {
        stt: '',
        assistant: '',
        tts: '',
        stt_model: '',
        llms: '',
        tts_model: ''
      },
      assistantModelOptions: {
        gpt: [
          {value: 'gpt-3.5-turbo', label: 'gpt-3.5-turbo'},
          {value: 'gpt-4o', label: 'GPT-4o'},
          {value: 'gpt-4', label: 'GPT-4'},
        ],
        groq: [
          {value: 'llama3-8b-8192', label: 'llama3-8b-8192'},
          // {value: 'llama3-70b-8192', label: 'llama3-70b-8192'},
          // {value: 'mixtral-8x7b-32768', label: 'mixtral-8x7b-32768'},
        ]
      },
      assistantProviderOptions: [
        {value: 'gpt', label: 'Openai', disabled: true,},
        {value: 'groq', label: 'Groq'},
      ]
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
    async getConfig() {
      try {
        this.isSubmitting = true
        const response = await axios.get(this.baseUrl + `config/?timestamp=${new Date().getTime()}`)
        this.configMsg = response.data
      } catch (error) {
        console.error('Error getting prompt:', error)
      } finally {
        this.isSubmitting = false
      }
    },
    async upConfig(field) {
      try {
        if (field === 'stt') {
          this.configMsg.stt_model = this.currentSttModelOptions[0].value
        }
        if (field === 'assistant') {
          this.configMsg.llms = this.currentAiModelOptions[0].value
        }
        if (field === 'tts') {
          this.configMsg.tts_model = this.currentTtsModelOptions[0].value
        }
        this.isSubmitting = true
        console.log('configMsg', this.configMsg)
        await axios.post(
            this.baseUrl + `config/?timestamp=${new Date().getTime()}`,
            {
              stt: this.configMsg.stt,
              chat: this.configMsg.assistant,
              tts: this.configMsg.tts,
              stt_m: this.configMsg.stt_model,
              // # voice: str = Form(description='Select the Text-to-Speech voice', default='en-US-Wavenet-C'),
              llm: this.configMsg.llms,
              tts_m: this.configMsg.tts_model
            },
            {
              headers: {
                'Content-Type': 'application/x-www-form-urlencoded'
              }
            }
        );
        await this.getConfig()
      } catch (error) {
        console.error('Error sending message:', error)
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
    this.getConfig()
  },
  computed: {
    currentSttModelOptions() {
      return this.sttModelOptions[this.configMsg.stt] || [];
    },
    currentAiModelOptions() {
      return this.assistantModelOptions[this.configMsg.assistant] || [];
    },
    currentTtsModelOptions() {
      return this.ttsModelOptions[this.configMsg.tts] || [];
    }
  }
}
</script>
