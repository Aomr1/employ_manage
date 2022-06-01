import request from '@/utils/request'

export function login(data) {
  return request({
    // url: 'http://127.0.0.1:5000/User/Login',
    url: '/User/Login',
    method: 'post',
    data
  })
}

export function getInfo(token) {
  return request({
    // url: 'http://127.0.0.1:5000/User/GetInfo',
    url: '/User/GetInfo',
    method: 'get',
    params: { token }
  })
}

// export function logout() {
//   return request({
//     url: '/vue-admin-template/user/logout',
//     // url: '/User/Logout',
//     method: 'post'
//   })
// }
