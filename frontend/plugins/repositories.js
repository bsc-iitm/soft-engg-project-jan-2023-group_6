import createRepository from '~/repositories/Repository'

export default (ctx, inject) => {
  const api = ctx.$axios.create({
    headers: {
      common: {
        'x-bb-channelid': 'WEB',
      },
    },
  })

  if (ctx.$cookies.get('user')) {
    api.interceptors.request.use(function (config) {
      config.headers.Authorization = `Bearer ${ctx.$cookies.get('user').token}`

      return config
    })
  }

  inject('repositories', createRepository(api))
}
