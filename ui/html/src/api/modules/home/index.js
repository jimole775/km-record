/**
 * 基础模块
 */
import http from '@/utils/http'
// const base = '/api'
const base = '/mock'
export default {
  getuser () {
    return {
      code: 200,
      message: 'success',
      data: {
        currentRole: {
          createdBy: '12345678',
          creationDate: 1561691744000,
          description: '测试员',
          id: 28,
          lastUpdateBy: '12345678',
          lastUpdateDate: 1619687230000,
          roleName: '测试员',
          status: '1',
          type: 'SYSTEM'
        },
        apartmentCode: '001',
        apartmentName: '测试',
        createdBy: null,
        creationDate: null,
        deptCodeList: null,
        email: null,
        employeeNumber: '12345678',
        employeeNumberList: null,
        id: 15,
        ids: null,
        image: '',
        lastUpdateBy: '',
        lastUpdateDate: '2021-05-27 17:19:26',
        name: '测试员',
        noticeReadDate: 123,
        orgCodeList: null,
        permissionAccount: null,
        redisTime: 12345,
        roleId: null,
        roleIdList: null,
        supplierAbbreation: null,
        supplierCode: null,
        type: 1
      }
    }
    // return http.get(`${base}/home/user`)
  },
  getPermissionMenu () {
    return []
    // return http.get(`${base}/home/menu`)
  },
  getuserpool () {
    return {}
    // return http.get(`${base}/home/user-pool`)
  }
}
