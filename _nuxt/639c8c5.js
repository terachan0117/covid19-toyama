(window.webpackJsonp=window.webpackJsonp||[]).push([[27],{442:function(t,e,n){var content=n(583);"string"==typeof content&&(content=[[t.i,content,""]]),content.locals&&(t.exports=content.locals);(0,n(19).default)("0d8d65f8",content,!0,{sourceMap:!1})},581:function(t){t.exports=JSON.parse('{"date":"2021/07/07 16:23","data":{"place":{"display":{"@ja":"富山駅","@en":"Toyama Sta."}},"date":"2021-07-06","data":[{"reference_date":"2021-07-05","increase_rate":4}]}}')},582:function(t,e,n){"use strict";n(442)},583:function(t,e,n){(e=n(18)(!1)).push([t.i,".StayingPopulation[data-v-2067a7de]{background-color:#fff;box-shadow:0 0 2px rgba(0,0,0,.15);border:.5px solid #d9d9d9!important;border-radius:4px;padding:18px;min-height:5em;display:flex;align-items:center}.StayingPopulation .StayingPopulation-title[data-v-2067a7de]{text-align:left;font-size:1.9rem;color:#4d4d4d;font-weight:600;font-size:1.2rem}.StayingPopulation .StayingPopulation-place[data-v-2067a7de]{padding:5px;margin:2px 5px 2px 10px;background-color:#008830;color:#fff;vertical-align:middle;text-align:center;-ms-writing-mode:tb-rl;writing-mode:vertical-rl;font-weight:600;font-size:1.2rem}.StayingPopulation .StayingPopulation-state[data-v-2067a7de]{flex:1;padding:2px;margin:2px 5px;border:2px solid #008830;text-align:center;vertical-align:middle;min-width:15em;font-size:1.1rem}",""]),t.exports=e},615:function(t,e,n){"use strict";n.r(e);var o=n(13),r=n.n(o),l=n(1),d=n(581),c=l.default.extend({filters:{formatDate:function(text){return r()(text).format("YYYY年MM月DD日")},arrow:function(t){return 0===t?0:(t>0?"↑":"↓")+Math.abs(t)}},data:function(){return{StayingPopulation:d,placeName:d.data.place.display,date:r()(d.data.date).format("YYYY年MM月DD日")}}}),f=(n(582),n(7)),m=n(34),v=n.n(m),_=n(600),component=Object(f.a)(c,(function(){var t=this,e=t.$createElement,n=t._self._c||e;return n("v-col",{attrs:{cols:"12",md:"6"}},[n("div",{staticClass:"StayingPopulation"},[n("div",{staticClass:"StayingPopulation-title"},[t._v("\n      "+t._s(t.$t("滞在人口の増減状況"))),n("br"),t._v(" "),n("app-link",{attrs:{to:"https://mobaku.jp/covid-19/archive/hokuriku.html#area_0"}},[t._v(t._s(t.$t("詳細はこちら"))+"\n      ")])],1),t._v(" "),["ja","ja-basic"].includes(t.$i18n.locale)?n("div",{staticClass:"StayingPopulation-place"},[t._v("\n      "+t._s(t.placeName["@ja"])+"\n    ")]):n("div",{staticClass:"StayingPopulation-place"},[t._v(t._s(t.placeName["@en"]))]),t._v(" "),n("div",{staticClass:"StayingPopulation-state"},[t._v("\n      [ "+t._s(t.date)+"時点 ]"),n("br"),t._v(" "),t._l(t.StayingPopulation.data.data,(function(data,e){return n("span",{key:e},[t._v("\n        "+t._s(t._f("formatDate")(data.reference_date))+"比\n        "+t._s(t._f("arrow")(data.increase_rate))+"％"),n("br")])})),t._v("\n      出典元: NTTドコモ\n    ")],2)])])}),[],!1,null,"2067a7de",null);e.default=component.exports;v()(component,{AppLink:n(48).default}),v()(component,{VCol:_.a})}}]);