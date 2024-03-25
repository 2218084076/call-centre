<template>
  <div style="width: 100%">
    <p class="title-p">Article Analysis System</p>
    <div class="upload-file"
    >
      <el-upload
          drag
          action="https://run.mocky.io/v3/9d059bf9-4660-45f2-925d-ce80ad6c4d15"
          @change="handleFileUpload"
          multiple
          :disabled="initAssistantStatus"
      >
        <el-icon class="el-icon--upload">
          <upload-filled/>
        </el-icon>
        <div class="el-upload__text">
          Please select knowledge base file
          <em>click to select</em>
        </div>
      </el-upload>
      <el-row class="row-bg" style="align-items: center">
        <el-col :span="3">
          Edit prompt
        </el-col>
        <el-col :span="17">
          <el-input
              v-model="prompts.prompts"
              clearable
              type="textarea"
              :autosize="{ minRows: 4, maxRows: 6}"
              placeholder="Enter prompt"
              :disabled="!initAssistantStatus"
          />
          <em>token count: {{ prompts.token }}</em>
        </el-col>
        <el-col :span="4">
          <el-button
              round
              type="primary"
              @click="submitFile"
              class="upload-file-button"
              :loading="uploadKnowledgeBase"
          >
            Upload
          </el-button>
        </el-col>
      </el-row>
    </div>
    <el-row class="row-bg" style="align-items: center;margin: 1% 0 0 0">
      <el-col :span="3">
        Edit question
      </el-col>
      <el-col :span="17">
        <el-input
            placeholder="Please enter your question"
            v-model="newMessage"
            :disabled="isSubmitting"
            :class="{'input-isSubmitting': isSubmitting,'input-text-box':!isSubmitting}"
            @keydown.enter="submitMessage"
            clearable
            type="textarea"
        />
      </el-col>
      <el-col :span="4">
        <el-button
            round
            type="primary"
            @click="submitMessage"
            @keydown.enter="submitMessage"
            :class="{ 'common-button': !isSubmitting}"
            :disabled="isSubmitting || isUploading"
            :loading="isSubmitting"
            style="font-size: large"
        >
          submit
        </el-button>
      </el-col>
    </el-row>
    <el-row class="row-bg" style="align-content: start">
      <el-col :span="3"/>
      <el-col :span="17" style=" padding: 1% 0 1% 0;display: grid;justify-content: start;">
        <div style="
                box-sizing:border-box;
                border: 1px dashed var(--el-border-color);
                border-radius: 10px;
                padding: 4%;
                width:max-content;
                height: max-content;
          ">
          <div v-if="!recordingStatus || playingStatus">
            <div class="title">Duration(录音时长): {{
                recorder && recorder.duration.toFixed(4)
              }}
            </div>
            <div style="justify-content: start;display: flex">
              <el-button
                  type="success"
                  @click="handleStart"
                  :disabled="recordingStatus"
                  round
                  size="large"
              >
                <el-icon>
                  <Microphone/>
                </el-icon>
              </el-button>
              <el-button
                  type="danger"
                  @click="handleStop"
                  round
                  size="large"
              >
                <el-icon>
                  <VideoPause/>
                </el-icon>
              </el-button>
              <el-button
                  type="primary"
                  @click="uploadRecord"
                  round
                  :disabled="recorderUploadStatus"
                  :loading="isSubmitting"
                  size="large"
              >
                <el-icon>
                  <Promotion/>
                </el-icon>
                submit
              </el-button>
            </div>
          </div>
          <div v-if="recordingStatus">
            <div class="title"> Play time(播放时长)：{{
                recorder &&
                (playTime > recorder.duration
                    ? recorder.duration.toFixed(4)
                    : playTime.toFixed(4))
              }}
            </div>
            <div style="justify-content: start;display: flex">
              <el-button
                  type="primary"
                  @click="handlePlay"
                  round
                  size="large"
              >
                <el-icon>
                  <VideoPlay/>
                </el-icon>
              </el-button>
              <el-button
                  type="warning"
                  @click="handleStopPlay"
                  round
                  size="large"
              >
                <el-icon>
                  <VideoPause/>
                </el-icon>
              </el-button>
              <el-button
                  type="info"
                  @click="handleDestroy"
                  round
                  size="large"
              >
                <el-icon>
                  <CircleCloseFilled/>
                </el-icon>
              </el-button>
              <el-button
                  type="primary"
                  @click="uploadRecord"
                  round
                  :disabled="recorderUploadStatus"
                  :loading="isSubmitting"
                  size="large"
              >
                <el-icon>
                  <Promotion/>
                </el-icon>
                submit
              </el-button>
            </div>
          </div>
        </div>
      </el-col>
    </el-row>
    <div
        v-for="message in messages" :key="message.id" :id="message.id"
        style="
            margin: 0 0 1% 0;
            padding: 2% 3% 2% 2%;
            justify-content: space-around;
            list-style-type: none;
            text-align: justify;
            word-wrap: normal;
            border-radius: 20px;
            font-size: small;
        "
        :class="{ 'gray-background': message.user === 'Assistant' , 'user-background': message.user === 'User'}"
    >
      <div class="dot" style="font-weight: bold;margin: 0 0 1% 0">
        {{ message.user }}:
        <div v-html="getDate(message.createdAt)"></div>
        <div>Total token: {{ message.token }}</div>
      </div>
      <div
          style="padding: 0 0 1% 1%"
          v-if="
            messages.length> 1 &&
            message.audioStart !== message.audioEnd
    ">
        Audio Total time consumed:
        <em v-html="getDate(message.audioStart)"></em>
        ---
        <em v-html="getDate(message.audioEnd)"></em>
      </div>
      <audio
          v-if="message.id === firstAssistantMessageId"
          :controls="hasMultipleAssistantMessages"
          :src="audioSrc"
          style="
             text-align: start;
             justify-content: start;
             display: flex;
             width: 90%;
          "
      ></audio>
      <div
          style="
              margin: 0 0 1% 1%;
              justify-content: start;
            "
          v-html="markdownToHtml(message.text)"
      ></div>
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

.disabled {
  pointer-events: none;
  opacity: 0.6;
  color: rgba(0, 0, 0, 0);
}

.el-upload-dragger .el-icon--upload {
  margin: 0;
}

.el-upload-dragger {
  max-height: max-content;
  padding: 0 2% 0 2%;
}


.title-p {
  font-size: large;
  color: hsla(161, 100%, 24%, 0.66);
  font-weight: bold;
  width: max-content;
}

.upload-file-button {
  height: max-content;
  cursor: pointer;
  min-width: 10%;
  margin: 2% 0 0 0;
  font-size: large;
}

.button-group {
  display: flex;
  align-items: center;
  justify-content: flex-start;
  margin: 1% 0 1% 0;
}

.upload-file {
  display: grid;
}

.circular {
  display: inline;
  height: 30px;
  width: 30px;
  animation: loading-rotate 2s linear infinite;
}

.path {
  animation: loading-dash 1.5s ease-in-out infinite;
  stroke-dasharray: 90, 150;
  stroke-dashoffset: 0;
  stroke-width: 2;
  stroke: var(--el-color-primary);
  stroke-linecap: round;
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

.input-isSubmitting {
  color: #949393;
  font-size: large;
  border-radius: 5px;
  border: 1px solid hsla(160, 100%, 37%, 1);
  font-family: emoji;
  display: flex;
  align-items: center;
  background-color: rgba(243, 243, 243, 0.68);
  justify-content: space-around;
}

.input-text-box {
  font-size: large;
  font-family: emoji;
  display: flex;
  align-items: center;
  justify-content: space-around;
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
}

.user-background {
  background-color: hsla(165, 38%, 81%, 0.4);
  border-radius: 5px;
}

.common-button {
  border: none;
  cursor: pointer;
  min-width: max-content;
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

.loading {
  animation: rotate 1s linear infinite;
  width: 4%;
  height: 4vh;
}

.is-not-loading {
  fill: rgba(40, 40, 40, 0);
  display: none;
}

.btn {
  display: flex;
  padding: 1% 1%;
  margin-bottom: 0;
  line-height: 1.42857143;
  text-align: center;
  white-space: nowrap;
  vertical-align: middle;
  cursor: pointer;
  border: #ccc 1px solid;
  border-radius: 4px;
  color: #333;
  background-color: #fff;
  align-items: center;
  min-height: 3vh;
  max-height: 3vh;
}
</style>

<script>
import axios from 'axios'
import * as marked from 'marked'
import {CircleCloseFilled, Microphone, Promotion, UploadFilled, VideoPause, VideoPlay} from '@element-plus/icons-vue'
import Recorder from 'js-audio-recorder'
import {getCurrentInstance} from "vue";

export default {
  components: {Microphone, VideoPlay, VideoPause, CircleCloseFilled, Promotion, UploadFilled},
  data() {
    const instance = getCurrentInstance();
    return {
      newMessage: '',
      timer: 0,
      baseUrl: instance?.appContext.config.globalProperties.baseUrl,
      messages: [],
      uploadKnowledgeBase: false,
      isLoading: false,
      isSubmitting: false,
      isUploading: false,
      file: '',
      fileName: "",
      uploadStatus: '',
      uploadFile: null,
      recorder: null,
      recordingStatus: false,
      recorderUploadStatus: false,
      playTime: 0,
      playingStatus: false,
      audioSrc: "response.mp3?_=" + new Date().getTime(),
      role: 'article_analysis_sys',
      prompts: {},
      initAssistantStatus: false
    }
  },
  computed: {
    hasMultipleAssistantMessages() {
      let assistantMessageCount = this.messages.filter(message => message.user === 'Assistant').length;
      return assistantMessageCount > 1;
    },
    firstAssistantMessageId() {
      const assistantMessages = this.messages.filter(message => message.user === 'Assistant');
      if (assistantMessages.length > 0) {
        return Math.min(...assistantMessages.map(message => message.id));
      }
      return null;
    }
  },
  created() {
    this.recorder = new Recorder()
  },
  methods: {
    handleStart() {
      this.recorder = new Recorder()
      Recorder.getPermission().then(() => {
        console.log('开始录音')
        this.recorder.start() // 开始录音
      }, (error) => {
        this.$message({
          message: '请先允许该网页使用麦克风',
          type: 'info'
        })
        console.log(`${error.name} : ${error.message}`)
      })
    },
    handleStop() {
      console.log('停止录音')
      this.recorder.stop()
      this.recordingStatus = true
    },
    handlePlay() {
      console.log('播放录音')
      this.recorder.play() // 播放录音
      this.timer = setInterval(() => {
        try {
          this.playTime = this.recorder.getPlayTime()
        } catch (error) {
          this.timer = null
        }
      }, 100)
    },
    handleStopPlay() {
      console.log('停止播放')
      this.recorder.stopPlay() // 停止播放

      // 播放时长
      this.playTime = this.recorder.getPlayTime()
      this.timer = null
    },
    handleDestroy() {
      console.log('销毁实例')
      this.recorder.destroy() // 毁实例
      this.timer = null
      this.playingStatus = false
      this.recordingStatus = false
    },
    async uploadRecord() {
      if (this.recorder == null || this.recorder.duration === 0) {
        this.$message({
          message: '请先录音',
          type: 'error'
        })
        return false
      }
      this.recorder.pause() // 暂停录音
      this.timer = null
      this.isSubmitting = true
      const formData = new FormData()
      const blob = this.recorder.getWAVBlob()
      const newbolb = new Blob([blob], {type: 'audio/wav'})
      const fileOfBlob = new File([newbolb], new Date().getTime() + '.wav')
      formData.append('file', fileOfBlob)
      formData.append('role', this.role)
      const url = this.baseUrl + `audio?timestamp=${new Date().getTime()}`;
      try {
        const response = await axios.post(url, formData);
        await this.fetchHistory()
        this.isSubmitting = false
        this.playingStatus = false
        this.recordingStatus = false
        await this.fetchHistory()
        this.audioSrc = ''
        this.audioSrc = "response.mp3"
      } catch (error) {
        console.error(error);
        this.$message({
          message: error,
          type: 'error'
        })
        this.isSubmitting = false
        this.playingStatus = false
        this.recordingStatus = false
        await this.fetchHistory()
        this.audioSrc = ''
        this.audioSrc = "response.mp3"
      }
    },
    async submitMessage() {
      try {
        this.isSubmitting = true
        await axios.post(
            this.baseUrl + 'askQuestion',
            {content: this.newMessage, role: this.role},
            {
              headers: {
                'Content-Type': 'multipart/form-data'
              }
            }
        );
        await this.fetchHistory()
        this.newMessage = ''
        await this.fetchHistory()
        this.audioSrc = ''
        this.audioSrc = "response.mp3"
      } catch (error) {
        console.error('Error sending message:', error)
        this.newMessage = ''
        await this.fetchHistory()
        this.audioSrc = ''
        this.audioSrc = "response.mp3"
      } finally {
        this.isSubmitting = false
        this.newMessage = ''
        await this.fetchHistory()
        this.audioSrc = ''
        this.audioSrc = "response.mp3"
      }
    },
    markdownToHtml(markdownString) {
      return marked.marked(markdownString);
    },
    async submitFile() {
      this.$message({
        message: 'Upload Knowledge Base files',
        type: 'info'
      })
      let formData = new FormData()
      formData.append('file', this.file)
      formData.append('role', this.role)
      formData.append('prompts', this.prompts.prompts)
      this.initAssistantStatus = false
      try {
        this.uploadKnowledgeBase = true
        const response = await axios.post(this.baseUrl + 'uploadKnowledgeBase', formData, {
          headers: {
            'Content-Type': 'multipart/form-data'
          }
        })
        this.uploadFile = null
        const responseData = response.data
        if (responseData.messages === 'success') {
          this.isSubmitting = false
          this.isLoading = false
          this.uploadKnowledgeBase = false
          this.uploadStatus = 'success'
          this.$message({
            message: 'Successfully Knowledge Base.',
            type: 'success'
          })
          await this.fetchHistory()
        }
      } catch (error) {
        console.error('Error uploading file:', error)
        this.isUploading = false
        this.isSubmitting = false
        this.isLoading = false
        this.$message({
          message: 'Error uploading file:  ' + error,
          type: 'error'
        })
        await this.fetchHistory()
      } finally {
        this.uploadKnowledgeBase = false
        await this.fetchHistory()
      }
    },
    async fetchHistory() {
      try {
        const response = await axios.get(this.baseUrl + `allDialogues?timestamp=${new Date().getTime()}`,
            {
              params: {
                role: this.role
              }
            }
        )
        const responseData = response.data
        if (responseData.message === 'success') {
          if (
              responseData.data &&
              responseData.data.answers &&
              responseData.data.answers.length > 0 &&
              responseData.data.answers[0].content === ""
          ) {
            this.$message({
              message: 'Initializing',
              type: 'info'
            })
          } else {
            const combinedMessages = [...responseData.data.answers, ...responseData.data.questions]
            this.messages = []
            this.messages = combinedMessages.map((message, index) => ({
              id: message.id,
              user: message.role,
              text: message.content,
              token: message.token,
              audioStart: message.audio_start,
              audioEnd: message.audio_end,
              createdAt: message.update_time
            })).sort((a, b) => a.id - b.id)
            this.isLoading = false
          }
        }
      } catch (error) {
        this.isLoading = false
        console.error('Error fetching chat history:', error)
      }
    },
    handleFileUpload(e) {
      this.file = e.raw
      this.fileName = e.name
      this.initAssistantStatus = true
    },
    getDate(text) {
      let date = new Date(text);
      return date.getFullYear() + '-'
          + (date.getMonth() + 1).toString().padStart(2, '0') + '-'
          + date.getDate().toString().padStart(2, '0') + ' '
          + date.getHours().toString().padStart(2, '0') + ':'
          + date.getMinutes().toString().padStart(2, '0') + ':'
          + date.getSeconds().toString().padStart(2, '0');
    },
    async getPrompts() {
      try {
        this.isSubmitting = true
        const res = await axios.get(this.baseUrl + 'prompts?assistants=' + this.role)
        const resData = res.data.data
        this.prompts = {
          prompts: resData.prompt,
          token: resData.token
        }
      } catch (error) {
        console.error('Error sending message:', error)
        this.prompts = ''
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
    this.getPrompts()
    this.audioSrc = ""
    this.audioSrc = "response.mp3?_=" + new Date().getTime()
    this.fetchHistory()
  },
  watch: {
    prompts(newVal) {
      if (newVal === '') {
        this.getPrompts();
      }
    },
  },
}
</script>
