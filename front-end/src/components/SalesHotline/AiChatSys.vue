<template>
  <el-button style="margin: 0" size="small" type="danger" icon="Delete" circle @click="clearMessage"/>
  <!-- 消息记录 -->
  <el-scrollbar class="chat-container" height="75vh" style="display: grid" ref="scrollbar">
    <div
        v-for="(message, index) in all_messages"
        :key="index"
        style="display: grid"
        :style="message.role === 'assistant' ? 'justify-self: start;' : 'justify-self: end'"
    >
      <div class="dot" style="font-weight: bold"
           :style="message.role === 'assistant' ? 'text-align: start;' : 'text-align: end;'">
        {{ message.role }}
      </div>
      <div
          style="
              margin: 0 0 1% 0;
              padding: 1% 2% 1% 2%;
              list-style-type: none;
              text-align: justify;
              word-wrap: normal;
              border-radius: 10px;
              font-size: small;
              width: 80%;
            "
          :class="{ 'gray-background': message.role === 'assistant', 'user-background': message.role === 'user' }"
      >
        <el-popover v-if="message.ttsTime" placement="top-start" width="max-content"
                    content="Total time spent on TTS steps">
          <template #reference>
            <el-button type="success" text bg class="m-2">
              <strong>TTS ( {{ message.tts }} )：</strong> {{ timeInSeconds(message.ttsTime) }} s
            </el-button>
          </template>
        </el-popover>
        <el-popover v-if="message.sttTime" placement="top-start" width="max-content"
                    content="Total time spent on STT steps">
          <template #reference>
            <el-button type="success" text bg class="m-2">
              <strong>STT ( {{ message.stt }} )：</strong> {{ timeInSeconds(message.sttTime) }} s
            </el-button>
          </template>
        </el-popover>
        <el-popover v-if="message.gptTime" placement="top-start" width="max-content"
                    content="Total time spent on requesting gpt steps">
          <template #reference>
            <el-button type="success" text bg class="m-2">
              <strong>Ai assistant ({{ message.ai }} - {{ message.model }})：</strong> {{
                timeInSeconds(message.gptTime)
              }} s
            </el-button>
          </template>
        </el-popover>
        <br/>
        <code style="color: #f89898"
              v-if="message.audio && (!message.audio.includes('.mp3') && !message.audio.includes('.wav'))">
          TTS failure:
          <br/>
          {{ message.audio.split('/').slice(-1)[0] }}</code>
        <div
            style="justify-content: start;"
            :class="{ 'arabic-text': containsArabic(message.content) }"
            v-html="markdownToHtml(message.content)"
        ></div>
        <audio
            ref="audioElement"
            :id="index"
            v-if="message.audio.includes('.mp3') || message.audio.includes('.wav')"
            :src="`${message.audio}?${Date.now()}`"
            controls
            preload="auto"
            style="
               text-align: start;
               justify-content: start;
               display: flex;
               height: 40px;
            "
            :autoplay="all_messages.length === 1 && this.all_messages[0].role === 'assistant'"
        ></audio>
      </div>
    </div>
  </el-scrollbar>
  <!-- 输入框 -->
  <div class="input-container">
    <el-row class="row-bg" justify="space-between" style="align-items: center">
      <el-col :span="15" style="">
        <el-input v-model="newMessage" clearable placeholder="Please enter your question" size="large"/>
      </el-col>
      <el-col :span="8">
        <el-button style="width: 60%" size="large" @click="submitMessage">
          Submit
        </el-button>
      </el-col>
    </el-row>
    <br/>
    <!--  语音输入  -->
    <el-row class="row-bg" style="align-items: center;width: 100%" justify="space-between">
      <el-col
          :span="20"
          style=" padding: 1% 0 1% 0; display: grid; justify-content: start; min-width: max-content;"
      >
        <el-button
            :type="isPressing ? 'info' : 'primary'"
            @touchstart.prevent="handleStart"
            @touchend.prevent="uploadRecord"
            @mousedown.prevent="handleStart"
            @mouseup.prevent="uploadRecord"
            :disabled="isSubmitting"
            size="large"
            :loading="isSubmitting"
            style="width: 200%"
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
  padding: 1%;
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
import axios from 'axios';
import * as marked from 'marked';
import {
  Delete,
} from '@element-plus/icons-vue';
import Recorder from 'js-audio-recorder';
import {getCurrentInstance} from 'vue';


export default {
  components: {
    Delete,
  },
  data() {
    const instance = getCurrentInstance();
    return {
      newMessage: '',
      baseUrl: instance?.appContext.config.globalProperties.aiSysUrl,
      messages: {
        message: '',
        data: {
          question: '',
          answer: '',
        },
        response_time: 0.0,
        token: {
          question: 0,
          answer: 0,
        },
        audio: '1',
        check: false,
        gptTime: '0:00:00.000000',
        ttsTime: '0:00:00.000000',
        sttTime: '0:00:00.000000',
        stt: '',
        tts: '',
        ai: '',
        model: ''
      },
      isSubmitting: false,
      audioKey: new Date().getTime(),
      file: '',
      fileName: '',
      recorder: null,
      playTime: 0,
      prompts: {},
      initAssistantStatus: false,
      state: true,
      all_messages: [],
      isPressing: false,
      errorContent: '',
      value: '',
      langOptions: [
        {value: 'en', label: 'en'},
        {value: 'zh', label: 'zh'},
      ],
      finalTranscript: '',
      interimTranscript: '',
      isListening: false,
      recognition: null,
      fullTranscript: '',
      stt_respo: {
        results: '',
        respo_time: '',
      }
    };
  },
  created() {
    this.recorder = new Recorder();
  },
  watch: {
    all_messages() {
      this.$nextTick(() => {
        this.scrollToBottom();
      });
    },
  },
  methods: {
    handleStart() {
      this.isPressing = true;
      this.recorder = new Recorder();
      Recorder.getPermission().then(
          () => {
            console.log('开始录音');
            this.recorder.start(); // 开始录音
          },
          (error) => {
            this.$message({
              message: 'Please allow this page to use the microphone first',
              type: 'info',
            });
            console.log(`${error.name} : ${error.message}`);
          }
      );
    },
    async uploadRecord() {
      this.isPressing = false;
      if (this.recorder == null || this.recorder.duration === 0) {
        return false;
      }
      this.recorder.pause(); // 暂停录音
      this.timer = null;
      this.isSubmitting = true;
      this.$message({
        message: 'Submit recording',
        type: 'info',
      });
      const formData = new FormData();
      const blob = this.recorder.getWAVBlob();
      const newbolb = new Blob([blob], {type: 'audio/wav'});
      const fileOfBlob = new File([newbolb], new Date().getTime() + '.wav');
      formData.append('audio', fileOfBlob);
      formData.append('language', this.value);
      const stt_task_url = this.baseUrl + 'stt/';
      const url = this.baseUrl + 'ask/';
      try {
        const respo = await axios.post(stt_task_url, formData)
        this.stt_respo = respo.data
        if (this.stt_respo.audio) {
          this.all_messages.push({
            role: 'user',
            content: this.stt_respo.results,
            audio: this.stt_respo.audio,
            sttTime: this.stt_respo.respo_time
          });
        }
        const response = await axios.post(url, formData);
        this.messages = response.data;
        this.isSubmitting = false;
        this.fetchHistory();
        this.recorder.duration = null;
        setTimeout(() => {
          const audioElement = document.getElementById('1');
          if (audioElement) {
            audioElement.play().catch((error) => console.error('自动播放失败', error));
          }
        }, 500); // 500毫秒的延迟
      } catch (error) {
        console.error(error);
        this.$message({
          message: error,
          type: 'error',
        });
        this.isSubmitting = false;
        this.audioKey = new Date().getTime();
        this.recorder = null;
        this.fetchHistory();
      }
    },
    async submitMessage() {
      this.scrollToBottom()
      try {
        this.isSubmitting = true;
        this.all_messages.push({role: 'user', content: this.newMessage, audio: '', sttTime: ''});
        const res = await axios.post(
            this.baseUrl + 'completions/',
            {question: this.newMessage},
            {
              headers: {
                'Content-Type': 'multipart/form-data',
              },
            }
        );
        this.messages = res.data;
        if (this.messages.name === 'Please submit the correct name') {
          this.newMessage = this.messages.name;
          this.$message({
            message: this.messages.name,
            type: 'info',
          });
        } else {
          this.fetchHistory();
        }
      } catch (error) {
        console.error('Error sending message:', error);
      } finally {
        this.isSubmitting = false;
        this.fetchHistory();
      }
    },
    markdownToHtml(markdownString) {
      if (markdownString) {
        return marked.marked(markdownString);
      }
    },
    fetchHistory() {
      try {
        axios.get(this.baseUrl + `messages/?timestamp=${new Date().getTime()}`).then((res) => {
          this.all_messages = this.reversePairs(res.data).filter((message) => message.role !== 'system');
        });
        this.newMessage = '';
        this.scrollToBottom()
      } catch (error) {
        this.isLoading = false;
        this.errorContent = error;
        console.error('Error fetching chat history:', error);
        this.newMessage = '';
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
      return pairs.flat();
    },
    async clearMessage() {
      this.messages.response_time = 0;
      this.recorder.duration = null;
      await axios.get(this.baseUrl + `initMessages/?timestamp=${new Date().getTime()}`);
      await this.fetchHistory();
    },
    containsArabic(text) {
      const arabicPattern = /[\u0600-\u06FF]/;
      return arabicPattern.test(text);
    },
    scrollToBottom() {
      const el = this.$refs.scrollbar.$el.querySelector('.el-scrollbar__wrap');
      if (el) {
        el.scrollTo({
          top: el.scrollHeight,
          behavior: 'smooth', // or 'auto' if you want instant scroll
        });
        setTimeout(() => {
          el.scrollTo({
            top: el.scrollHeight,
            behavior: 'smooth', // or 'auto' if you want instant scroll
          });
        }, 100); // 100毫秒的延迟
      }
    },
    timeInSeconds(timStr) {
      return this.convertTimeToSeconds(timStr);
    },
    convertTimeToSeconds(timeStr) {
      if (typeof timeStr !== 'string') {
        console.error('Expected a string but received:', typeof timeStr);
        return 0;
      }
      const timeParts = timeStr.split(':');
      const hours = parseInt(timeParts[0], 10);
      const minutes = parseInt(timeParts[1], 10);
      const seconds = parseFloat(timeParts[2]);

      return hours * 3600 + minutes * 60 + seconds;
    },
    requestMicrophonePermission() {
      navigator.mediaDevices.getUserMedia({audio: true})
          .then((stream) => {
            this.startRecognition();
          })
          .catch((err) => {
            console.error('Error accessing microphone: ', err);
            alert('Microphone access is required for speech recognition.');
          });
    },
    startRecognition() {
      const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
      if (!SpeechRecognition) {
        alert('SpeechRecognition is not supported in this browser.');
        return;
      }

      this.recognition = new SpeechRecognition();
      this.recognition.lang = 'en-US';
      this.recognition.interimResults = true;
      this.recognition.maxAlternatives = 1;

      this.recognition.onresult = (event) => {
        this.interimTranscript = ''; // Clear interim transcript for each new result event

        for (let i = event.resultIndex; i < event.results.length; i++) {
          if (event.results[i].isFinal) {
            this.finalTranscript += event.results[i][0].transcript + ' ';
          } else {
            this.interimTranscript += event.results[i][0].transcript;
          }
        }
      };

      this.recognition.onerror = (event) => {
        console.error('Error occurred in recognition: ', event.error);
      };

      this.recognition.onend = () => {
        if (this.isListening) {
          setTimeout(() => {
            this.recognition.start(); // Restart the recognition with a slight delay to prevent blocking
          }, 100);
        }
      };

      this.recognition.start();
      this.isListening = true;
    },
    stopRecognition() {
      if (this.recognition) {
        this.recognition.stop();
        this.isListening = false;
        this.recognition = null; // Release the recognition instance
      }
    }
  },
  beforeUnmount() {
    if (this.timer) {
      clearInterval(this.timer);
    }
  },
  mounted() {
    this.fetchHistory();
    this.$nextTick(() => {
      this.scrollToBottom();
      setTimeout(() => {
        const audioElement = document.getElementById(`${this.all_messages.length - 1}`);
        if (audioElement) {
          audioElement.play().catch((error) => console.error('Autoplay failure', error));
        }
      }, 560);
    });
    this.isPressing = false;
    this.recorder.duration = 0;
  },
  beforeDestroy() {
    this.stopRecording();
  }
};
</script>
