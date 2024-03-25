<template>
  <el-row class="row-bg" style="margin: 1% 0 0 0">
    <el-col class="title-p">AI Demo for CSL Sales Hotline</el-col>
  </el-row>
  <el-row class="row-bg" justify="center" style="align-items: center;">
    <el-col
        :span="12"
        style="padding: 1% 0 1% 0;display: grid;justify-content: start;width: 100%;min-width: max-content">
      <div style="
                box-sizing:border-box;
                border-radius: 10px;
                padding: 4%;
                min-width: 240px;
          ">
        <div class="title">Duration(录音时长): {{
            recorder && recorder.duration.toFixed(4)
          }}
        </div>
        <div style="justify-content: start;display: flex">
          <el-button
              :type="isPressing ? 'info' : 'primary'"
              @touchstart.prevent="handleStart"
              @touchend.prevent="uploadRecord"
              @mousedown.prevent="handleStart"
              @mouseup.prevent="uploadRecord"
              :disabled="isSubmitting"
              round
              size="large"
              :loading="isSubmitting"
              style="width: 100%"
          >
            <el-icon>
              <Microphone/>
            </el-icon>
            Hold to speak
          </el-button>
        </div>
      </div>
    </el-col>
    <el-col :span="10">
      <el-button style="width: 60%" size="large" @click="clearMessage" type="info" round>Clear</el-button>
    </el-col>
  </el-row>

  <el-row class="row-bg" style="align-content: start">
    <el-col :span="5"/>
  </el-row>
  <p>Request time {{ messages.response_time }}</p>
  <div style="display: grid">
    <div
        v-for="(message,index) in all_messages"
        :key="index"
        style="width: 80%"
        :style="message.role === 'assistant' ? 'justify-self: start;' : 'justify-self: end;'"
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
            font-size: small;"
          :class="{ 'gray-background': message.role === 'assistant' , 'user-background': message.role === 'user'}"
      >
        <audio
            ref="audioElement"
            :id="index"
            v-if="message.role === 'assistant' && message.audio"
            :src="`${message.audio}?${Date.now()}`"
            controls
            style="
               text-align: start;
               justify-content: start;
               display: flex;
               width: 90%;
            "
            :autoplay="all_messages.length===1 && this.all_messages[0].role === 'assistant'"
        ></audio>
        <div
            style="
                margin: 0 0 1% 1%;
                justify-content: start;
              "
            v-html="markdownToHtml(message.content)"
        ></div>
      </div>
    </div>
  </div>
  <el-backtop :right="100" :bottom="100"/>
</template>

<style scoped lang="stylus">
.title {
  text-align: start;
  margin: 0 0 4% 0;
  font-size: large;
}

.title-p {
  color: hsla(161, 100%, 24%, 0.66);
  font-weight: bold;
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
}

.user-background {
  background-color: hsla(165, 38%, 81%, 0.4);
  border-radius: 5px;
  align-items: end;
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
</style>

<script>
import axios from 'axios'
import * as marked from 'marked'
import {
  CircleCloseFilled,
  Microphone,
  Promotion,
  UploadFilled,
  VideoPause,
  VideoPlay,
  Delete
} from '@element-plus/icons-vue'
import Recorder from 'js-audio-recorder'
import {getCurrentInstance} from 'vue'

export default {
  components: {Microphone, VideoPlay, VideoPause, CircleCloseFilled, Promotion, UploadFilled, Delete},
  data() {
    const instance = getCurrentInstance();
    return {
      newMessage: '',
      baseUrl: instance?.appContext.config.globalProperties.baseUrl,
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
        "audio": '1'
      },
      isSubmitting: false,
      audioKey: new Date().getTime(),
      file: '',
      fileName:
          "",
      recorder: null,
      recordingStatus: false,
      playTime: 0,
      playingStatus: false,
      audioSrc: "",
      prompts: {},
      initAssistantStatus: false,
      temperature: 1,
      all_messages: [],
      isPressing: false
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
      formData.append('temperature', this.temperature)
      const url = this.baseUrl + 'ask/';
      try {
        const response = await axios.post(url, formData);
        this.messages = response.data
        this.isSubmitting = false
        this.playingStatus = false
        this.recordingStatus = false
        this.audioSrc = `https://testapp.tfg.ltd/api/v2/output/${this.messages.audio}`
        this.audioKey = new Date().getTime()
        this.fetchHistory()
        setTimeout(() => {
          const audioElement = document.getElementById('1');
          if (audioElement) {
            audioElement.play().catch(error => console.error("自动播放失败", error));
          }
        }, 500); // 500毫秒的延迟

      } catch (error) {
        console.error(error);
        this.$message({
          message: error,
          type: 'error'
        })
        this.isSubmitting = false
        this.playingStatus = false
        this.recordingStatus = false
        this.audioSrc = `https://testapp.tfg.ltd/api/v2/output/speech.mp3?timestamp=${new Date().getTime()}`
        this.audioKey = new Date().getTime()
        this.recorder = null
      }
    },
    async submitMessage() {
      try {
        this.isSubmitting = true
        const res = await axios.post(
            this.baseUrl + 'chatCompletion',
            {content: this.newMessage, temperature: this.temperature},
            {
              headers: {
                'Content-Type': 'multipart/form-data'
              }
            }
        );
        this.messages = res.data
        this.newMessage = ''
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
    fetchHistory() {
      try {
        const response = axios.get(this.baseUrl + `messages/?timestamp=${new Date().getTime()}`,
        ).then(res => {
          this.all_messages = this.reversePairs(res.data).filter(message => message.role !== "system")
        })
      } catch (error) {
        this.isLoading = false
        console.error('Error fetching chat history:', error)
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
      const reversedPairs = pairs.reverse();
      const flattened = reversedPairs.flat();
      return flattened;
    },
    async clearMessage() {
      this.messages.response_time = 0
      this.recorder = null
      await axios.get(this.baseUrl + `initMessages/?timestamp=${new Date().getTime()}`)
      await this.fetchHistory()
    },
  },
  beforeUnmount() {
    if (this.timer) {
      clearInterval(this.timer);
    }
  },
  mounted() {
    this.fetchHistory()
    this.audioSrc = `https://testapp.tfg.ltd/api/v2/output/${this.messages.audio}`
    this.$nextTick(() => {
      setTimeout(() => {
        const audioElement = document.getElementById('1');
        if (audioElement) {
          audioElement.play().catch(error => console.error("自动播放失败", error));
        }
      }, 500); // 增加延迟确保audio标签已加载
    });
    this.isPressing = false
    this.recorder.duration = 0
  },
}
</script>
