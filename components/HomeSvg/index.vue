<template>
  <div>
    <router-link to="/">
      <svg-icon icon-class="home" class="svg" />
    </router-link>
  </div>
</template>

<script>
export default {
  name: 'HomeSvg'
}
</script>

<style scoped>
  .svg {
    display: inline-block;
    cursor: pointer;
    fill: #5a5e66;
    width: 20px;
    height: 20px;
    vertical-align: 10px;
    font-size: 20px;
  }
</style>
