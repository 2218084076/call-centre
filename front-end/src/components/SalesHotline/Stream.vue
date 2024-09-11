<script>
export default {
  data() {
    return {
      isRecording: false,
      mediaRecorder: null,
      socket: null,
      isPressing: false
    };
  },
  methods: {
    async startRecording() {
      try {
        this.isPressing = true
        const stream = await navigator.mediaDevices.getUserMedia({audio: true});
        this.mediaRecorder = new MediaRecorder(stream);
        // this.socket = new WebSocket('ws://testapp.tfg.ltd/api/atom/ws/audio/');
        this.socket = new WebSocket('ws://192.168.8.152:8000/atom/atomStream/ws/audio/');
        this.socket.onopen = () => {
          console.log('WebSocket is connected.');
          this.mediaRecorder.start();

          this.mediaRecorder.ondataavailable = (event) => {
            if (event.data.size > 0 && this.socket.readyState === WebSocket.OPEN) {
              this.socket.send(event.data);
            }
          };

          this.isRecording = true;
        };

        this.socket.onclose = () => {
          console.log('WebSocket is closed.');
        };
      } catch (error) {
        console.error('Error accessing audio media', error);
      }
    },
    stopRecording() {
      this.isPressing = false
      if (this.mediaRecorder) {
        this.mediaRecorder.stop();
      }
      if (this.socket) {
        this.socket.close();
      }
      this.isRecording = false;
    }
  }
};

</script>

<template>
  <el-row class="row-bg" justify="center">
    <el-col :span="20">
      <el-button
          :type="isPressing ? 'info' : 'primary'"
          circle
          class="square-button"
          @touchstart.prevent="startRecording"
          @touchend.prevent="stopRecording"
          @mousedown.prevent="startRecording"
          @mouseup.prevent="stopRecording"
      >
        <el-icon size="80">
          <Microphone/>
        </el-icon>
      </el-button>
    </el-col>
  </el-row>
</template>

<style scoped lang="stylus">

.square-button {
  align-items: center;
  justify-content: center;
  height: 200px;
  width: 200px;
  border-radius: 100%;
  transition: transform 0.4s;
  transform-style: preserve-3d;
  -webkit-transform-style: preserve-3d;
  -moz-transform-style: preserve-3d;
  position: relative;
}
</style>