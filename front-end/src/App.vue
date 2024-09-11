<template>
  <router-view></router-view>
</template>

<script>
</script>

<style>
body {
  margin: 0;
}

#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  margin-top: 0;
}

.title-p {
  color: hsla(161, 100%, 24%, 0.66);
  font-weight: bold;
}


.toggle {
  cursor: pointer;
  margin: 20px;
}

.el-upload-dragger {
  padding: 0 0 1% 0;
}

.el-upload {
  --el-upload-dragger-padding-vertical: 1%;
  --el-upload-dragger-padding-horizontal: 1%;
}


.demo-tabs > .el-tabs__content {
  color: #6b778c;
  height: 100%;
  align-items: flex-end;
  min-width: 25%;
  max-width: 100%;
  align-content: center;
}

.el-tabs__item {
  white-space: pre;
  min-width: max-content;
}

.el-tabs__header {
  margin: 0;
}

.el-tabs--left .el-tabs__content {
  height: 100%;
}

.el-tabs__content {
  height: 100%;
  margin: 1%;
}


.el-tabs__nav {
  margin: 0 0 0 2%;
}

</style>
