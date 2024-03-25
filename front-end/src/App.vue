<template>
  <!--  <nav>-->
  <!--    <router-link to="/">Sales Hotline</router-link>-->
  <!--    |-->
  <!--    <router-link to="/callCentre">Call Centre</router-link>-->
  <!--  </nav>-->
  <router-view></router-view>
</template>

<script>
</script>

<style>
body {
  margin-top: 0;
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

.el-tabs--top .el-tabs__item.is-top:nth-child(2) {
  padding: 10%;
}

.el-tabs--top .el-tabs__item.is-top:last-child {
  padding: 10%;
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
  background-color: aliceblue;
  white-space: pre;
  min-width: max-content;
  min-height: 5vh;
  margin: 0 10% 0 0;
  padding: 0;
}

.el-tabs__header {
  height: 5vh;
  margin: 0;
}

.el-tabs--left .el-tabs__content {
  height: 100%;
}

.el-tabs__content {
  height: 100%;
}

.el-upload-dragger {
  border: 1px dashed #79bbff
}

</style>
