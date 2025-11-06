<!-- filepath: src/components/Login.vue -->
<template>
  <div class="login-container">
    <h2>用户登录</h2>
    <input class= "input_area" v-model="username" placeholder="用户名" />
    <input class= "input_area" v-model="password" type="password" placeholder="密码" />
    <button class="btn" style=" color: black; border-color: black; font-size: 1.2rem; font-family: 'Courier New', Courier, monospace;" @click="login">登录</button>
    <button class="btn" style=" color: black; border-color: black; font-size: 1.2rem; font-family: 'Courier New', Courier, monospace;" @click="register">注册</button>
    <p v-if="error" style="color:red">{{ error }}</p>
  </div>
</template>

<script>

export default {
  data() {
    return {
      username: "",
      password: "",
      error: "",
      rules: {
        username: [
          { required: true, message: "用户名不能为空！", trigger: "blur" },
        ],
        password: [
          { required: true, message: "密码不能为空！", trigger: "blur" },
        ],
      },
    };
  },
  methods: {
    async login() {
      this.error = ''
      if (!this.username.trim() || !this.password.trim()) {
        this.error = '用户名和密码不能为空'
        return
      }
      try {
        const res = await fetch('http://localhost:5000/api/login', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({
            username: this.username,
            password: this.password
          })
        })
        const data = await res.json()
        if (res.ok) {
          localStorage.setItem('isLogin', 'true')
          localStorage.setItem('username', data.username)
          localStorage.setItem('uid', data.uid)
          localStorage.setItem('isAdmin', data.is_admin ? '1' : '0')
          this.$router.push('/HomePagecopy')
        } else {
          this.error = data.message || '登录失败'
        }
      } catch (e) {
        this.error = '网络错误，请稍后重试'
      }
    },
    register() {
      // 简单演示，实际应调用后端API
      this.$router.push("/Register");
    //   alert("注册功能尚未实现");
    }
  }
};
</script>

<style scoped>
.input_area {
  width: 100%;
  max-width: 500px;
  margin: 5px auto 10px auto;
  position: relative;
  margin-bottom: 10px;
  position: relative;
  z-index: 1;
  animation: fadeInUp 1s ease-out 0.6s both;
  justify-content: center; /* 水平居中 */
}
.login-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  min-height: 100vh;
  padding: 20px;
  background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
  position: relative;
  overflow: hidden;
  cursor: pointer;
}
.login-container input {
  margin: 8px 0;
  padding: 8px;
  width: 200px;
}
.login-container button {
  margin-top: 12px;
  padding: 8px 24px;
}
</style>