import { login, getInfo } from '@/api/user'
import { getToken, setToken, removeToken } from '@/utils/auth'
import { resetRouter } from '@/router'
import axios from 'axios'

const getDefaultState = () => {
  return {
    token: getToken(),
    name: '',
    sex: '',
    education: '',
    avatar: '',
    roles: [],
    department: '',
    mail: '',
    imp: 0,
    zt_state: '',
    school: '',
    home: '',
    marriage: '',
    birthday: '',
    entrytime: '',
    remark: '',
    creatime: ''
  }
}

const state = getDefaultState()

const mutations = {
  RESET_STATE: (state) => {
    Object.assign(state, getDefaultState())
  },
  SET_TOKEN: (state, token) => {
    state.token = token
  },
  SET_NAME: (state, name) => {
    state.name = name
  },
  SET_SEX: (state, sex) => {
    state.sex = sex
  },
  SET_EDUCATION: (state, education) => {
    state.education = education
  },
  SET_AVATAR: (state, avatar) => {
    state.avatar = avatar
  },
  SET_ROLES: (state, roles) => {
    state.roles = roles
  },
  SET_DEPARTMENT: (state, department) => {
    state.department = department
  },
  SET_MAIL: (state, mail) => {
    state.mail = mail
  },
  SET_IMP: (state, imp) => {
    state.imp = imp
  },
  SET_STATE: (state, zt_state) => {
    state.zt_state = zt_state
  },
  SET_SCHOOL: (state, school) => {
    state.school = school
  },
  SET_HOME: (state, home) => {
    state.home = home
  },
  SET_MARRIAGE: (state, marriage) => {
    state.marriage = marriage
  },
  SET_BIRTHDAY: (state, birthday) => {
    state.birthday = birthday
  },
  SET_ENTRYTIME: (state, entrytime) => {
    state.entrytime = entrytime
  },
  SET_REMARK: (state, remark) => {
    state.remark = remark
  },
  SET_CREATETIME: (state, creatime) => {
    state.creatime = creatime
  }
}

const actions = {
  // user login
  login({ commit }, userInfo) {
    const { username, password } = userInfo
    return new Promise((resolve, reject) => {
      login({ username: username.trim(), password: password }).then(response => {
        const { data } = response
        commit('SET_TOKEN', data.token)
        setToken(data.token)
        resolve()
      }).catch(error => {
        reject(error)
      })
    })
  },

  // get user info
  getInfo({ commit, state }) {
    return new Promise((resolve, reject) => {
      getInfo(state.token).then(response => {
        const { data } = response
        if (!data) {
          return reject('Verification failed, please Login again.')
        }

        const { id, name, roles, department, mail, sex, education, imp, state, school, home, marriage, birthday, entrytime, remark, creatime } = data

        /* 获取二进制图片                                      开始 */
        function arrayBufferToBase64(buffer) {
          // 第一步，将ArrayBuffer转为二进制字符串
          var binary = ''
          var bytes = new Uint8Array(buffer)
          var len = bytes.byteLength
          for (var i = 0; i < len; i++) {
            binary += String.fromCharCode(bytes[i])
          }
          // 将二进制字符串转为base64字符串
          return window.btoa(binary)
        }

        axios({
          method: 'get',
          url: 'http://127.0.0.1:5000/User/GetAvatar',
          responseType: 'arraybuffer', // 最为关键
          params: { 'id': id }
        }).then((response) => {
          commit('SET_AVATAR', 'data:image/jpeg;base64,' + arrayBufferToBase64(response.data))
          /* avatar =
            'data:image/jpeg;base64,' + arrayBufferToBase64(response.data) */
        })
        /* 获取二进制图片                                      结束 */

        commit('SET_NAME', name)
        commit('SET_SEX', sex)
        commit('SET_EDUCATION', education)
        /* commit('SET_AVATAR', avatar) */
        commit('SET_ROLES', roles)
        commit('SET_DEPARTMENT', department)
        commit('SET_MAIL', mail)
        commit('SET_IMP', imp)
        commit('SET_STATE', state)
        commit('SET_SCHOOL', school)
        commit('SET_HOME', home)
        commit('SET_MARRIAGE', marriage)
        commit('SET_BIRTHDAY', birthday)
        commit('SET_ENTRYTIME', entrytime)
        commit('SET_REMARK', remark)
        commit('SET_CREATETIME', creatime)
        resolve(data)
      }).catch(error => {
        reject(error)
      })
    })
  },

  // user logout
  logout({ commit, state }) {
    return new Promise((resolve, reject) => {
      removeToken() // must remove  token  first
      resetRouter()
      commit('RESET_STATE')
      resolve()
    })
  },

  // remove token
  resetToken({ commit }) {
    return new Promise(resolve => {
      removeToken() // must remove  token  first
      commit('RESET_STATE')
      resolve()
    })
  }
}

export default {
  namespaced: true,
  state,
  mutations,
  actions
}
