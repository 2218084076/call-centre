<template>
  <div style="width: 100%">
    <el-row class="row-bg">
      <el-col :span="6">
        <p class="title-p">Call Centre</p>
      </el-col>
    </el-row>
    <div style="align-items: start;flex: inherit;display: flex">
      <div>
        <div class="m-4">
          <el-select
              size="large"
              v-model="value"
              value-key="id"
              placeholder="choose record"
              style="width: 240px"
          >
            <el-option
                v-for="item in names"
                :label="item.label"
                :value="item.value"
            />
          </el-select>
        </div>
      </div>
      <div style="margin: 0 0 0 1%">
        <el-button @click="submitMessage" :loading="isSubmitting" size="large" type="primary" round>Submit
        </el-button>
      </div>
    </div>
    <el-row
        class="row-bg "
        style="
        text-align: start;
        padding: 1%"
    >
      <el-col>
        <div class="inline-flex"
             style="padding: 2%;min-height: 4vh"
             :style="{
          boxShadow: `var(${getCssVarName(shadowObj.type)})`,
        }">
          <div
              style="
              margin: 0 0 1% 1%;
              justify-content: start;
            "
              v-html="markdownToHtml(message.text)"
          ></div>
        </div>
      </el-col>
    </el-row>
  </div>
  <el-backtop :right="100" :bottom="100"/>
</template>

<style scoped lang="stylus">
.title-p {
  color: hsla(161, 100%, 24%, 0.66);
  font-weight: bold;
}

</style>

<script>
import axios from 'axios'
import * as marked from 'marked'
import {getCurrentInstance} from "vue";

export default {
  data() {
    const instance = getCurrentInstance();
    return {
      value: '',
      baseUrl: instance?.appContext.config.globalProperties.baseUrl,
      names: [
        {value: '53660366', label: '53660366'},
        {value: '61229671', label: '61229671'},
        {value: '61618976', label: '61618976'},
        {value: '64018715', label: '64018715'},
        {value: '64081538', label: '64081538'},
        {value: '66806263', label: '66806263'},
        {value: '67775055', label: '67775055'},
        {value: '69720218', label: '69720218'},
        {value: '92710229', label: '92710229'},
        {value: '98107680', label: '98107680'},
      ],
      message: {text: ''},
      isSubmitting: false,
      shadowObj: {
        name: 'Lighter Shadow',
        type: 'lighter',
      },
      temperature: 0.7,
    }
  },
  methods: {
    async submitMessage() {
      this.message = {text: ''}
      let formData = new FormData();
      try {
        console.log(this.value)
        formData.append('name', this.value);
        this.isSubmitting = true
        const res = await axios.post(
            this.baseUrl + 'chatCompletion/',
            formData,
            {
              headers: {
                'Content-Type': 'multipart/form-data',
                timeout: 5000,
              }
            }
        );
        console.log(res)
        this.message = {
          text: res.data.data
        }
      } catch (error) {
        this.isSubmitting = false
        this.message = {text: "Error: " + (error.response?.data || "Request failed")}; // 使用错误消息
      } finally {
        this.isSubmitting = false
      }
    },
    markdownToHtml(markdownString) {
      return marked.marked(markdownString);
    },
    getCssVarName(type) {
      return `--el-box-shadow${type ? '-' : ''}${type}`
    }
  },
}
</script>
