import {Message} from "element-ui";

export const addZero = (data) => {
    return data < 10 ? ('0' + data) : data;
};

// 校验有效日期
export const isValidDate = (date) => {
    let reg = /^((([1][8-9][0-9][0-9]|[2][0-9]{3})-(((0[13578]|1[02])-(0[1-9]|[12][0-9]|3[01]))|((0[469]|11)-(0[1-9]|[12][0-9]|30))|(02-(0[1-9]|[1][0-9]|2[0-8]))))|((([1][8-9]|[2][0-9])(0[48]|[2468][048]|[13579][26])|(([2][048])00))-02-29))$/;
    if (!reg.test(date)) {
        date = '';
    }
    return date;
};

// 校验有效时间
export const isValidTime = (time) => {
    let reg = /^(([0-1][0-9])|(2[0-3])):([0-5][0-9]):([0-5][0-9])$/;
    if (!reg.test(time)) {
        time = '';
    }
    return time;
};

// 校验激活时间和失效时间是否有效
export const checkDateAndTime = (activateTime, deactivateTime) => {
    if (activateTime === '') return true;
    if (deactivateTime === '') return true;

    let activate = typeof (activateTime) === "number" ? activateTime : Date.parse(activateTime);
    let deactivate = Date.parse(deactivateTime);
    return activate < deactivate;
};

// 数组向前移动元素
export const moveIndexToFront = (arr, index) => {
    if (index < 1) return arr;
    arr[index] = arr.splice(index - 1, 1, arr[index])[0];
    return arr;
};

// 数组向后移动元素
export const moveIndexToBack = (arr, index) => {
    if (index >= arr.length - 1) return arr;
    arr[index] = arr.splice(index + 1, 1, arr[index])[0];
    return arr;
};

export const showMsg = (type, content) => {
    Message({
        message: content, type: type, showClose: true, center: true
    })
}

// 获取时间戳
export const transformTimeToTimestamp = (date, time) => {
    return Date.parse(new Date(date + ' ' + time));
}

// 格式化时间
export const formatDate = (fmt) => {
    /**
     *  fmt : return
     * "YY" : "2022"
     * "YY-MM" : "2022-06"
     * "YY-MM-DD" : "2022-06-02"
     * "YY-MM-DD hh:mm:ss" : "2022-06-02 14:20:56"
     * "星期W" : "星期一"
     * */
    const date = new Date()
    const o = {
        'Y+': date.getFullYear(),
        'M+': date.getMonth() + 1, // 月
        'D+': date.getDate(), // 日
        'h+': date.getHours(), // 时
        'm+': date.getMinutes(), // 分
        's+': date.getSeconds(), // 秒
        W: date.getDay() // 周
    }
    for (let k in o) {
        if (new RegExp('(' + k + ')').test(fmt)) {
            fmt = fmt.replace(RegExp.$1, () => {
                if (k === 'W') {
                    // 星期几
                    const week = ['日', '一', '二', '三', '四', '五', '六']
                    return week[o[k]]
                } else if (k === 'Y+' || RegExp.$1.length === 1) {
                    // 年份 or 小于10不加0
                    return o[k]
                } else {
                    return ('00' + o[k]).substr(('' + o[k]).length) // 小于10补位0
                }
            })
        }
    }
    return fmt
}