import request from '@/utils/request'

export function getroutes(data) {
  return request({
    // url: 'http://127.0.0.1:5000/User/GetRouter',
    url: '/User/GetRouter',
    method: 'post',
    data
  })
}
