<script setup lang="ts">

</script>

<template>
  <nav style="align-items: center">
    <router-link to="/realtimeSTT" class="oval-button">
      <el-icon class="icon-item">
        <Service/>
      </el-icon>
      <div class="content">
        <span>RealtimeSTT</span>
        <span class="description"> Realtime STT Demo</span>
      </div>
    </router-link>
    <br/>
    <router-link to="/aiSys" class="oval-button">
      <el-icon class="icon-item">
        <Coordinate/>
      </el-icon>
      <div class="content">
        <span>AI assistant</span>
        <span class="description">Customized AI assistant system</span>
      </div>
    </router-link>
    <br/>

    <router-link to="/chatBot" class="oval-button">
      <el-icon class="icon-item">
        <ChatDotRound/>
      </el-icon>
      <div class="content">
        <span>Chat Bot</span>
      </div>
    </router-link>
    <br/>
    <router-link to="/promptEditor" class="oval-button">
      <el-icon class="icon-item">
        <EditPen/>
      </el-icon>
      <div class="content">
        <span>Prompts Editor</span>
      </div>
    </router-link>
    <br/>
    <!--    <router-link to="/acrosticPoem" class="oval-button">-->
    <!--      <el-icon style="font-size: 40px">-->
    <!--        <Opportunity />-->
    <!--      </el-icon>-->
    <!--      <div class="content">-->
    <!--        <span>Acrostic Poem</span>-->
    <!--      </div>-->
    <!--    </router-link>-->
    <!--    <br/>-->
    <router-link to="/callCentre" class="oval-button">
      <el-icon class="icon-item">
        <HelpFilled/>
      </el-icon>
      <div class="content">
        <span>Call Centre</span>
        <span class="description">Analyze hotline recordings</span>
      </div>
    </router-link>
    <br/>
    <router-link to="/orderSys" class="oval-button">
      <el-icon class="icon-item">
        <DishDot/>
      </el-icon>
      <div class="content">
        <span>Ordering system</span>
      </div>
    </router-link>
  </nav>
  <router-view></router-view>
</template>

<style scoped lang="stylus">
nav {
  display: flex;
  flex-direction: column; /* 确保子元素垂直排列 */
  padding: 5%;
  align-items: flex-start; /* 将子元素对齐到左侧 */
}

.oval-button {
  display: flex;
  align-items: center;
  justify-content: flex-start;
  padding: 10px; /* Adjust based on your needs */
  border: 1px solid #dcdfe6; /* Example border, you can remove it or change its color */
  border-radius: 50px; /* This creates the oval shape */
  font-size: 45px; /* Adjust text size as needed */
  background-color: #f2f2f2; /* Example background, you can change it */
  text-decoration: none; /* Removes underline from links */
  width: 70%;
}

.oval-button el-icon {
  font-size: 40px; /* Icon size, adjust if needed */
  margin-right: 8px; /* Space between icon and text */

}

.oval-button span {
  vertical-align: middle;
}

.content {
  display: flex;
  flex-direction: column;
  align-items: flex-start;
  font-size: 30px;
}

.description {
  font-size: 20px; /* Smaller font size for the description */
  color: #909399; /* Lighter text color for the description */
}

.icon-item {
  font-size: 40px;
  margin: 1%
}

</style>