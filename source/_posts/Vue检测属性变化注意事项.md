title: Vue检测属性变化注意事项
date: 2018-02-28 20:18:20
tags:
    - Vue
categories:
---
在用Vue写前端时，看到同事写的代码里
```
this.subnetIps[String(subnet_id)] = ''
this.subnetIps[String(subnet_id)] = ips
```
觉得很奇怪，为什么要先置空，再赋值？尝试把`this.subnetIps[String(subnet_id)] = ''`去掉后，发现前端的值不会发生变化。于是看Vue文档，在[检测变化的注意事项](https://cn.vuejs.org/v2/guide/reactivity.html#%E6%A3%80%E6%B5%8B%E5%8F%98%E5%8C%96%E7%9A%84%E6%B3%A8%E6%84%8F%E4%BA%8B%E9%A1%B9)里提到这是由于Javascript语言的缺陷造成的。文档里提到可以使用$set方法，于是把两条语句改成`this.$set(this.subnetIps, String(subnet_id), ips)`
