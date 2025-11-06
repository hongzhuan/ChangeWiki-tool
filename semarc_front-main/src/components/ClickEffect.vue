<template>
  <div></div>
</template>

<script>
export default {
  data() {
    return {
       emojis: ['🍉', '🥝', '🍓', '🍏', '🌶', '🥕', '🥥', '🍒', '🍑', '🫐'], // 点击效果的表情符号
    };
  },
  methods: {
    createClickEffect(event) {
      const emojiCount = 3; // 每次点击生成的表情符号数量
      const x = event.clientX;
      const y = event.clientY;

      // for (let i = 0; i < emojiCount; i++) {
      //   const emoji = this.emojis[Math.floor(Math.random() * this.emojis.length)];
      //   const clickEffect = document.createElement('div');
      //   clickEffect.className = 'click-effect';
      //   clickEffect.textContent = emoji;

      //   // 随机偏移位置
      //   const offsetX = (Math.random() - 0.5) * 100; // -50 到 50 的随机值
      //   const offsetY = (Math.random() - 0.5) * 100; // -50 到 50 的随机值

      //   clickEffect.style.left = `${x + offsetX}px`;
      //   clickEffect.style.top = `${y + offsetY}px`;

      //   // 添加到页面
      //   document.body.appendChild(clickEffect);

      //   // 动画结束后移除元素
      //   setTimeout(() => {
      //     clickEffect.remove();
      //   }, 2000);
      // }
    },
  },
};
</script>

<style>
.click-effect {
  position: fixed;
  pointer-events: none;
  font-size: 2rem;
  animation: fireworkEffect 2s ease-out forwards;
  z-index: 9999;
  user-select: none;
}

@keyframes fireworkEffect {
  0% {
    transform: scale(1) translateY(0);
    opacity: 1;
  }
  100% {
    transform: scale(1) translateY(500px); /* 降落到底部 */
    opacity: 0;
  }
}
</style>