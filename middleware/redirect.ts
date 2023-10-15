import { Middleware } from '@nuxt/types'

const redirect: Middleware = ({ route, redirect }) => {
  redirect(301, 'https://www.pref.toyama.jp/1021/kurashi/kenkou/iryou/virus/index.html')
  /*
  if (route.path.includes('flow')) {
    redirect(
      'http://www.pref.toyama.jp/cms_sec/1205/kj00021473.html'
    )
  }
  */
}

export default redirect
