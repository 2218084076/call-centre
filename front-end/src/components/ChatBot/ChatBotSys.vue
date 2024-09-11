<template>
  <el-button style="margin: 1% 0 0 0" size="large" type="danger" icon="Delete" circle @click="clearMessage"/>
  <!-- 消息记录 -->
  <el-scrollbar ref="scrollbar" class="chat-container" height="74vh" style="display: grid">
    <div
        v-for="(message,index) in all_messages"
        :key="index"
        style="display: grid"
        :style="message.role === 'assistant' ? 'justify-self: start;' : 'justify-self: end'"
    >
      <div class="dot" style="font-weight: bold"
           :style="message.role === 'assistant' ? 'text-align: start;' : 'text-align:  end;'">
        {{ message.role }}
      </div>
      <div
          style="
              margin: 0 0 1% 0;
              padding: 1%;
              list-style-type: none;
              text-align: justify;
              word-wrap: normal;
              border-radius: 10px;
              font-size: small;
              width: 75%;
            "
          :class="{ 'gray-background': message.role === 'assistant' , 'user-background': message.role === 'user'}"
      >
        <div
            style="
                justify-content: start;
              "
            v-html="markdownToHtml(message.content)"
        ></div>
        <audio
            ref="audioElement"
            :id="index"
            v-if="message.audio"
            :src="`${message.audio}?${Date.now()}`"
            controls
            preload="auto"
            style="
               text-align: start;
               justify-content: start;
               display: flex;
               width: 90%;
            "
        ></audio>
      </div>
    </div>
  </el-scrollbar>
  <!-- 输入框 -->
  <div class="input-container">
    <el-row class="row-bg" justify="center" style="align-items: center">
      <el-col :span="15" style="">
        <el-input
            v-model="newMessage"
            clearable
            placeholder="Please enter your question"
            size="large"
            @keyup.enter="submitMessage"
        />
      </el-col>
      <el-col :span="6">
        <el-button
            style="width: 80%"
            size="large"
            @click="submitMessage"
        >
          Submit
        </el-button>
      </el-col>
    </el-row>
    <el-row class="row-bg" justify="center" style="align-items: center">
      <el-col
          :span="21"
          style="
          padding: 1% 0 1% 0;
          display: grid;
          "
      >
        <el-button
            :type="isPressing?'info':'primary'"
            @touchstart.prevent="handleStart"
            @touchend.prevent="uploadRecord"
            @mousedown.prevent="handleStart"
            @mouseup.prevent="uploadRecord"
            :disabled="isSubmitting"
            size="large"
            :loading="isSubmitting"
        >
          <el-icon>
            <Microphone/>
          </el-icon>
          Hold to speak<span v-if="recorder.duration"> {{ recorder && recorder.duration.toFixed(4) }}</span>
        </el-button>
      </el-col>
    </el-row>
  </div>
</template>

<style scoped lang="stylus">
.input-container {
  position: fixed;
  bottom: 0;
  width: 100%;
  background-color: white;
  padding: 1% 0 0 0;
  box-shadow: 13px -3px 13px 0 rgba(0, 0, 0, 0.1);
}

.chat-container {
  display: grid;
}

@keyframes loading-rotate {
  to {
    transform: rotate(360deg);
  }
}

@keyframes loading-dash {
  0% {
    stroke-dasharray: 1, 200;
    stroke-dashoffset: 0;
  }
  50% {
    stroke-dasharray: 90, 150;
    stroke-dashoffset: -40px;
  }
  100% {
    stroke-dasharray: 90, 150;
    stroke-dashoffset: -120px;
  }
}

@keyframes custom-spin-move {
  to {
    opacity: 1;
  }
}


.dot:before {
  content: '•';
  margin-right: 5px;
  font-size: x-large;
  color: hsl(161, 100%, 30%);
}

.gray-background {
  background-color: rgba(196, 196, 196, 0.35);
  border-radius: 5px;
  margin-bottom: 20px !important;
  justify-self: start;
}

.user-background {
  background-color: hsla(165, 38%, 81%, 0.4);
  border-radius: 5px;
  align-items: end;
  justify-self: end;
}

@keyframes rotate {
  0% {
    transform: rotate(0deg);
    width: 2%;
    height: 2vh;
  }
  100% {
    transform: rotate(360deg);
    width: 2%;
    height: 2vh;
  }
}

.arabic-text {
  direction: rtl;
  text-align: right;
}
</style>

<script>
import axios from 'axios'
import * as marked from 'marked'
import {
  CircleCloseFilled,
  Delete,
  Microphone,
  Promotion,
  UploadFilled,
} from '@element-plus/icons-vue'
import Recorder from 'js-audio-recorder'
import {getCurrentInstance} from 'vue'

export default {
  components: {Microphone, CircleCloseFilled, Promotion, UploadFilled, Delete},
  data() {
    const instance = getCurrentInstance();
    return {
      newMessage: '',
      baseUrl: instance?.appContext.config.globalProperties.chatbotUrl,
      messages: {
        "message": "",
        "data": {
          "question": "",
          "answer": ""
        },
        "response_time": 0.0,
        "token": {
          "question": 0,
          "answer": 0
        },
        "audio": '1',
        "start_time": 0,
        "end_time": 0,
        'name': '',
        'img': '',
        'check': false
      },
      isSubmitting: false,
      audioKey: new Date().getTime(),
      file: '',
      fileName:
          "",
      recorder: null,
      playTime: 0,
      audioSrc: "",
      prompts: {},
      initAssistantStatus: false,
      state: true,
      all_messages: [],
      isPressing: false,
      errorContent: '',
      value: '',
      options: [{value: 'en', label: 'en'}, {value: 'zh', label: 'zh'}
      ]
    }
  },
  created() {
    this.recorder = new Recorder()
  },
  methods: {
    handleStart() {
      this.isPressing = true
      this.recorder = new Recorder()
      Recorder.getPermission().then(() => {
        console.log('开始录音')
        this.recorder.start() // 开始录音
      }, (error) => {
        this.$message({
          message: 'Please allow this page to use the microphone first',
          type: 'info'
        })
        console.log(`${error.name} : ${error.message}`)
      })
    },
    async uploadRecord() {
      this.isPressing = false
      if (this.recorder == null || this.recorder.duration === 0) {
        return false
      }
      this.recorder.pause() // 暂停录音
      this.timer = null
      this.isSubmitting = true
      this.$message({
        message: 'Submit recording',
        type: 'info'
      })
      const formData = new FormData()
      const blob = this.recorder.getWAVBlob()
      const newbolb = new Blob([blob], {type: 'audio/wav'})
      const fileOfBlob = new File([newbolb], new Date().getTime() + '.wav')
      formData.append('audio', fileOfBlob)
      formData.append('language', this.value)
      const sttUrl = this.baseUrl + 'stt/';
      const aiUrl = this.baseUrl + 'ask/';
      try {
        const response = await axios.post(sttUrl, formData);
        this.stt_res = response.data

        const aiRes = await axios.post(aiUrl, formData)
        this.messages = aiRes.data

        this.isSubmitting = false
        this.fetchHistory()
        this.recorder.duration = null
        // setTimeout(() => {
        //   const audioElement = document.getElementById('1');
        //   if (audioElement) {
        //     audioElement.play().catch(error => console.error("自动播放失败", error));
        //   }
        // }, 500); // 500毫秒的延迟

      } catch (error) {
        console.error(error);
        this.$message({
          message: error,
          type: 'error'
        })
        this.isSubmitting = false
        this.audioSrc = `https://testapp.tfg.ltd/api/v2/output/speech.mp3?timestamp=${new Date().getTime()}`
        this.audioKey = new Date().getTime()
        this.recorder = null
        this.fetchHistory()
      }
    },
    async submitMessage() {
      this.all_messages.push({"role": "user", "content": this.newMessage})
      this.scrollToBottom();
      try {
        this.isSubmitting = true
        const res = await axios.post(
            this.baseUrl + 'completions/',
            {question: this.newMessage},
            {
              headers: {
                'Content-Type': 'multipart/form-data'
              }
            }
        );
        this.messages = res.data
        if (this.messages.name === "Please submit the correct name") {
          this.newMessage = this.messages.name
          this.$message({
            message: this.messages.name,
            type: 'info'
          })
        } else {
          this.fetchHistory()
        }
      } catch (error) {
        console.error('Error sending message:', error)
      } finally {
        this.isSubmitting = false
        this.fetchHistory()
      }
    },
    markdownToHtml(markdownString) {
      return marked.marked(markdownString);
    },
    fetchHistory() {
      try {
        axios.get(this.baseUrl + `messages/?timestamp=${new Date().getTime()}`,
        ).then(res => {
          this.all_messages = this.reversePairs(res.data).filter(message => message.role !== "system")
        });
        this.newMessage = ''
        this.scrollToBottom()
      } catch (error) {
        this.isLoading = false
        this.errorContent = error
        console.error('Error fetching chat history:', error)
        this.newMessage = ''
      }
    },
    reversePairs(messages) {
      const pairs = [];
      let pair = [];
      // Step 1: 分组
      messages.forEach((message, index) => {
        pair.push(message);
        if (message.role === 'assistant' || index === messages.length - 1) {
          pairs.push([...pair]);
          pair = [];
        }
      });
      // const reversedPairs = pairs.reverse();
      return pairs.flat()
    },
    async clearMessage() {
      this.messages.response_time = 0
      this.recorder.duration = null
      await axios.get(this.baseUrl + `initMessages/?timestamp=${new Date().getTime()}`)
      await this.fetchHistory()
    },
    scrollToBottom() {
      const el = this.$refs.scrollbar.$el.querySelector('.el-scrollbar__wrap');
      if (el) {
        el.scrollTo({
          top: el.scrollHeight,
          behavior: 'auto', // or 'auto' if you want instant scroll
        });
        setTimeout(() => {
          el.scrollTo({
            top: el.scrollHeight,
            behavior: 'smooth', // or 'auto' if you want instant scroll
          });
        }, 100); // 100毫秒的延迟
      }
    },
  },
  beforeUnmount() {
    if (this.timer) {
      clearInterval(this.timer);
    }
  },
  mounted() {
    this.fetchHistory()
    this.$nextTick(() => {
      this.scrollToBottom();
    });
    this.isPressing = false
    this.recorder.duration = 0
  },
}
</script>
