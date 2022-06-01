<template>
  <div>
    <svg-icon icon-class="back" class="svg" onclick="javascript:history.go(-1);" />
  </div>
</template>

<script>
export default {
  name: 'BackSvg'
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
