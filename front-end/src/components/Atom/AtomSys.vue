<template>
  <br/>
  <el-row class="row-bg" justify="space-between">
    <el-col :span="14" style="margin: 0 0 0 2%">
      <el-input
          v-model="newMessage"
          clearable
          placeholder="Please confirm your name
          يرجى تأكيد اسمك
"
      />
    </el-col>
    <el-col :span="8">
      <el-button
          style="width: 60%"
          size="large"
          @click="submitMessage"
      >
        Confirm
      </el-button>
    </el-col>
  </el-row>

  <el-row class="row-bg" justify="space-between" style="align-items: end;">
    <el-col
        :span="14"
        style="padding: 1% 0 1% 0;display: grid;justify-content: start;width: 100%;min-width: max-content;margin: 0 0 0 2%"
    >
      <div style="
                box-sizing:border-box;
                border-radius: 10px;
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
              size="large"
              :loading="isSubmitting"
              style="width: 100%"
          >
            <el-icon>
              <Microphone/>
            </el-icon>
            Press and hold to say your name
          </el-button>
        </div>
      </div>
    </el-col>
    <el-col :span="8">
      <el-button
          style="width: 60%"
          size="large"
          @click="clearMessage"
      >Clear
      </el-button>
    </el-col>
  </el-row>

  <el-row class="row-bg" justify="space-evenly">
    <el-col :span="5">
      <p v-if="messages.response_time!==0.0">Request time {{ messages.response_time }}</p>
    </el-col>
  </el-row>

  <div style="display: grid">
    <div
        v-for="(message,index) in all_messages"
        :key="index"
        style="width: 80%"
        :style="message.role === 'assistant' ? 'justify-self: start;margin:0 0 0 2%' : 'justify-self: end;margin:0 2% 0 0'"
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
        <div
            style="
                margin: 0 0 1% 1%;
                justify-content: start;
              "
            :class="{'arabic-text': containsArabic(message.content)}"
            v-html="markdownToHtml(message.content)"
        ></div>
        <img v-if="message.role === 'assistant'" style="border-radius: 10px" :src="this.baseUrl+'output/'+message.img"
             alt="img" width="98%"/>
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
  VideoPause,
  VideoPlay
} from '@element-plus/icons-vue'
import Recorder from 'js-audio-recorder'
import {getCurrentInstance} from 'vue'

export default {
  components: {Microphone, VideoPlay, VideoPause, CircleCloseFilled, Promotion, UploadFilled, Delete},
  data() {
    const instance = getCurrentInstance();
    return {
      newMessage: '',
      baseUrl: instance?.appContext.config.globalProperties.atomSysUrl,
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
      recordingStatus: false,
      playTime: 0,
      playingStatus: false,
      audioSrc: "",
      prompts: {},
      initAssistantStatus: false,
      state: true,
      all_messages: [],
      isPressing: false,
      errorContent: ''
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
      const url = this.baseUrl + 'speak/';
      try {
        const response = await axios.post(url, formData);
        this.messages = response.data
        this.isSubmitting = false
        this.playingStatus = false
        this.recordingStatus = false
        this.state = this.messages.check
        this.newMessage = this.messages.name
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
            this.baseUrl + 'check/',
            {content: this.newMessage, state: true},
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
      const reversedPairs = pairs.reverse();
      return reversedPairs.flat();
    },
    async clearMessage() {
      this.messages.response_time = 0
      this.recorder = null
      await axios.get(this.baseUrl + `initMessages/?timestamp=${new Date().getTime()}`)
      await this.fetchHistory()
    },
    containsArabic(text) {
      const arabicPattern = /[\u0600-\u06FF]/;
      return arabicPattern.test(text);
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
