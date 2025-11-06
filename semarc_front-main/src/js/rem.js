// rem等比适配配置文件
// 基准大小
const baseSize = 16
let rem;

// 设置 rem 函数
function setRem() {
    // 当前页面宽度相对于 1920宽的缩放比例，可根据自己需要修改。
    const scaleX = document.documentElement.clientWidth / 1920
    const scaleY = document.documentElement.clientHeight / 1080
    // 需要取缩放倍数较小的，因为需要宽高都兼容
    if (scaleX > scaleY) {
        // 设置页面根节点字体大小（“Math.min(scale, 2)” 指最高放大比例为2，可根据实际业务需求调整）
        document.documentElement.style.fontSize = baseSize * Math.min(scaleY, 2) + 'px'
        rem = baseSize * Math.min(scaleY, 2)
    } else {
        document.documentElement.style.fontSize = baseSize * Math.min(scaleX, 2) + 'px'
        rem = baseSize * Math.min(scaleX, 2)
    }

}

// 初始化
setRem()
// 改变窗口大小时重新设置 rem
window.onresize = function () {
    setRem()
}

export default function (px) {
    return px * rem
}

export const fontSize = (res) => {
    const clientWidth = window.innerWidth || document.documentElement.clientWidth || document.body.clientWidth;
    if (!clientWidth) return;
    let fontSize = clientWidth / 1920;
    return res * fontSize;
}
