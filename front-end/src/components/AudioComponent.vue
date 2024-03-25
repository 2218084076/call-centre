<template>
  <div style="padding: 20px;">
    <h3>录音上传</h3>

    <div style="font-size:14px">
      <h3>录音时长：{{ recorder && recorder.duration.toFixed(4) }}</h3>
      <br/>
      <el-button type="primary" @click="handleStart">开始录音</el-button>
      <el-button type="warning" @click="handleStop">停止录音</el-button>
      <br/>
      <br/>
      <h3>
        播放时长：{{
          recorder &&
          (playTime > recorder.duration
              ? recorder.duration.toFixed(4)
              : playTime.toFixed(4))
        }}
      </h3>
      <br/>
      <el-button type="primary" @click="handlePlay">播放录音</el-button>
      <el-button type="warning" @click="handleStopPlay">停止播放</el-button>
      <el-button type="error" @click="handleDestroy">销毁录音</el-button>
      <el-button type="primary" @click="uploadRecord">上传</el-button>
    </div>
  </div>
</template>

<script>
import Recorder from 'js-audio-recorder'
import axios from "axios";
import {h, ref} from "vue";
import * as marked from "marked";
import {ElNotification} from "element-plus";

export default {
  data() {
    return {
      newMessage: '',
      timer: 0,
      baseUrl: 'https://testapp.tfg.ltd/api/v1/',
      messages: [],
      isSubmitting: false,
      isLoading: false,
      file: '',
      fileName: "",
      uploadStatus: '',
      isUploading: false,
      uploadFile: null,
      recorder: null,
      recordingStatus: false,
      recorderUploadStatus: false,
      playTime: 0,
      playingStatus: false,
      audioSrc: "response.mp3"
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
    // 开始录音
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
      this.recorder.stop() // 停止录音
    },
    handlePlay() {
      console.log('播放录音')
      console.log(this.recorder)
      this.recorder.play() // 播放录音

      // 播放时长
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
      const formData = new FormData()
      const blob = this.recorder.getWAVBlob()
      const newbolb = new Blob([blob], {type: 'audio/wav'})
      const fileOfBlob = new File([newbolb], new Date().getTime() + '.wav')
      formData.append('file', fileOfBlob)
      const url = baseUrl + 'audio';
      this.src = url
      try {
        const response = await axios.post(url, formData);
        console.log(response);
        await fetchHistory()
      } catch (error) {
        console.error(error);
      }
    },
    async submitMessage() {
      try {
        this.isSubmitting = true
        this.isLoading = true
        await axios.post(baseUrl + 'askQuestion', {content: newMessage.value, role: 'article_analysis_sys'})
        await fetchHistory()
        this.newMessage = ref('')
      } catch (error) {
        console.error('Error sending message:', error)
      } finally {
        this.isSubmitting = false
        this.isLoading = false
      }
    },
    markdownToHtml(markdownString) {
      return marked.marked(markdownString);
    },
    async submitFile() {
      this.isLoading = true
      let formData = new FormData()
      formData.append('file', file)
      formData.append('role', 'article_analysis_sys')
      notificationBox('Uploading file.')
      try {
        this.isSubmitting = true
        this.isLoading = true
        const response = await axios.post(baseUrl + 'uploadKnowledgeBase', formData, {
          headers: {
            'Content-Type': 'multipart/form-data'
          }
        })
        uploadFile.value = null
        const responseData = response.data
        if (responseData.messages === 'success') {
          isSubmitting = false
          isLoading = false
          uploadStatus = 'success'
        }
      } catch (error) {
        console.error('Error uploading file:', error)
        this.isUploading = false
        this.isSubmitting = false
        this.isLoading = false
        this.uploadStatus = 'Error uploading file:  ' + error
      } finally {
        await fetchHistory()
        this.isSubmitting = false
        this.isLoading = false
      }
    },
    async fetchHistory() {
      try {
        this.isLoading = true
        const response = await axios.get(baseUrl + 'allDialogues',
            {
              params: {
                role: 'article_analysis_sys'
              }
            }
        )
        const responseData = response.data
        if (responseData.message === 'success') {
          const combinedMessages = [...responseData.data.questions, ...responseData.data.answers]
              .sort((a, b) => a.id - b.id)
          messages.value = combinedMessages.map((message, index) => ({
            id: index + 1,
            user: message.user,
            text: message.text
          }))
          this.isLoading = false
        }
      } catch (error) {
        this.isLoading = false
        console.error('Error fetching chat history:', error)
      }
    },
    handleFileUpload(e) {
      this.file = e.raw
      this.fileName = e.name
    },
    notificationBox(text) {
      ElNotification({
        duration: 1000,
        title: 'Message',
        message: h('i', {style: 'color: #337ecc'}, text),
      })
    },
  },
  beforeUnmount() {
    if (this.timer) {
      clearInterval(this.timer);
    }
  }
}
</script>

