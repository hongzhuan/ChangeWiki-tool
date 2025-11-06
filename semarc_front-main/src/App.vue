<template>
  <div id="app">
    <router-view />
  </div>
</template>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: white;
}

html, body, #app {
  height: 100%;
  width: 100%;
  /* background-color: rgb(8, 22, 43); */
  background-color: rgb(36, 13, 241);
  padding: 0;
  margin: 0;
  overflow: hidden;
  font-family: "宋体";
  font-size: 16px;
  scrollbar-width: none; /* Firefox */
  -ms-overflow-style: none; /* IE 10+ */
}

::-webkit-scrollbar {
  width: 0 !important;
  height: 0;
}
</style>
