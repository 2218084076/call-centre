<script setup lang="ts">
import {ref, onMounted, onUnmounted, getCurrentInstance, ComponentInternalInstance, computed} from 'vue';
import {ElTag} from 'element-plus'
import {ElMessage} from 'element-plus'

const instance = getCurrentInstance() as ComponentInternalInstance | null;
const wsUrl: string = instance?.appContext.config.globalProperties.realTimeSTT;

const displayDiv = ref<HTMLElement | null>(null);
const server_available = ref(false);
const mic_available = ref(false);
const fullSentences = ref<object[]>([]);

const serverCheckInterval = 5000; // Check every 5 seconds
let socket: WebSocket | null = null;

function connectToServer() {
  if (socket) {
    socket.close();
  }

  socket = new WebSocket(wsUrl);

  socket.onopen = () => {
    server_available.value = true;
  };

  socket.onmessage = (event) => {
    const data = JSON.parse(event.data);

    if (data.type === 'realtime') {
      // displayRealtimeText(data.text);
    } else if (data.type === 'fullSentence') {
      ElMessage({
        message: 'Receive a reply.',
        type: 'success',
        showClose: true,
        duration: 1000
      })
      fullSentences.value.push({text: data.text, check: data.check});
      // displayRealtimeText(""); // Refresh display with new full sentence
    }
  };

  socket.onclose = () => {
    server_available.value = false;
  };
}

function displayRealtimeText(realtimeText: string) {
  if (!displayDiv.value) return;

  const displayedText = fullSentences.value.map((sentence, index) => {
    const p = document.createElement('p');
    p.textContent = sentence + " ";
    p.className = index % 2 === 0 ? 'yellow' : 'cyan';
    return p.outerHTML;
  }).join('') + realtimeText;

  displayDiv.value.innerHTML = displayedText;
}

function start_msg() {
  if (!mic_available.value) {
    displayRealtimeText("🎤  please allow microphone access  🎤");
  } else if (!server_available.value) {
    displayRealtimeText("🖥️  please start server  🖥️");
  } else {
    displayRealtimeText("👄  start speaking  👄");
  }
}

const displayedMessage = computed(() => {
  if (!mic_available.value) {
    return {component: ElTag, props: {type: 'warning'}, children: '🎤  please allow microphone access  🎤'};
  } else if (!server_available.value) {
    return {component: ElTag, props: {type: 'danger'}, children: '🖥️  please start server  🖥️'};
  } else {
    return {component: ElTag, props: {type: 'success'}, children: '🎙️  start speaking  🎙️'};
  }
});

function checkServerAvailability() {
  setInterval(() => {
    if (!server_available.value) {
      connectToServer();
    }
  }, serverCheckInterval);
}

function requestMicrophoneAccess() {
  navigator.mediaDevices.getUserMedia({audio: true})
      .then(stream => {
        const audioContext = new AudioContext();
        const source = audioContext.createMediaStreamSource(stream);
        const processor = audioContext.createScriptProcessor(256, 1, 1);

        source.connect(processor);
        processor.connect(audioContext.destination);
        mic_available.value = true;

        processor.onaudioprocess = (e) => {
          const inputData = e.inputBuffer.getChannelData(0);
          const outputData = new Int16Array(inputData.length);

          // Convert to 16-bit PCM
          for (let i = 0; i < inputData.length; i++) {
            outputData[i] = Math.max(-32768, Math.min(32767, inputData[i] * 32768));
          }

          // Send the 16-bit PCM data to the server
          if (socket && socket.readyState === WebSocket.OPEN) {
            const metadata = JSON.stringify({sampleRate: audioContext.sampleRate});
            const metadataBytes = new TextEncoder().encode(metadata);
            const metadataLength = new ArrayBuffer(4);
            const metadataLengthView = new DataView(metadataLength);
            metadataLengthView.setInt32(0, metadataBytes.byteLength, true); // true for little-endian
            // const combinedData = new Blob([metadataLength, metadataBytes, outputData.buffer]);
            const combinedData = new Blob([outputData.buffer]);
            socket.send(combinedData);
          }
        };
      })
      .catch(e => console.error(e));
}

function replaceLineBreaks(text: string) {
  text = '- ' + text
  return text.replace(/--- /g, '<br/><br/>- ');
}

onMounted(() => {
  connectToServer();
  checkServerAvailability();
  requestMicrophoneAccess();
});

onUnmounted(() => {
  if (socket) {
    socket.close();
  }
});
</script>

<template>
  <el-row class="row-bg" justify="center" id="app">
    <!--  demo desc  -->
    <el-col :span="24">
      <el-tag
          style="margin: 1%;word-wrap: break-word;white-space: pre-wrap;height: max-content;padding: 1%;line-height: 1.5"
          type="info"
      >
        Use "Real-time STT" to determine in real time whether the content you are currently listening to is the answer
        to the specified question
        <br/>
        Q1: "What's your name?"
        <br/>
        Q2: "Which house are you in?"
      </el-tag>
    </el-col>
    <!--  service state  -->
    <el-col :span="24">
      <el-tag
          effect="plain"
          v-bind="displayedMessage.props"
          v-html="displayedMessage.children"
          style="line-height: 1.5"
      ></el-tag>
    </el-col>
    <!--  Realtime transcription record   -->
    <el-col :span="24">
      <el-scrollbar height="75vh">
        <el-tag
            v-for="(item,index) in fullSentences.slice().reverse()"
            :type="item.check ? 'success' : (index % 2 === 0 ? 'primary' : 'info')"
            :key="item"
            size="large"
            style="word-wrap: break-word;white-space: pre-wrap;text-align: start;padding: 1%;height: auto;line-height: 1.5"
            class="scrollbar-demo-item"
        >
          <span>{{ item.text }}</span>
          <el-tag
              :type="item.check ? 'success':'danger'"
              effect="dark"
              round>Check: {{ item.check }}
          </el-tag>
        </el-tag>
      </el-scrollbar>
    </el-col>
  </el-row>
</template>

<style scoped lang="stylus">
.scrollbar-demo-item {
  display: flex;
  align-items: center;
  justify-content: center;
  margin: 1%;
  padding: 1%;
}

</style>
